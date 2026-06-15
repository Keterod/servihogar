from src.repository.supabase_client import SupabaseClient


class CatalogoRepository:
    def list_categorias(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("categorias_servicio")
            .select("id_categoria, nombre, descripcion")
            .eq("estado", "activo")
            .order("nombre")
        )
        return result.data or []

    def list_zonas(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("zonas")
            .select("id_zona, nombre, id_ciudad")
            .eq("estado", "activo")
            .order("nombre")
        )
        return result.data or []
