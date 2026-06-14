from fastapi import APIRouter

from src.schemas.tecnico import TecnicoResponse
from src.services.tecnicos_service import TecnicosService

router = APIRouter()
_service = TecnicosService()


@router.get("/tecnicos", response_model=list[TecnicoResponse])
async def listar_tecnicos():
    return _service.obtener_todos()
