from typing import Annotated

from fastapi import Depends, Header, HTTPException

from src.schemas.auth import AuthMeResponse, TipoUsuario
from src.services.auth_service import AuthError, AuthService

_auth_service = AuthService()

_AUTH_ERROR_STATUS = {
    "unauthorized": 401,
    "not_found": 404,
    "conflict": 409,
    "validation": 422,
    "unavailable": 503,
}


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> AuthMeResponse:
    try:
        return _auth_service.obtener_usuario_actual(authorization)
    except AuthError as exc:
        raise HTTPException(
            status_code=_AUTH_ERROR_STATUS.get(exc.code, 401),
            detail=str(exc),
        ) from exc


def require_cliente(
    user: Annotated[AuthMeResponse, Depends(get_current_user)],
) -> AuthMeResponse:
    if user.tipo_usuario != TipoUsuario.cliente or user.id_cliente is None:
        raise HTTPException(
            status_code=403,
            detail="Solo los clientes pueden acceder a este recurso",
        )
    return user


def require_tecnico_validado(
    user: Annotated[AuthMeResponse, Depends(get_current_user)],
) -> AuthMeResponse:
    if user.tipo_usuario != TipoUsuario.tecnico or user.id_tecnico is None:
        raise HTTPException(
            status_code=403,
            detail="Solo los técnicos pueden acceder a este recurso",
        )
    if user.estado_validacion != "validado":
        raise HTTPException(
            status_code=403,
            detail="Tu cuenta de técnico está pendiente de validación",
        )
    return user


def require_administrador(
    user: Annotated[AuthMeResponse, Depends(get_current_user)],
) -> AuthMeResponse:
    if user.tipo_usuario != TipoUsuario.administrador or user.id_administrador is None:
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden acceder a este recurso",
        )
    return user
