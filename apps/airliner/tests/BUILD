python_requirement(
    name="pydantic",
    requirements=["pydantic>=2.0"],
)

python_tests(
    name="tests",
    dependencies=["//apps/airliner/src:lib", "//pkgs/generated:airliner", "//apis/airliner/v1:schema", ":fixtures", ":pydantic"],
)

files(
    name="fixtures",
    sources=["fixtures/*.json"],
)
