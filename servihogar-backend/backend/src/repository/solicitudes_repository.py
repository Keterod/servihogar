from collections import Counter

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

    def get_by_cliente_id(self, id_cliente: int) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio")
            .select(
                "*, categorias_servicio!inner(nombre), zonas!inner(nombre)"
            )
            .eq("id_cliente", id_cliente)
            .order("fecha_publicacion", desc=True)
        )
        if not result.data:
            return []

        solicitud_ids = [s["id_solicitud"] for s in result.data]
        cotizaciones_result = SupabaseClient.execute(
            client.table("cotizaciones")
            .select("id_solicitud")
            .in_("id_solicitud", solicitud_ids)
        )
        cotizaciones_count = Counter(
            c["id_solicitud"] for c in (cotizaciones_result.data or [])
        )

        for solicitud in result.data:
            sid = solicitud["id_solicitud"]
            solicitud["cotizaciones_count"] = cotizaciones_count.get(sid, 0)
            solicitud["categoria_nombre"] = solicitud.pop("categorias_servicio", {}).get("nombre", "")
            solicitud["zona_nombre"] = solicitud.pop("zonas", {}).get("nombre", "")

        return result.data
