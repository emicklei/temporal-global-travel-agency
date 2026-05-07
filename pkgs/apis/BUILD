python_requirement(
    name="pydantic",
    requirements=["pydantic>=2.0"],
)

python_requirement(
    name="nexus-rpc",
    requirements=["nexus-rpc>=1.0.0"],
)

python_sources(
    name="airliner",
    sources=["airliner/**/*.py"],
    dependencies=[":pydantic", ":nexus-rpc"],
)

python_sources(
    name="bikerental",
    sources=["bikerental/**/*.py"],
    dependencies=[":pydantic", ":nexus-rpc"],
)

python_sources(
    name="citytaxi",
    sources=["citytaxi/**/*.py"],
    dependencies=[":pydantic", ":nexus-rpc"],
)

python_sources(
    name="tourguide",
    sources=["tourguide/**/*.py"],
    dependencies=[":pydantic", ":nexus-rpc"],
)

python_sources(
    name="travelagent",
    sources=["travelagent/**/*.py"],
    dependencies=[":pydantic", ":nexus-rpc"],
)
