from fastapi import APIRouter, Request

from src.core.config import settings

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/health/cors")
async def cors_debug(request: Request):
    """Temporary helper to verify Origin vs configured CORS origins in production."""
    configured = settings.get_cors_origins()
    origin = request.headers.get("origin")
    return {
        "configured_origins": configured,
        "request_origin": origin,
        "origin_allowed": origin in configured if origin else None,
    }
