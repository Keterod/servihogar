from fastapi import APIRouter, HTTPException

from src.schemas.solicitud import ServicioAceptadoResponse, SolicitudDisponibleResponse
from src.schemas.tecnico import TecnicoDetalleResponse, TecnicoResponse
from src.services.solicitudes_service import SolicitudesService
from src.services.tecnicos_service import TecnicosService

router = APIRouter()
_service = TecnicosService()
_solicitudes_service = SolicitudesService()


@router.get("/tecnicos", response_model=list[TecnicoResponse])
async def listar_tecnicos():
    return _service.obtener_todos()


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
