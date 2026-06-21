from src.repository.supabase_client import SupabaseClient


class CategoriasRepository:
    def get_all(self):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_categorias")
        )
        return result.data
