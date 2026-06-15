from src.repository.supabase_client import SupabaseClient
from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.tecnico import (
    PortafolioItem,
    TecnicoCategoriaRef,
    TecnicoDetalleResponse,
    TecnicoResponse,
    TecnicoZonaRef,
)


class TecnicosService:
    def __init__(self):
        self._repo = TecnicosRepository()

    def obtener_todos(self) -> list[TecnicoResponse]:
        data = self._repo.get_all()
        result = []
        for item in data:
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
                    calificacion=self._calcular_calificacion(item["id_tecnico"]),
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
        portafolio = self._map_portafolio(self._repo.get_portafolio(id_tecnico))
        return TecnicoDetalleResponse(
            id_tecnico=item["id_tecnico"],
            nombres=usuario.get("nombres", ""),
            apellidos=usuario.get("apellidos", ""),
            descripcion=item.get("descripcion"),
            experiencia_anios=item["experiencia_anios"],
            calificacion=self._calcular_calificacion(item["id_tecnico"]),
            categorias=categorias,
            zonas=zonas,
            portafolio=portafolio,
        )

    @staticmethod
    def _map_portafolio(rows: list) -> list[PortafolioItem]:
        portafolio = []
        for row in rows or []:
            portafolio.append(
                PortafolioItem(
                    id_portafolio=row["id_portafolio"],
                    titulo=row["titulo"],
                    descripcion=row.get("descripcion"),
                    imagen_url=row["imagen_url"],
                )
            )
        return portafolio

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

    @staticmethod
    def _calcular_calificacion(id_tecnico: int) -> float | None:
        client = SupabaseClient.get()
        cotizaciones = SupabaseClient.execute(
            client.table("cotizaciones")
            .select("id_cotizacion")
            .eq("id_tecnico", id_tecnico)
        )
        if not cotizaciones.data:
            return None
        cot_ids = [c["id_cotizacion"] for c in cotizaciones.data]
        valoraciones = SupabaseClient.execute(
            client.table("valoraciones")
            .select("puntuacion")
            .in_("id_cotizacion", cot_ids)
        )
        if not valoraciones.data:
            return None
        scores = [v["puntuacion"] for v in valoraciones.data]
        return round(sum(scores) / len(scores), 1)
