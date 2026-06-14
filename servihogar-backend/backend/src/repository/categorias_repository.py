from src.repository.supabase_client import SupabaseClient


class CategoriasRepository:
    def get_all(self):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("categorias_servicio").select("*").eq("estado", "activo")
        )
        return result.data
