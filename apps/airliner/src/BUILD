python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_requirement(
    name="structlog",
    requirements=["structlog>=24.4.0"],
)

python_sources(
    name="lib",
    sources=["airliner/**/*.py"],
    dependencies=[
        ":temporalio",
        ":structlog",
        "//pkgs/generated:airliner",
    ],
)
