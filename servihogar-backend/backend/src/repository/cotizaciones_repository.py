from src.repository.supabase_client import SupabaseClient


class CotizacionesRepository:
    def exists_for_tecnico(self, id_solicitud: int, id_tecnico: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_exists_cotizacion_tecnico", {
                "p_id_solicitud": id_solicitud,
                "p_id_tecnico": id_tecnico,
            })
        )
        return bool(result.data)

    def insert(self, data: dict) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_insert_cotizacion", {
                "p_id_solicitud": data["id_solicitud"],
                "p_id_tecnico": data["id_tecnico"],
                "p_monto": data["monto"],
                "p_descripcion": data["descripcion"],
                "p_tiempo_estimado": data.get("tiempo_estimado"),
            })
        )
        return result.data or None

    def get_by_id(self, id_cotizacion: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_get_cotizacion_by_id", {
                "p_id_cotizacion": id_cotizacion,
            })
        )
        return result.data or None

    def aceptar_cotizacion_cliente(
        self, id_cotizacion: int, id_cliente: int
    ) -> dict:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_aceptar_cotizacion_cliente", {
                "p_id_cotizacion": id_cotizacion,
                "p_id_cliente": id_cliente,
            })
        )
        return result.data or {}

    def rechazar_cotizacion_cliente(
        self, id_cotizacion: int, id_cliente: int
    ) -> dict:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_rechazar_cotizacion_cliente", {
                "p_id_cotizacion": id_cotizacion,
                "p_id_cliente": id_cliente,
            })
        )
        return result.data or {}

    def has_accepted_for_solicitud(self, id_solicitud: int) -> bool:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_has_cotizacion_aceptada_solicitud", {
                "p_id_solicitud": id_solicitud,
            })
        )
        return bool(result.data)

    def get_accepted_for_solicitud(self, id_solicitud: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_get_cotizacion_aceptada_solicitud", {
                "p_id_solicitud": id_solicitud,
            })
        )
        return result.data or None
