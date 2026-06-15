from fastapi import APIRouter

from src.schemas.catalogo import ZonaResponse
from src.services.catalogo_service import CatalogoService

router = APIRouter()
_service = CatalogoService()


@router.get("/zonas", response_model=list[ZonaResponse])
async def listar_zonas():
    return _service.listar_zonas()
