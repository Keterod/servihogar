from fastapi import APIRouter

from src.schemas.catalogo import CategoriaServicioResponse
from src.services.catalogo_service import CatalogoService

router = APIRouter()
_service = CatalogoService()


@router.get("/categorias", response_model=list[CategoriaServicioResponse])
async def listar_categorias():
    return _service.listar_categorias()
