from src.repository.supabase_client import SupabaseClient


class ZonasRepository:
    def get_all(self):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_zonas")
        )
        return result.data
