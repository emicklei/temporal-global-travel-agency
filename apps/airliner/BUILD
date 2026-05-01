python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_sources(
    name="lib",
    sources=["workflows/**/*.py", "worker/**/*.py", "activtities/**/*.py"],
    dependencies=[
        "//pkgs/apis:airliner",
        "//pkgs/logger/src:lib",
        ":temporalio",
    ],
)
