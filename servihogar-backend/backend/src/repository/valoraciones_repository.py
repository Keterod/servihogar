from src.repository.supabase_client import SupabaseClient


class ValoracionesRepository:
    def exists_for_cotizacion(self, id_cotizacion: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_exists_valoracion_cotizacion", {
                "p_id_cotizacion": id_cotizacion,
            })
        )
        return bool(result.data)

    def insert(self, data: dict) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_insert_valoracion", {
                "p_id_cotizacion": data["id_cotizacion"],
                "p_puntuacion": data["puntuacion"],
                "p_comentario": data.get("comentario"),
                "p_puntualidad": data.get("puntualidad"),
                "p_calidad": data.get("calidad"),
                "p_precio": data.get("precio"),
                "p_trato": data.get("trato"),
            })
        )
        return result.data or None
