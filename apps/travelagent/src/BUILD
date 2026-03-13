python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_sources(
    name="lib",
    sources=["travelagent/**/*.py"],
    dependencies=[":temporalio"],
)
