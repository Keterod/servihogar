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

    def get_solicitud_by_id(self, id_solicitud: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio")
            .select("id_solicitud, id_cliente, estado, id_categoria, id_zona")
            .eq("id_solicitud", id_solicitud)
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None

    def update_estado(self, id_solicitud: int, estado: str) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio")
            .update({"estado": estado})
            .eq("id_solicitud", id_solicitud)
            .select("id_solicitud, estado")
        )
        if not result.data:
            return None
        return result.data[0]

    def get_solicitud_for_cotizacion(
        self, id_solicitud: int, categorias: list[int], zonas: list[int]
    ) -> dict | None:
        """Return a pending solicitud eligible for the technician (same filters as disponibles)."""
        if not categorias or not zonas:
            return None

        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio")
            .select("id_solicitud, estado, id_categoria, id_zona")
            .eq("id_solicitud", id_solicitud)
            .eq("estado", "pendiente")
            .in_("id_categoria", categorias)
            .in_("id_zona", zonas)
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None

    def get_by_cliente_id(self, id_cliente: int) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_listar_solicitudes_cliente", {"p_id_cliente": id_cliente})
        )
        return result.data or []

    @staticmethod
    def _join_nombre(data) -> str:
        if isinstance(data, list):
            data = data[0] if data else {}
        if not isinstance(data, dict):
            return ""
        return data.get("nombre") or ""

    @staticmethod
    def _unwrap_embedded(value):
        if isinstance(value, list):
            return value[0] if value else None
        return value

    @staticmethod
    def _safe_float(value) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def get_by_id(self, id_solicitud: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("solicitudes_servicio")
            .select(
                "*, categorias_servicio!inner(nombre), zonas!inner(nombre)"
            )
            .eq("id_solicitud", id_solicitud)
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

    def get_by_id_for_cliente(self, id_solicitud: int, id_cliente: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_get_solicitud_cliente_by_id", {
                "p_id_solicitud": id_solicitud,
                "p_id_cliente": id_cliente,
            })
        )
        return result.data or None

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

    @staticmethod
    def _cliente_nombre_from_row(row: dict) -> str | None:
        clientes = row.pop("clientes", None)
        if isinstance(clientes, list):
            clientes = clientes[0] if clientes else {}
        if not isinstance(clientes, dict):
            return None
        usuario = clientes.get("usuarios") or {}
        if isinstance(usuario, list):
            usuario = usuario[0] if usuario else {}
        if not isinstance(usuario, dict):
            return None
        nombre = f"{usuario.get('nombres', '')} {usuario.get('apellidos', '')}".strip()
        return nombre or None

    def get_disponibles_for_tecnico(self, id_tecnico: int) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_solicitudes_disponibles_tecnico", {
                "p_id_tecnico": id_tecnico,
            })
        )
        return result.data or []

    def get_servicios_aceptados_for_tecnico(self, id_tecnico: int) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.rpc("rpc_servicios_aceptados_tecnico", {
                "p_id_tecnico": id_tecnico,
            })
        )
        return result.data or []
