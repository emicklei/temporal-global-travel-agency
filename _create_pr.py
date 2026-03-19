#!/usr/bin/env python3
"""Commit and create PR for Pydantic model generator refactor."""

import subprocess
import sys

# Stage all changes
subprocess.run(["git", "add", "-A"], check=True)

# Commit with a clear message
commit_msg = """refactor: switch API model generator to Pydantic BaseModel

- Updated scripts/generate_api_models.py to generate Pydantic BaseModel with field_validator
- Added ConfigDict(extra='forbid', strict=True) to enforce schema constraints
- Regenerated all API models (airliner, citytaxi, travelagent)
- Refactored airliner tests to use generated FlightPlan model directly
- Removed custom FlightPlanSchemaModel duplicate class
- Added pydantic requirements to generated/BUILD and airliner/tests/BUILD"""

result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr, file=sys.stderr)
    sys.exit(1)

print("✓ Committed changes")

# Create pull request
pr_msg = """## Summary
- Refactor JSON schema generator to produce Pydantic BaseModel classes instead of dataclass
- Implement field_validator decorators for pattern matching and datetime validation
- Regenerate all API models with Pydantic-based output
- Refactor airliner tests to use generated FlightPlan model for schema validation

## How it works
- JSON schemas in apis/** define all constraints (patterns, datetime formats, additionalProperties)
- Generator now emits Pydantic models with ConfigDict(strict=True, extra='forbid')
- field_validator decorators enforce constraints that can't be expressed in type annotations
- Tests validate both type safety and schema constraint compliance

## Verification
- ./pants test apps/airliner/tests:: ✓
"""

pr_result = subprocess.run(
    ["gh", "pr", "create", "--head", "feature/servicenow-temporal-activity", "-t", "refactor: switch to Pydantic models", "-b", pr_msg],
    capture_output=True, text=True
)
print(pr_result.stdout)
if pr_result.returncode != 0:
    print("Warning:", pr_result.stderr, file=sys.stderr)
else:
    print("✓ Pull request created")
