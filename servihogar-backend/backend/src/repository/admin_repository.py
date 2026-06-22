from src.repository.supabase_client import SupabaseClient


class AdminRepository:
    def get_resumen_counts(self) -> dict[str, int]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.rpc("rpc_admin_resumen"))
        return result.data or {}

    def get_tecnicos_pendientes(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.rpc("rpc_admin_tecnicos_pendientes"))
        return result.data or []

    def get_tecnico_estado(self, id_tecnico: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_admin_get_tecnico_estado", {"p_id_tecnico": id_tecnico})
        )
        return result.data

    def update_tecnico_estado(self, id_tecnico: int, estado: str) -> dict:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_admin_actualizar_estado_tecnico", {
                "p_id_tecnico": id_tecnico,
                "p_estado_validacion": estado,
            })
        )
        return result.data

    def get_reporte_usuarios(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.rpc("rpc_admin_reporte_usuarios"))
        return result.data or []

    def get_reporte_solicitudes(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.rpc("rpc_admin_reporte_solicitudes"))
        return result.data or []

    def get_reporte_cotizaciones(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.rpc("rpc_admin_reporte_cotizaciones"))
        return result.data or []

    def get_reporte_servicios_finalizados(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_admin_reporte_servicios_finalizados")
        )
        return result.data or []

    def get_reporte_tecnicos_activos(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_admin_reporte_tecnicos_activos")
        )
        return result.data or []
