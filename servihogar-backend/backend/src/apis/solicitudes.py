from fastapi import APIRouter, HTTPException

from src.schemas.solicitud import (
    SolicitudDetalleResponse,
    SolicitudListResponse,
    SolicitudRequest,
    SolicitudResponse,
)
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


@router.get("/clientes/demo/solicitudes", response_model=list[SolicitudListResponse])
async def listar_solicitudes_cliente():
    return _service.obtener_por_cliente()


@router.get("/solicitudes/{id_solicitud}", response_model=SolicitudDetalleResponse)
async def obtener_solicitud(id_solicitud: int):
    resultado = _service.obtener_detalle(id_solicitud)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return resultado
