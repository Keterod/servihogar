from src.repository.supabase_client import SupabaseClient


class CatalogoRepository:
    def list_categorias(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_categorias")
        )
        return result.data or []

    def list_zonas(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_zonas")
        )
        return result.data or []
