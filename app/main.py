import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AnalyzePasswordRequest, AnalyzePasswordResponse, HealthResponse
from app.services.analyzer import analyze_password

app = FastAPI(title="PassGuard CI API")


def _allowed_origins() -> list[str]:
    configured = os.getenv("CORS_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://enzog.github.io",
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok", service="passguard-ci-api")


@app.post("/password/analyze", response_model=AnalyzePasswordResponse)
def analyze_endpoint(payload: AnalyzePasswordRequest) -> AnalyzePasswordResponse:
    return analyze_password(payload.password)
