from src.repository.zonas_repository import ZonasRepository


class ZonasService:
    def __init__(self):
        self._repo = ZonasRepository()

    def obtener_todas(self):
        return self._repo.get_all()
