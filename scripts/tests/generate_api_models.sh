#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

if ! command -v schema2py >/dev/null 2>&1; then
	echo "schema2py not found on PATH" >&2
	exit 1
fi

ensure_future_annotations_import() {
	local file_path="$1"
	if grep -q '^from __future__ import annotations$' "$file_path"; then
		return
	fi

	if head -n 1 "$file_path" | grep -q '^#'; then
		tmp_file="$(mktemp)"
		{
			head -n 1 "$file_path"
			echo
			echo 'from __future__ import annotations'
			tail -n +2 "$file_path"
		} >"$tmp_file"
		mv "$tmp_file" "$file_path"
	else
		tmp_file="$(mktemp)"
		{
			echo 'from __future__ import annotations'
			cat "$file_path"
		} >"$tmp_file"
		mv "$tmp_file" "$file_path"
	fi
}

patch_travelagent_route_properties_model() {
	local file_path="$1"
	if [[ "$file_path" != "pkgs/generated/travelagent/v1/journey.py" ]]; then
		return
	fi

	perl -0pi -e 's/class RouteProperties\(BaseModel\):\n\s+model_config = ConfigDict\(extra="forbid", strict=True\)/class RouteProperties(BaseModel):\n    model_config = ConfigDict(extra="allow", strict=True\)/' "$file_path"
}

generated_count=0

while IFS= read -r schema_file; do
	relative_path="${schema_file#apis/}"
	domain="${relative_path%%/*}"
	remainder="${relative_path#*/}"
	version="${remainder%%/*}"
	filename="${schema_file##*/}"
	module_name="${filename%.schema.json}"
	output_path="pkgs/generated/${domain}/${version}/${module_name}.py"

	mkdir -p "$(dirname "$output_path")"
	schema2py -schema "$schema_file" -out "$output_path"
	ensure_future_annotations_import "$output_path"
	patch_travelagent_route_properties_model "$output_path"
	generated_count=$((generated_count + 1))
done < <(find apis -type f -name '*.schema.json' | sort)

if [[ "$generated_count" -eq 0 ]]; then
	echo "No schema files found under apis/." >&2
	exit 1
fi

echo "Generated ${generated_count} model file(s)."