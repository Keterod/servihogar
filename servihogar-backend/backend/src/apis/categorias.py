from fastapi import APIRouter

from src.schemas.categoria import CategoriaResponse
from src.services.categorias_service import CategoriasService

router = APIRouter()
_service = CategoriasService()


@router.get("/categorias", response_model=list[CategoriaResponse])
async def listar_categorias():
    return _service.obtener_todas()
