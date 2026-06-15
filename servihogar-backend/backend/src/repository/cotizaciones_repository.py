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

    def get_by_id(self, id_cotizacion: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .select(
                "id_cotizacion, id_solicitud, id_tecnico, monto, descripcion, "
                "tiempo_estimado, estado, fecha_envio"
            )
            .eq("id_cotizacion", id_cotizacion)
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None

    def update_estado(self, id_cotizacion: int, estado: str) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .update({"estado": estado})
            .eq("id_cotizacion", id_cotizacion)
            .select(
                "id_cotizacion, id_solicitud, id_tecnico, monto, descripcion, "
                "tiempo_estimado, estado, fecha_envio"
            )
        )
        if not result.data:
            return None
        return result.data[0]

    def reject_pending_others(self, id_solicitud: int, except_id_cotizacion: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .update({"estado": "rechazada"})
            .eq("id_solicitud", id_solicitud)
            .eq("estado", "pendiente")
            .neq("id_cotizacion", except_id_cotizacion)
        )
        return result.data is not None

    def has_accepted_for_solicitud(self, id_solicitud: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .select("id_cotizacion")
            .eq("id_solicitud", id_solicitud)
            .eq("estado", "aceptada")
            .limit(1)
        )
        return bool(result.data)

    def get_accepted_for_solicitud(self, id_solicitud: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .select("id_cotizacion, id_solicitud, id_tecnico, estado")
            .eq("id_solicitud", id_solicitud)
            .eq("estado", "aceptada")
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None
