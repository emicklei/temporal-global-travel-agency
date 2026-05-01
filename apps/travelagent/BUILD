python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_sources(
    name="lib",
    sources=["workflows/**/*.py", "worker/**/*.py", "activities/**/*.py"],
    dependencies=[
        "//pkgs/apis:airliner",
        "//pkgs/apis:bikerental",
        "//pkgs/apis:citytaxi",
        "//pkgs/apis:travelagent",
        "//pkgs/logger/src:lib",
        ":temporalio",
    ],
)
