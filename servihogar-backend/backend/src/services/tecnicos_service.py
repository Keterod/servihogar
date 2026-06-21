import logging

from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.tecnico import (
    PortafolioCreateRequest,
    PortafolioItem,
    PortafolioItemResponse,
    TecnicoCategoriaRef,
    TecnicoDetalleResponse,
    TecnicoResponse,
    TecnicoZonaRef,
)

MAX_PORTAFOLIO_ITEMS = 20
ALLOWED_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")

logger = logging.getLogger(__name__)


class PortafolioError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class TecnicosService:
    def __init__(self):
        self._repo = TecnicosRepository()

    def obtener_todos(self) -> list[TecnicoResponse]:
        data = self._repo.get_all()
        result = []
        for item in (data or []):
            usuario = item.pop("usuarios", {})
            categorias = self._map_categorias(item.pop("tecnico_categorias", []) or [])
            zonas = self._map_zonas(item.pop("tecnico_zonas", []) or [])
            result.append(
                TecnicoResponse(
                    id_tecnico=item["id_tecnico"],
                    nombres=usuario.get("nombres", ""),
                    apellidos=usuario.get("apellidos", ""),
                    descripcion=item.get("descripcion"),
                    experiencia_anios=item["experiencia_anios"],
                    calificacion=item.get("calificacion"),
                    categorias=categorias,
                    zonas=zonas,
                )
            )
        return result

    def obtener_por_id(self, id_tecnico: int) -> TecnicoDetalleResponse | None:
        item = self._repo.get_by_id(id_tecnico)
        if item is None:
            return None
        usuario = item.pop("usuarios", {})
        categorias = self._map_categorias(item.pop("tecnico_categorias", []) or [])
        zonas = self._map_zonas(item.pop("tecnico_zonas", []) or [])
        portafolio = self._map_portafolio(item.pop("portafolio", []) or [])
        return TecnicoDetalleResponse(
            id_tecnico=item["id_tecnico"],
            nombres=usuario.get("nombres", ""),
            apellidos=usuario.get("apellidos", ""),
            descripcion=item.get("descripcion"),
            experiencia_anios=item["experiencia_anios"],
            calificacion=item.get("calificacion"),
            categorias=categorias,
            zonas=zonas,
            portafolio=portafolio,
        )

    @staticmethod
    def _map_portafolio(rows: list) -> list[PortafolioItem]:
        return [TecnicosService._to_portafolio_item(row) for row in (rows or [])]

    @staticmethod
    def _validar_imagen_url(imagen_url: str, prefix: str) -> None:
        if ".." in imagen_url or imagen_url.startswith("/"):
            raise PortafolioError("validation", "Ruta de imagen inválida")
        if not imagen_url.startswith(prefix):
            raise PortafolioError(
                "validation",
                f"La imagen debe estar bajo el prefijo {prefix}",
            )
        lower = imagen_url.lower()
        if not any(lower.endswith(ext) for ext in ALLOWED_IMAGE_SUFFIXES):
            raise PortafolioError(
                "validation",
                "Solo se permiten imágenes JPEG, PNG o WebP",
            )

    @staticmethod
    def _resolve_storage_path(imagen_url: str) -> str | None:
        if imagen_url.startswith("http://") or imagen_url.startswith("https://"):
            return None
        return imagen_url

    @staticmethod
    def _to_portafolio_item_response(row: dict) -> PortafolioItemResponse:
        imagen_url = row["imagen_url"]
        return PortafolioItemResponse(
            id_portafolio=row["id_portafolio"],
            titulo=row["titulo"],
            descripcion=row.get("descripcion"),
            imagen_url=imagen_url,
            storage_path=TecnicosService._resolve_storage_path(imagen_url),
            estado=row["estado"],
            fecha_subida=row["fecha_subida"],
        )

    @staticmethod
    def _to_portafolio_item(row: dict) -> PortafolioItem:
        imagen_url = row["imagen_url"]
        return PortafolioItem(
            id_portafolio=row["id_portafolio"],
            titulo=row["titulo"],
            descripcion=row.get("descripcion"),
            imagen_url=imagen_url,
            storage_path=TecnicosService._resolve_storage_path(imagen_url),
        )

    def listar_mi_portafolio(self, id_tecnico: int) -> list[PortafolioItemResponse]:
        rows = self._repo.list_portafolio_for_tecnico(id_tecnico)
        return [self._to_portafolio_item_response(r) for r in rows]

    def agregar_portafolio(
        self, id_tecnico: int, data: PortafolioCreateRequest
    ) -> PortafolioItemResponse:
        logger.info(
            "Agregar portafolio id_tecnico=%s titulo=%s storage_path=%s",
            id_tecnico,
            data.titulo,
            data.imagen_url,
        )
        prefix = f"tecnicos/{id_tecnico}/portafolio/"
        self._validar_imagen_url(data.imagen_url, prefix)

        count = self._repo.count_portafolio_visible(id_tecnico)
        if count >= MAX_PORTAFOLIO_ITEMS:
            raise PortafolioError(
                "limit",
                f"Máximo {MAX_PORTAFOLIO_ITEMS} ítems visibles en el portafolio",
            )

        inserted = self._repo.insert_portafolio(
            id_tecnico, data.titulo, data.imagen_url, data.descripcion
        )
        if inserted is None:
            raise PortafolioError("failed", "No se pudo registrar el ítem de portafolio")

        return self._to_portafolio_item_response(inserted)

    @staticmethod
    def _map_categorias(rows: list) -> list[TecnicoCategoriaRef]:
        categorias = []
        for row in rows:
            categoria = row.get("categorias_servicio") or {}
            if categoria:
                categorias.append(
                    TecnicoCategoriaRef(
                        id_categoria=categoria["id_categoria"],
                        nombre=categoria["nombre"],
                    )
                )
        return categorias

    @staticmethod
    def _map_zonas(rows: list) -> list[TecnicoZonaRef]:
        zonas = []
        for row in rows:
            zona = row.get("zonas") or {}
            if zona:
                zonas.append(
                    TecnicoZonaRef(
                        id_zona=zona["id_zona"],
                        nombre=zona["nombre"],
                    )
                )
        return zonas
