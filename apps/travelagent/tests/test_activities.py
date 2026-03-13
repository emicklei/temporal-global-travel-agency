from travelagent.activities import compose_hello_message


def test_compose_hello_message_returns_expected_text() -> None:
    assert (
        compose_hello_message("Temporal traveler")
        == "Hello, Temporal traveler! Welcome to Temporal Travel Agent."
    )


def test_compose_hello_message_preserves_name_formatting() -> None:
    assert (
        compose_hello_message("  Ada Lovelace  ")
        == "Hello,   Ada Lovelace  ! Welcome to Temporal Travel Agent."
    )
