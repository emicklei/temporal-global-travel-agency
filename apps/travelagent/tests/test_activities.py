from temporalio.testing import ActivityEnvironment  # pants: no-infer-dep

from travelagent.activities import compose_hello_message


def test_compose_hello_message_with_activity_environment() -> None:
    env = ActivityEnvironment()
    result = env.run(compose_hello_message, "Temporal traveler")

    assert result == "Hello, Temporal traveler! Welcome to Temporal Travel Agent."


def test_compose_hello_message_preserves_name_formatting_with_environment() -> None:
    env = ActivityEnvironment()
    result = env.run(compose_hello_message, "  Ada Lovelace  ")

    assert result == "Hello,   Ada Lovelace  ! Welcome to Temporal Travel Agent."
