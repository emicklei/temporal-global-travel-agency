#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v schema2py >/dev/null 2>&1; then
	echo "schema2py not found on PATH" >&2
	exit 1
fi

if [[ ! -d "apis" ]]; then
	echo "No schema files found under apis/." >&2
	exit 1
fi

python_files_under_apis="$(find apis -type f -name '*.py' | sort)"
if [[ -n "$python_files_under_apis" ]]; then
	echo "Python files are not allowed under apis/. Keep generated models under pkgs/generated/." >&2
	echo "$python_files_under_apis" >&2
	exit 1
fi

validated_count=0

while IFS= read -r schema_file; do
	schema2py -validate -schema "$schema_file"
	validated_count=$((validated_count + 1))
done < <(find apis -type f -name '*.schema.json' | sort)

if [[ "$validated_count" -eq 0 ]]; then
	echo "No schema files found under apis/." >&2
	exit 1
fi

echo "Schema validation passed for ${validated_count} file(s)."