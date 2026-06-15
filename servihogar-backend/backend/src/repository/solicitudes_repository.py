from src.repository.supabase_client import SupabaseClient


class SolicitudesRepository:
    def get_demo_cliente_id(self) -> int | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("usuarios")
            .select("clientes!inner(id_cliente)")
            .eq("auth_user_id", "eb65fb3b-d00b-40b5-82e8-933cd3cd346c")
            .limit(1)
        )
        if not result.data:
            return None
        clientes = result.data[0].get("clientes")
        if not clientes:
            return None
        if isinstance(clientes, list):
            return clientes[0]["id_cliente"]
        return clientes["id_cliente"]

    def insert(self, data: dict) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio").insert(data)
        )
        if not result.data:
            return None
        return result.data[0]
