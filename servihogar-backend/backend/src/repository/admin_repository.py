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
