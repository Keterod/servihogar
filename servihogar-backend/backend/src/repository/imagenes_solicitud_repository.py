from src.repository.supabase_client import SupabaseClient


class ImagenesSolicitudRepository:
    def insert(
        self,
        id_solicitud: int,
        imagen_url: str,
        descripcion: str | None = None,
    ) -> dict | None:
        client = SupabaseClient.get()
        payload: dict = {
            "id_solicitud": id_solicitud,
            "imagen_url": imagen_url,
        }
        if descripcion is not None:
            payload["descripcion"] = descripcion

        result = SupabaseClient.execute(
            client.table("imagenes_solicitud").insert(payload).select("*")
        )
        rows = result.data or []
        return rows[0] if rows else None

    def count_by_solicitud(self, id_solicitud: int) -> int:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("imagenes_solicitud")
            .select("id_imagen", count="exact")
            .eq("id_solicitud", id_solicitud)
        )
        return result.count or 0

    def list_by_solicitud(self, id_solicitud: int) -> list:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("imagenes_solicitud")
            .select("id_imagen, imagen_url, descripcion, fecha_subida")
            .eq("id_solicitud", id_solicitud)
            .order("fecha_subida")
        )
        return result.data or []
