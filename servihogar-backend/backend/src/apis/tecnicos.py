from typing import Annotated

import logging

from fastapi import APIRouter, Depends, HTTPException
from supabase._sync.client import SupabaseException

from src.apis.deps import require_tecnico_validado
from src.schemas.auth import AuthMeResponse
from src.schemas.solicitud import ServicioAceptadoResponse, SolicitudDisponibleResponse
from src.schemas.tecnico import (
    PortafolioCreateRequest,
    PortafolioItemResponse,
    TecnicoDetalleResponse,
    TecnicoResponse,
)
from src.services.solicitudes_service import SolicitudesService
from src.services.tecnicos_service import PortafolioError, TecnicosService

logger = logging.getLogger(__name__)

router = APIRouter()
_service = TecnicosService()
_solicitudes_service = SolicitudesService()

_PORTAFOLIO_ERROR_STATUS = {
    "validation": 422,
    "limit": 409,
    "failed": 503,
}

@router.get("/tecnicos", response_model=list[TecnicoResponse])
async def listar_tecnicos():
    return _service.obtener_todos()


@router.get(
    "/tecnicos/me/solicitudes-disponibles",
    response_model=list[SolicitudDisponibleResponse],
)
async def listar_mis_solicitudes_disponibles(
    tecnico: Annotated[AuthMeResponse, Depends(require_tecnico_validado)],
):
    return _solicitudes_service.obtener_solicitudes_disponibles_para_tecnico(
        tecnico.id_tecnico
    )


@router.get(
    "/tecnicos/me/servicios-aceptados",
    response_model=list[ServicioAceptadoResponse],
)
async def listar_mis_servicios_aceptados(
    tecnico: Annotated[AuthMeResponse, Depends(require_tecnico_validado)],
):
    return _solicitudes_service.obtener_servicios_aceptados_para_tecnico(tecnico.id_tecnico)


@router.get(
    "/tecnicos/me/portafolio",
    response_model=list[PortafolioItemResponse],
)
async def listar_mi_portafolio(
    tecnico: Annotated[AuthMeResponse, Depends(require_tecnico_validado)],
):
    return _service.listar_mi_portafolio(tecnico.id_tecnico)


@router.post(
    "/tecnicos/me/portafolio",
    response_model=PortafolioItemResponse,
    status_code=201,
)
async def agregar_portafolio(
    data: PortafolioCreateRequest,
    tecnico: Annotated[AuthMeResponse, Depends(require_tecnico_validado)],
):
    logger.info(
        "POST /tecnicos/me/portafolio id_tecnico=%s payload=%s storage_path=%s",
        tecnico.id_tecnico,
        data.model_dump(exclude_none=True),
        data.imagen_url,
    )
    try:
        return _service.agregar_portafolio(tecnico.id_tecnico, data)
    except PortafolioError as exc:
        raise HTTPException(
            status_code=_PORTAFOLIO_ERROR_STATUS.get(exc.code, 400),
            detail=str(exc),
        ) from exc
    except SupabaseException as exc:
        logger.exception(
            "Error de Supabase al agregar portafolio id_tecnico=%s storage_path=%s",
            tecnico.id_tecnico,
            data.imagen_url,
        )
        detail = str(exc)
        status_code = 422 if "query failed" in detail.lower() else 503
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except Exception:
        logger.exception(
            "Error inesperado al agregar portafolio id_tecnico=%s storage_path=%s",
            tecnico.id_tecnico,
            data.imagen_url,
        )
        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar el ítem de portafolio",
        ) from None


@router.get(
    "/tecnicos/demo/solicitudes-disponibles",
    response_model=list[SolicitudDisponibleResponse],
)
async def listar_solicitudes_disponibles_demo():
    return _solicitudes_service.obtener_solicitudes_disponibles_demo()


@router.get(
    "/tecnicos/demo/servicios-aceptados",
    response_model=list[ServicioAceptadoResponse],
)
async def listar_servicios_aceptados_demo():
    return _solicitudes_service.obtener_servicios_aceptados_demo()


@router.get("/tecnicos/{id_tecnico}", response_model=TecnicoDetalleResponse)
async def obtener_tecnico(id_tecnico: int):
    tecnico = _service.obtener_por_id(id_tecnico)
    if tecnico is None:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    return tecnico
