import logging

from fastapi import APIRouter, Header, HTTPException

from src.schemas.auth import AuthMeResponse, AuthRegisterRequest, AuthRegisterResponse
from src.services.auth_service import AuthError, AuthService

logger = logging.getLogger(__name__)

router = APIRouter()
_service = AuthService()

_ERROR_STATUS = {
    "unauthorized": 401,
    "not_found": 404,
    "conflict": 409,
    "validation": 422,
    "unavailable": 503,
}


@router.post("/auth/register", response_model=AuthRegisterResponse, status_code=201)
async def registrar_usuario(data: AuthRegisterRequest):
    try:
        return _service.registrar_usuario(data)
    except AuthError as exc:
        status_code = _ERROR_STATUS.get(exc.code, 503)
        logger.warning(
            "POST /auth/register rechazado status=%s email=%s detalle=%s",
            status_code,
            data.email,
            exc,
        )
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("POST /auth/register error no controlado email=%s", data.email)
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc


@router.get("/auth/me", response_model=AuthMeResponse)
async def obtener_usuario_actual(
    authorization: str | None = Header(default=None),
):
    try:
        return _service.obtener_usuario_actual(authorization)
    except AuthError as exc:
        raise HTTPException(
            status_code=_ERROR_STATUS.get(exc.code, 401),
            detail=str(exc),
        ) from exc
