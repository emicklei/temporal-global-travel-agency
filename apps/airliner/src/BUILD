python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_sources(
    name="lib",
    sources=["airliner/**/*.py"],
    dependencies=[
        ":temporalio",
        "//pkgs/generated:airliner",
        "//pkgs/logger/src:lib",
    ],
)
