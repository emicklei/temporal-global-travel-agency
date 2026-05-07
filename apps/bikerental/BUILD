python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_sources(
    name="lib",
    sources=["workflows/**/*.py", "worker/**/*.py", "activities/**/*.py"],
    dependencies=[
        "//pkgs/apis:bikerental",
        "//pkgs/logger/src:lib",
        ":temporalio",
    ],
)
