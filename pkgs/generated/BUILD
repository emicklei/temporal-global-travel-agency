python_requirement(
    name="pydantic",
    requirements=["pydantic>=2.0"],
)

python_sources(
    name="airliner",
    sources=["__init__.py", "airliner/**/*.py"],
)

python_sources(
    name="citytaxi",
    sources=["__init__.py", "citytaxi/**/*.py"],
)

python_sources(
    name="travelagent",
    sources=["__init__.py", "travelagent/**/*.py"],
    dependencies=[":pydantic"],
)
