python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_sources(
    name="lib",
    sources=["servicenow/**/*.py"],
    dependencies=[":temporalio"],
)
