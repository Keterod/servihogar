from fastapi import APIRouter, HTTPException

from src.schemas.solicitud import SolicitudRequest, SolicitudResponse
from src.services.solicitudes_service import SolicitudesService

router = APIRouter()
_service = SolicitudesService()


@router.post("/solicitudes", response_model=SolicitudResponse, status_code=201)
async def crear_solicitud(data: SolicitudRequest):
    resultado = _service.crear_solicitud(data)
    if resultado is None:
        raise HTTPException(
            status_code=503, detail="No se pudo crear la solicitud. Intenta nuevamente."
        )
    return resultado
