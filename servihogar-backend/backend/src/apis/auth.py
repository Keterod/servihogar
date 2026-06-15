from fastapi import APIRouter, Header, HTTPException

from src.schemas.auth import AuthMeResponse
from src.services.auth_service import AuthError, AuthService

router = APIRouter()
_service = AuthService()

_ERROR_STATUS = {
    "unauthorized": 401,
    "not_found": 404,
}


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
