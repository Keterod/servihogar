import logging

from src.repository.supabase_client import SupabaseClient

logger = logging.getLogger(__name__)

DEMO_TECNICO_AUTH_USER_ID = "9ce2ac73-1b61-40de-ac53-bafc12b3eb29"


class TecnicosRepository:
    def get_demo_tecnico_id(self) -> int | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("usuarios")
            .select("tecnicos!inner(id_tecnico)")
            .eq("auth_user_id", DEMO_TECNICO_AUTH_USER_ID)
            .limit(1)
        )
        if not result.data:
            return None
        tecnicos = result.data[0].get("tecnicos")
        if not tecnicos:
            return None
        if isinstance(tecnicos, list):
            return tecnicos[0]["id_tecnico"]
        return tecnicos["id_tecnico"]

    def get_categorias_for_tecnico(self, id_tecnico: int) -> list[int]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnico_categorias")
            .select("id_categoria")
            .eq("id_tecnico", id_tecnico)
        )
        return [row["id_categoria"] for row in (result.data or [])]

    def get_zonas_for_tecnico(self, id_tecnico: int) -> list[int]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnico_zonas")
            .select("id_zona")
            .eq("id_tecnico", id_tecnico)
        )
        return [row["id_zona"] for row in (result.data or [])]

    def get_all(self):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_tecnicos_publicos")
        )
        return result.data

    def get_by_id(self, id_tecnico: int):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_get_tecnico_publico_by_id", {"p_id_tecnico": id_tecnico})
        )
        return result.data

    def list_portafolio_for_tecnico(self, id_tecnico: int):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_portafolio_tecnico", {"p_id_tecnico": id_tecnico})
        )
        return result.data or []

    def count_portafolio_visible(self, id_tecnico: int) -> int:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_count_portafolio_visible", {"p_id_tecnico": id_tecnico})
        )
        return result.data if isinstance(result.data, int) else 0

    def insert_portafolio(
        self,
        id_tecnico: int,
        titulo: str,
        imagen_url: str,
        descripcion: str | None = None,
    ) -> dict | None:
        client = SupabaseClient.get()
        params: dict = {
            "p_id_tecnico": id_tecnico,
            "p_titulo": titulo,
            "p_imagen_url": imagen_url,
        }
        if descripcion is not None:
            params["p_descripcion"] = descripcion

        logger.info(
            "Insert portafolio_tecnico id_tecnico=%s storage_path=%s params=%s",
            id_tecnico,
            imagen_url,
            params,
        )

        result = SupabaseClient.execute(
            client.rpc("rpc_insert_portafolio_tecnico", params),
            context="insert portafolio_tecnico",
        )
        return result.data or None
