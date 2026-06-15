from src.repository.catalogo_repository import CatalogoRepository
from src.schemas.catalogo import CategoriaServicioResponse, ZonaResponse


class CatalogoService:
    def __init__(self):
        self._repo = CatalogoRepository()

    def listar_categorias(self) -> list[CategoriaServicioResponse]:
        return [CategoriaServicioResponse.model_validate(row) for row in self._repo.list_categorias()]

    def listar_zonas(self) -> list[ZonaResponse]:
        return [ZonaResponse.model_validate(row) for row in self._repo.list_zonas()]
