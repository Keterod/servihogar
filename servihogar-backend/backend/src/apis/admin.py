from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.apis.deps import require_administrador
from src.schemas.admin import (
    AdminResumenResponse,
    TecnicoPendienteAdminResponse,
    TecnicoValidacionResponse,
)
from src.schemas.auth import AuthMeResponse
from src.services.admin_service import AdminError, AdminService

router = APIRouter()
_service = AdminService()

_ERROR_STATUS = {
    "not_found": 404,
    "bad_request": 400,
    "conflict": 409,
    "failed": 503,
}


def _handle_error(exc: AdminError) -> HTTPException:
    return HTTPException(
        status_code=_ERROR_STATUS.get(exc.code, 503),
        detail=str(exc),
    )


@router.get("/admin/demo/resumen", response_model=AdminResumenResponse)
async def obtener_resumen_admin_demo(
    _admin: Annotated[AuthMeResponse, Depends(require_administrador)],
):
    return _service.obtener_resumen_demo()


@router.get(
    "/admin/demo/tecnicos-pendientes",
    response_model=list[TecnicoPendienteAdminResponse],
)
async def listar_tecnicos_pendientes_admin_demo(
    _admin: Annotated[AuthMeResponse, Depends(require_administrador)],
):
    return _service.obtener_tecnicos_pendientes_demo()


@router.patch(
    "/admin/demo/tecnicos/{id_tecnico}/aprobar",
    response_model=TecnicoValidacionResponse,
)
async def aprobar_tecnico_admin_demo(
    id_tecnico: int,
    _admin: Annotated[AuthMeResponse, Depends(require_administrador)],
):
    try:
        return _service.aprobar_tecnico_demo(id_tecnico)
    except AdminError as exc:
        raise _handle_error(exc) from exc


@router.patch(
    "/admin/demo/tecnicos/{id_tecnico}/rechazar",
    response_model=TecnicoValidacionResponse,
)
async def rechazar_tecnico_admin_demo(
    id_tecnico: int,
    _admin: Annotated[AuthMeResponse, Depends(require_administrador)],
):
    try:
        return _service.rechazar_tecnico_demo(id_tecnico)
    except AdminError as exc:
        raise _handle_error(exc) from exc
