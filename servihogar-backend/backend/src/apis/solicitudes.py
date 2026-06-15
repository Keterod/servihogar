from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.apis.deps import get_current_user, require_cliente
from src.schemas.auth import AuthMeResponse
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
async def crear_solicitud(
    data: SolicitudRequest,
    cliente: Annotated[AuthMeResponse, Depends(require_cliente)],
):
    resultado = _service.crear_solicitud_para_cliente(cliente.id_cliente, data)
    if resultado is None:
        raise HTTPException(
            status_code=503, detail="No se pudo crear la solicitud. Intenta nuevamente."
        )
    return resultado


@router.get("/clientes/me/solicitudes", response_model=list[SolicitudListResponse])
async def listar_mis_solicitudes(
    cliente: Annotated[AuthMeResponse, Depends(require_cliente)],
):
    return _service.obtener_por_cliente_id(cliente.id_cliente)


@router.get("/clientes/demo/solicitudes", response_model=list[SolicitudListResponse])
async def listar_solicitudes_cliente_demo():
    return _service.obtener_por_cliente()


@router.get("/solicitudes/{id_solicitud}", response_model=SolicitudDetalleResponse)
async def obtener_solicitud(
    id_solicitud: int,
    user: Annotated[AuthMeResponse, Depends(get_current_user)],
):
    acceso = _service.verificar_acceso_detalle(id_solicitud, user)
    if acceso == "not_found":
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if acceso == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver esta solicitud",
        )

    resultado = _service.obtener_detalle_por_id(id_solicitud)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return resultado
