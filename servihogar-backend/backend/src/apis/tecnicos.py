from fastapi import APIRouter, HTTPException

from src.schemas.tecnico import TecnicoDetalleResponse, TecnicoResponse
from src.services.tecnicos_service import TecnicosService

router = APIRouter()
_service = TecnicosService()


@router.get("/tecnicos", response_model=list[TecnicoResponse])
async def listar_tecnicos():
    return _service.obtener_todos()


@router.get("/tecnicos/{id_tecnico}", response_model=TecnicoDetalleResponse)
async def obtener_tecnico(id_tecnico: int):
    tecnico = _service.obtener_por_id(id_tecnico)
    if tecnico is None:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    return tecnico
