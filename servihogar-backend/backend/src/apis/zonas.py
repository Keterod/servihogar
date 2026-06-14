from fastapi import APIRouter

from src.schemas.zona import ZonaResponse
from src.services.zonas_service import ZonasService

router = APIRouter()
_service = ZonasService()


@router.get("/zonas", response_model=list[ZonaResponse])
async def listar_zonas():
    return _service.obtener_todas()
