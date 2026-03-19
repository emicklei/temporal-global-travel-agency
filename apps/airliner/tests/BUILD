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
        "//apps/airliner/src:lib",
        "//pkgs/generated:airliner",
        "//apis/airliner/v1:schema",
        ":fixtures",
        ":pydantic",
        ":temporalio",
    ],
)

files(
    name="fixtures",
    sources=["fixtures/*.json"],
)
