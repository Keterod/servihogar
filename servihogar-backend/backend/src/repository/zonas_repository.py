from src.repository.supabase_client import SupabaseClient


class ZonasRepository:
    def get_all(self):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("zonas").select("*").eq("estado", "activo")
        )
        return result.data
