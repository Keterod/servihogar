from src.repository.categorias_repository import CategoriasRepository


class CategoriasService:
    def __init__(self):
        self._repo = CategoriasRepository()

    def obtener_todas(self):
        return self._repo.get_all()
