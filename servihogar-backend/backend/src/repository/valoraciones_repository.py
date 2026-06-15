from src.repository.supabase_client import SupabaseClient


class ValoracionesRepository:
    def exists_for_cotizacion(self, id_cotizacion: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("valoraciones")
            .select("id_valoracion")
            .eq("id_cotizacion", id_cotizacion)
            .limit(1)
        )
        return bool(result.data)

    def insert(self, data: dict) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("valoraciones")
            .insert(data)
            .select(
                "id_valoracion, id_cotizacion, puntuacion, comentario, "
                "puntualidad, calidad, precio, trato, fecha_valoracion"
            )
        )
        if not result.data:
            return None
        return result.data[0]
