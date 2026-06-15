from fastapi import APIRouter, HTTPException

from src.schemas.valoracion import ValoracionRequest, ValoracionResponse
from src.services.valoraciones_service import ValoracionError, ValoracionesService

router = APIRouter()
_service = ValoracionesService()

_ERROR_STATUS = {
    "not_found": 404,
    "bad_request": 400,
    "conflict": 409,
    "failed": 503,
}


def _handle_error(exc: ValoracionError) -> HTTPException:
    return HTTPException(
        status_code=_ERROR_STATUS.get(exc.code, 503),
        detail=str(exc),
    )


@router.post("/valoraciones", response_model=ValoracionResponse, status_code=201)
async def crear_valoracion(data: ValoracionRequest):
    try:
        return _service.crear_valoracion_demo(data)
    except ValoracionError as exc:
        raise _handle_error(exc) from exc
