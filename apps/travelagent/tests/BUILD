python_requirement(
    name="temporalio",
    requirements=["temporalio>=1.8.0"],
)

python_tests(
    name="tests",
    dependencies=[
        "//apps/travelagent:lib",
        "//pkgs/apis:travelagent",
        "//pkgs/apis:airliner",
        "//pkgs/apis:bikerental",
        "//pkgs/apis:citytaxi",
        ":fixtures",
        ":temporalio",
    ],
)

files(
    name="fixtures",
    sources=["fixtures/*.json"],
)
