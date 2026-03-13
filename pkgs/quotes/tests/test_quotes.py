from quotes import random_scientist_quote


EXPECTED_QUOTES = {
    "Somewhere, something incredible is waiting to be known. - Carl Sagan",
    "Nothing in life is to be feared, it is only to be understood. - Marie Curie",
    "If I have seen further it is by standing on the shoulders of Giants. - Isaac Newton",
    "The important thing is to never stop questioning. - Albert Einstein",
    "Science and everyday life cannot and should not be separated. - Rosalind Franklin",
}


def test_random_scientist_quote_returns_known_quote() -> None:
    assert random_scientist_quote() in EXPECTED_QUOTES
