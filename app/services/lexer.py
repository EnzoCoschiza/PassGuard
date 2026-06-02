from app.schemas import Token, TokenType


def _char_group(char: str) -> str:
    if "a" <= char <= "z":
        return "lower"
    if "A" <= char <= "Z":
        return "upper"
    if "0" <= char <= "9":
        return "number"
    if char.isspace():
        return "whitespace"
    if ord(char) < 128:
        return "symbol"
    return "unknown"


def _token_type_for_letters(segment: str) -> TokenType:
    has_lower = any("a" <= char <= "z" for char in segment)
    has_upper = any("A" <= char <= "Z" for char in segment)
    if has_lower and has_upper:
        return TokenType.MIXED_WORD
    if has_lower:
        return TokenType.LOWERCASE_WORD
    return TokenType.UPPERCASE_WORD


def tokenize_password(password: str) -> list[Token]:
    if password == "":
        return []

    tokens: list[Token] = []
    buffer = password[0]
    current_group = _char_group(password[0])

    for char in password[1:]:
        next_group = _char_group(char)
        if current_group in {"lower", "upper"} and next_group in {"lower", "upper"}:
            buffer += char
            current_group = "letters"
            continue
        if current_group == "letters" and next_group in {"lower", "upper"}:
            buffer += char
            continue
        if next_group == current_group:
            buffer += char
            continue
        tokens.append(_build_token(buffer, current_group))
        buffer = char
        current_group = next_group

    tokens.append(_build_token(buffer, current_group))
    return tokens


def _build_token(segment: str, group: str) -> Token:
    if group in {"lower", "upper", "letters"}:
        token_type = _token_type_for_letters(segment)
    elif group == "number":
        token_type = TokenType.NUMBER
    elif group == "whitespace":
        token_type = TokenType.WHITESPACE
    elif group == "symbol":
        token_type = TokenType.SYMBOL
    else:
        token_type = TokenType.UNKNOWN
    return Token(type=token_type, value=segment)
