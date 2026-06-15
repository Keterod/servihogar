from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.apis.deps import require_cliente, require_tecnico_validado
from src.schemas.auth import AuthMeResponse
from src.schemas.cotizacion import CotizacionActionResponse, CotizacionRequest, CotizacionResponse
from src.services.cotizaciones_service import CotizacionError, CotizacionesService

router = APIRouter()
_service = CotizacionesService()
_ERROR_STATUS = {
    "not_found": 404,
    "bad_request": 400,
    "duplicate": 409,
    "conflict": 409,
    "forbidden": 403,
    "failed": 503,
}


def _handle_error(exc: CotizacionError) -> HTTPException:
    return HTTPException(
        status_code=_ERROR_STATUS.get(exc.code, 503),
        detail=str(exc),
    )


@router.post("/cotizaciones", response_model=CotizacionResponse, status_code=201)
async def crear_cotizacion(
    data: CotizacionRequest,
    tecnico: Annotated[AuthMeResponse, Depends(require_tecnico_validado)],
):
    try:
        return _service.crear_cotizacion_para_tecnico(tecnico.id_tecnico, data)
    except CotizacionError as exc:
        raise _handle_error(exc) from exc


@router.patch(
    "/cotizaciones/{id_cotizacion}/aceptar",
    response_model=CotizacionActionResponse,
)
async def aceptar_cotizacion(
    id_cotizacion: int,
    cliente: Annotated[AuthMeResponse, Depends(require_cliente)],
):
    try:
        return _service.aceptar_cotizacion_para_cliente(
            id_cotizacion, cliente.id_cliente
        )
    except CotizacionError as exc:
        raise _handle_error(exc) from exc


@router.patch(
    "/cotizaciones/{id_cotizacion}/rechazar",
    response_model=CotizacionActionResponse,
)
async def rechazar_cotizacion(
    id_cotizacion: int,
    cliente: Annotated[AuthMeResponse, Depends(require_cliente)],
):
    try:
        return _service.rechazar_cotizacion_para_cliente(
            id_cotizacion, cliente.id_cliente
        )
    except CotizacionError as exc:
        raise _handle_error(exc) from exc
