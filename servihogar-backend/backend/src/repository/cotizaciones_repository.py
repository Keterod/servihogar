from src.repository.supabase_client import SupabaseClient


class CotizacionesRepository:
    def exists_for_tecnico(self, id_solicitud: int, id_tecnico: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .select("id_cotizacion")
            .eq("id_solicitud", id_solicitud)
            .eq("id_tecnico", id_tecnico)
            .limit(1)
        )
        return bool(result.data)

    def insert(self, data: dict) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.table("cotizaciones").insert(data))
        if not result.data:
            return None
        return result.data[0]
