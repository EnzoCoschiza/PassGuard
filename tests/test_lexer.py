from app.schemas import TokenType
from app.services.lexer import tokenize_password


def test_tokenizes_reference_password() -> None:
    tokens = tokenize_password("UTN@2026segura")
    assert [(token.type, token.value) for token in tokens] == [
        (TokenType.UPPERCASE_WORD, "UTN"),
        (TokenType.SYMBOL, "@"),
        (TokenType.NUMBER, "2026"),
        (TokenType.LOWERCASE_WORD, "segura"),
    ]


def test_tokenizes_mixed_word() -> None:
    tokens = tokenize_password("abcDEF")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.MIXED_WORD
    assert tokens[0].value == "abcDEF"


def test_tokenizes_whitespace() -> None:
    tokens = tokenize_password("   ")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.WHITESPACE


def test_groups_symbols() -> None:
    tokens = tokenize_password("!!!")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.SYMBOL
    assert tokens[0].value == "!!!"
