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

    @staticmethod
    def _join_nombre(data) -> str:
        if isinstance(data, list):
            data = data[0] if data else {}
        if not isinstance(data, dict):
            return ""
        return data.get("nombre", "")

    def get_by_id_for_cliente(self, id_solicitud: int, id_cliente: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio")
            .select(
                "*, categorias_servicio!inner(nombre), zonas!inner(nombre)"
            )
            .eq("id_solicitud", id_solicitud)
            .eq("id_cliente", id_cliente)
            .limit(1)
        )
        rows = result.data or []
        if not rows:
            return None
        solicitud = rows[0]
        solicitud["categoria_nombre"] = self._join_nombre(
            solicitud.pop("categorias_servicio", None)
        )
        solicitud["zona_nombre"] = self._join_nombre(solicitud.pop("zonas", None))
        return solicitud

    def get_cotizaciones_by_solicitud(self, id_solicitud: int) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("cotizaciones")
            .select(
                "id_cotizacion, id_tecnico, monto, descripcion, tiempo_estimado, "
                "estado, fecha_envio, "
                "tecnicos!inner(descripcion, usuarios!inner(nombres, apellidos))"
            )
            .eq("id_solicitud", id_solicitud)
            .order("fecha_envio", desc=True)
        )
        if not result.data:
            return []

        cotizaciones = []
        for row in result.data:
            tecnico = row.pop("tecnicos", None)
            if isinstance(tecnico, list):
                tecnico = tecnico[0] if tecnico else {}
            if not isinstance(tecnico, dict):
                tecnico = {}
            usuario = tecnico.get("usuarios") or {}
            if isinstance(usuario, list):
                usuario = usuario[0] if usuario else {}
            nombres = usuario.get("nombres", "")
            apellidos = usuario.get("apellidos", "")
            cotizaciones.append(
                {
                    "id_cotizacion": row["id_cotizacion"],
                    "id_tecnico": row["id_tecnico"],
                    "tecnico_nombre": f"{nombres} {apellidos}".strip(),
                    "tecnico_descripcion": tecnico.get("descripcion"),
                    "precio": float(row["monto"]),
                    "tiempo_estimado": row.get("tiempo_estimado"),
                    "descripcion_propuesta": row["descripcion"],
                    "estado": row["estado"],
                    "fecha_creacion": row["fecha_envio"],
                }
            )
        return cotizaciones
