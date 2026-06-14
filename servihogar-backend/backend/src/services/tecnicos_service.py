from src.repository.supabase_client import SupabaseClient
from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.tecnico import TecnicoResponse


class TecnicosService:
    def __init__(self):
        self._repo = TecnicosRepository()

    def obtener_todos(self) -> list[TecnicoResponse]:
        data = self._repo.get_all()
        result = []
        for item in data:
            usuario = item.pop("usuarios", {})
            result.append(
                TecnicoResponse(
                    id_tecnico=item["id_tecnico"],
                    nombres=usuario.get("nombres", ""),
                    apellidos=usuario.get("apellidos", ""),
                    descripcion=item.get("descripcion"),
                    experiencia_anios=item["experiencia_anios"],
                    calificacion=self._calcular_calificacion(item["id_tecnico"]),
                )
            )
        return result

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
