from typing import Annotated

import logging

from fastapi import APIRouter, Depends, HTTPException
from supabase._sync.client import SupabaseException

from src.apis.deps import get_current_user, require_cliente
from src.schemas.auth import AuthMeResponse
from src.schemas.solicitud import (
    ImagenSolicitudRequest,
    ImagenSolicitudResponse,
    SolicitudDetalleResponse,
    SolicitudListResponse,
    SolicitudRequest,
    SolicitudResponse,
)
from src.services.solicitudes_service import ImagenError, SolicitudesService

logger = logging.getLogger(__name__)

router = APIRouter()
_service = SolicitudesService()

_IMAGEN_ERROR_STATUS = {
    "not_found": 404,
    "forbidden": 403,
    "validation": 422,
    "limit": 409,
    "failed": 503,
}


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


@router.post(
    "/solicitudes/{id_solicitud}/imagenes",
    response_model=ImagenSolicitudResponse,
    status_code=201,
)
async def registrar_imagen_solicitud(
    id_solicitud: int,
    data: ImagenSolicitudRequest,
    cliente: Annotated[AuthMeResponse, Depends(require_cliente)],
):
    try:
        return _service.registrar_imagen(id_solicitud, cliente.id_cliente, data)
    except ImagenError as exc:
        raise HTTPException(
            status_code=_IMAGEN_ERROR_STATUS.get(exc.code, 400),
            detail=str(exc),
        ) from exc
    except SupabaseException as exc:
        logger.exception(
            "Error de Supabase al registrar imagen para solicitud %s", id_solicitud
        )
        detail = str(exc)
        status_code = 422 if "query failed" in detail.lower() else 503
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except Exception as exc:
        logger.exception(
            "Error inesperado al registrar imagen para solicitud %s", id_solicitud
        )
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la imagen",
        ) from exc


@router.get(
    "/solicitudes/{id_solicitud}/imagenes",
    response_model=list[ImagenSolicitudResponse],
)
async def listar_imagenes_solicitud(
    id_solicitud: int,
    user: Annotated[AuthMeResponse, Depends(get_current_user)],
):
    acceso = _service.verificar_acceso_detalle(id_solicitud, user)
    if acceso == "not_found":
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if acceso == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver las imágenes de esta solicitud",
        )
    return _service.listar_imagenes(id_solicitud)
