from fastapi import APIRouter, HTTPException

from src.schemas.cotizacion import CotizacionRequest, CotizacionResponse
from src.services.cotizaciones_service import CotizacionError, CotizacionesService

router = APIRouter()
_service = CotizacionesService()

_ERROR_STATUS = {
    "not_found": 404,
    "bad_request": 400,
    "duplicate": 409,
    "failed": 503,
}


@router.post("/cotizaciones", response_model=CotizacionResponse, status_code=201)
async def crear_cotizacion(data: CotizacionRequest):
    try:
        return _service.crear_cotizacion_demo(data)
    except CotizacionError as exc:
        raise HTTPException(
            status_code=_ERROR_STATUS.get(exc.code, 503),
            detail=str(exc),
        ) from exc
