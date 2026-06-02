from enum import Enum

from pydantic import BaseModel, StrictStr


class SecurityLevel(str, Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


class TokenType(str, Enum):
    LOWERCASE_WORD = "LOWERCASE_WORD"
    UPPERCASE_WORD = "UPPERCASE_WORD"
    MIXED_WORD = "MIXED_WORD"
    NUMBER = "NUMBER"
    SYMBOL = "SYMBOL"
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"


class Token(BaseModel):
    type: TokenType
    value: str


class WarningItem(BaseModel):
    code: str
    message: str


class AnalyzePasswordRequest(BaseModel):
    password: StrictStr


class AnalyzePasswordResponse(BaseModel):
    score: int
    level: SecurityLevel
    tokens: list[Token]
    warnings: list[WarningItem]
    passed_rules: list[str]
    failed_rules: list[str]


class HealthResponse(BaseModel):
    status: str
    service: str
