from fastapi import APIRouter, HTTPException

from src.schemas.cotizacion import CotizacionActionResponse, CotizacionRequest, CotizacionResponse
from src.services.cotizaciones_service import CotizacionError, CotizacionesService

router = APIRouter()
_service = CotizacionesService()

_ERROR_STATUS = {
    "not_found": 404,
    "bad_request": 400,
    "duplicate": 409,
    "conflict": 409,
    "failed": 503,
}


def _handle_error(exc: CotizacionError) -> HTTPException:
    return HTTPException(
        status_code=_ERROR_STATUS.get(exc.code, 503),
        detail=str(exc),
    )


@router.post("/cotizaciones", response_model=CotizacionResponse, status_code=201)
async def crear_cotizacion(data: CotizacionRequest):
    try:
        return _service.crear_cotizacion_demo(data)
    except CotizacionError as exc:
        raise _handle_error(exc) from exc


@router.patch(
    "/cotizaciones/{id_cotizacion}/aceptar",
    response_model=CotizacionActionResponse,
)
async def aceptar_cotizacion(id_cotizacion: int):
    try:
        return _service.aceptar_cotizacion_demo(id_cotizacion)
    except CotizacionError as exc:
        raise _handle_error(exc) from exc


@router.patch(
    "/cotizaciones/{id_cotizacion}/rechazar",
    response_model=CotizacionActionResponse,
)
async def rechazar_cotizacion(id_cotizacion: int):
    try:
        return _service.rechazar_cotizacion_demo(id_cotizacion)
    except CotizacionError as exc:
        raise _handle_error(exc) from exc
