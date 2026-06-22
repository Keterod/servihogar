from src.repository.supabase_client import SupabaseClient


class ImagenesSolicitudRepository:
    def insert(
        self,
        id_solicitud: int,
        imagen_url: str,
        descripcion: str | None = None,
    ) -> dict | None:
        client = SupabaseClient.get()
        params: dict = {
            "p_id_solicitud": id_solicitud,
            "p_imagen_url": imagen_url,
        }
        if descripcion is not None:
            params["p_descripcion"] = descripcion

        result = SupabaseClient.execute(
            client.rpc("rpc_insert_imagen_solicitud", params)
        )
        return result.data or None

    def count_by_solicitud(self, id_solicitud: int) -> int:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_count_imagenes_solicitud", {"p_id_solicitud": id_solicitud})
        )
        return result.data if isinstance(result.data, int) else 0

    def list_by_solicitud(self, id_solicitud: int) -> list:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_imagenes_solicitud", {"p_id_solicitud": id_solicitud})
        )
        return result.data or []
