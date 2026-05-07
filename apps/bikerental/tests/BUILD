python_requirement(
    name="pydantic",
    requirements=["pydantic>=2.0"],
)

python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_tests(
    name="tests",
    dependencies=[
        "//apps/bikerental:lib",
        "//pkgs/apis:bikerental",
        "//pkgs/logger/src:lib",
        ":fixtures",
        ":pydantic",
        ":temporalio",
    ],
)

files(
    name="fixtures",
    sources=["fixtures/*.json"],
)
