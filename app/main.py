from fastapi import FastAPI

from app.schemas import AnalyzePasswordRequest, AnalyzePasswordResponse, HealthResponse
from app.services.analyzer import analyze_password

app = FastAPI(title="PassGuard CI API")


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok", service="passguard-ci-api")


@app.post("/password/analyze", response_model=AnalyzePasswordResponse)
def analyze_endpoint(payload: AnalyzePasswordRequest) -> AnalyzePasswordResponse:
    return analyze_password(payload.password)
