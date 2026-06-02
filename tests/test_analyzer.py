from app.schemas import SecurityLevel
from app.services.analyzer import analyze_password


def test_short_password_is_weak() -> None:
    result = analyze_password("Ab1!")
    assert result.level == SecurityLevel.WEAK
    assert "MIN_LENGTH" in result.failed_rules


def test_missing_symbol_is_medium() -> None:
    result = analyze_password("Password9")
    assert result.level == SecurityLevel.MEDIUM
    assert result.score == 70
    assert "HAS_SYMBOL" in result.failed_rules


def test_complete_password_is_strong() -> None:
    result = analyze_password("Xyzt!789")
    assert result.level == SecurityLevel.STRONG
    assert result.score == 100


def test_year_detection_penalizes_score() -> None:
    result = analyze_password("Xyzt!2026")
    warning_codes = [warning.code for warning in result.warnings]
    assert "YEAR_DETECTED" in warning_codes
    assert result.score == 70


def test_sequence_detection_penalizes_score() -> None:
    result = analyze_password("Abcd!123")
    warning_codes = [warning.code for warning in result.warnings]
    assert "SIMPLE_SEQUENCE_DETECTED" in warning_codes
    assert result.score == 75
    assert result.level == SecurityLevel.STRONG


def test_repetition_detection_penalizes_score() -> None:
    result = analyze_password("Xyz!!!12")
    warning_codes = [warning.code for warning in result.warnings]
    assert "EXCESSIVE_REPETITION_DETECTED" in warning_codes
    assert result.score == 75
    assert result.level == SecurityLevel.STRONG


def test_score_is_bounded_at_zero() -> None:
    result = analyze_password("abc   ")
    assert result.score == 0
    assert result.level == SecurityLevel.WEAK


def test_score_is_bounded_at_hundred() -> None:
    result = analyze_password("Secure!9")
    assert result.score == 100


def test_multiple_warnings_prevent_strong_level() -> None:
    result = analyze_password("Xyz2026!!!")
    assert result.score == 45
    assert result.level == SecurityLevel.MEDIUM


def test_whitespace_is_reported() -> None:
    result = analyze_password("Abcd 123!")
    warning_codes = [warning.code for warning in result.warnings]
    assert "WHITESPACE_DETECTED" in warning_codes
