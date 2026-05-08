#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v schema2py >/dev/null 2>&1; then
	echo "schema2py not found on PATH" >&2
	exit 1
fi

generated_count=0

while IFS= read -r schema_file; do
	relative_path="${schema_file#apis/}"
	domain="${relative_path%%/*}"
	remainder="${relative_path#*/}"
	version="${remainder%%/*}"
	filename="${schema_file##*/}"
	module_name="${filename%.schema.json}"
	output_path="pkgs/apis/${domain}/${version}/${module_name}.py"

	mkdir -p "$(dirname "$output_path")"
	schema2py -schema "$schema_file" -out "$output_path"
	generated_count=$((generated_count + 1))
done < <(find apis -type f -name '*.schema.json' | sort)

if [[ "$generated_count" -eq 0 ]]; then
	echo "No schema files found under apis/." >&2
	exit 1
fi

echo "Generated ${generated_count} model file(s)."
