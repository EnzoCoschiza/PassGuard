import re

from app.schemas import AnalyzePasswordResponse, SecurityLevel, Token, TokenType, WarningItem
from app.services.lexer import tokenize_password

RULE_ORDER = [
    "MIN_LENGTH",
    "HAS_LOWERCASE",
    "HAS_UPPERCASE",
    "HAS_NUMBER",
    "HAS_SYMBOL",
    "YEAR_NOT_DETECTED",
    "NO_SIMPLE_SEQUENCE",
    "NO_EXCESSIVE_REPETITION",
]

SEQUENCE_PATTERNS = ("123", "abc", "qwerty")
YEAR_PATTERN = re.compile(r"(19\d{2}|20\d{2})")
REPETITION_PATTERN = re.compile(r"(.)\1\1+")

WARNING_MESSAGES = {
    "YEAR_DETECTED": "La contrasena contiene un ano reconocible.",
    "SIMPLE_SEQUENCE_DETECTED": "La contrasena contiene una secuencia simple.",
    "EXCESSIVE_REPETITION_DETECTED": "La contrasena contiene repeticiones excesivas.",
    "WHITESPACE_DETECTED": "La contrasena contiene espacios en blanco.",
}


def analyze_password(password: str) -> AnalyzePasswordResponse:
    tokens = tokenize_password(password)
    warnings = _collect_warnings(password, tokens)
    rule_results = _evaluate_rules(password, warnings)
    score = _calculate_score(rule_results, warnings)
    level = _calculate_level(score, rule_results["MIN_LENGTH"], warnings)

    passed_rules = [rule for rule in RULE_ORDER if rule_results[rule]]
    failed_rules = [rule for rule in RULE_ORDER if not rule_results[rule]]

    return AnalyzePasswordResponse(
        score=score,
        level=level,
        tokens=tokens,
        warnings=warnings,
        passed_rules=passed_rules,
        failed_rules=failed_rules,
    )


def _collect_warnings(password: str, tokens: list[Token]) -> list[WarningItem]:
    warning_codes: list[str] = []
    lowered = password.lower()

    if YEAR_PATTERN.search(password):
        warning_codes.append("YEAR_DETECTED")
    if any(pattern in lowered for pattern in SEQUENCE_PATTERNS):
        warning_codes.append("SIMPLE_SEQUENCE_DETECTED")
    if REPETITION_PATTERN.search(password):
        warning_codes.append("EXCESSIVE_REPETITION_DETECTED")
    if any(token.type == TokenType.WHITESPACE for token in tokens):
        warning_codes.append("WHITESPACE_DETECTED")

    return [WarningItem(code=code, message=WARNING_MESSAGES[code]) for code in warning_codes]


def _evaluate_rules(password: str, warnings: list[WarningItem]) -> dict[str, bool]:
    warning_codes = {item.code for item in warnings}
    return {
        "MIN_LENGTH": len(password) >= 8,
        "HAS_LOWERCASE": any("a" <= char <= "z" for char in password),
        "HAS_UPPERCASE": any("A" <= char <= "Z" for char in password),
        "HAS_NUMBER": any(char.isdigit() for char in password),
        "HAS_SYMBOL": any(_is_ascii_symbol(char) for char in password),
        "YEAR_NOT_DETECTED": "YEAR_DETECTED" not in warning_codes,
        "NO_SIMPLE_SEQUENCE": "SIMPLE_SEQUENCE_DETECTED" not in warning_codes,
        "NO_EXCESSIVE_REPETITION": "EXCESSIVE_REPETITION_DETECTED" not in warning_codes,
    }


def _calculate_score(rule_results: dict[str, bool], warnings: list[WarningItem]) -> int:
    score = 0

    if rule_results["MIN_LENGTH"]:
        score += 25
    if rule_results["HAS_LOWERCASE"]:
        score += 15
    if rule_results["HAS_UPPERCASE"]:
        score += 15
    if rule_results["HAS_NUMBER"]:
        score += 15
    if rule_results["HAS_SYMBOL"]:
        score += 15
    if (
        rule_results["HAS_LOWERCASE"]
        and rule_results["HAS_UPPERCASE"]
        and rule_results["HAS_NUMBER"]
        and rule_results["HAS_SYMBOL"]
    ):
        score += 15

    for warning in warnings:
        if warning.code == "YEAR_DETECTED":
            score -= 30
        elif warning.code == "SIMPLE_SEQUENCE_DETECTED":
            score -= 25
        elif warning.code == "EXCESSIVE_REPETITION_DETECTED":
            score -= 25
        elif warning.code == "WHITESPACE_DETECTED":
            score -= 10

    return max(0, min(100, score))


def _calculate_level(
    score: int,
    min_length_passed: bool,
    warnings: list[WarningItem],
) -> SecurityLevel:
    if not min_length_passed:
        return SecurityLevel.WEAK
    if score <= 39:
        return SecurityLevel.WEAK
    if score <= 74:
        return SecurityLevel.MEDIUM
    if len(warnings) >= 2:
        return SecurityLevel.MEDIUM
    return SecurityLevel.STRONG


def _is_ascii_symbol(char: str) -> bool:
    return not char.isalnum() and not char.isspace() and ord(char) < 128
