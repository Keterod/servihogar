from src.repository.supabase_client import SupabaseClient


class AdminRepository:
    def get_resumen_counts(self) -> dict[str, int]:
        return {
            "total_usuarios": self._count_all("usuarios", "id_usuario"),
            "total_clientes": self._count_all("clientes", "id_cliente"),
            "total_tecnicos": self._count_all("tecnicos", "id_tecnico"),
            "total_solicitudes": self._count_all(
                "solicitudes_servicio", "id_solicitud"
            ),
            "solicitudes_pendientes": self._count_by_field(
                "solicitudes_servicio", "id_solicitud", "estado", "pendiente"
            ),
            "solicitudes_en_proceso": self._count_by_field(
                "solicitudes_servicio", "id_solicitud", "estado", "en_proceso"
            ),
            "solicitudes_finalizadas": self._count_by_field(
                "solicitudes_servicio", "id_solicitud", "estado", "finalizada"
            ),
            "tecnicos_pendientes": self._count_by_field(
                "tecnicos", "id_tecnico", "estado_validacion", "pendiente"
            ),
            "tecnicos_validados": self._count_by_field(
                "tecnicos", "id_tecnico", "estado_validacion", "validado"
            ),
            "tecnicos_rechazados": self._count_by_field(
                "tecnicos", "id_tecnico", "estado_validacion", "rechazado"
            ),
            "total_cotizaciones": self._count_all("cotizaciones", "id_cotizacion"),
            "total_valoraciones": self._count_all("valoraciones", "id_valoracion"),
        }

    def get_tecnicos_pendientes(self) -> list[dict]:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnicos")
            .select(
                "id_tecnico, descripcion, experiencia_anios, estado_validacion, "
                "fecha_solicitud_validacion, "
                "usuarios!inner(nombres, apellidos, telefono, fecha_registro), "
                "tecnico_categorias(categorias_servicio(nombre)), "
                "tecnico_zonas(zonas(nombre))"
            )
            .eq("estado_validacion", "pendiente")
            .order("fecha_solicitud_validacion", desc=True)
        )
        return result.data or []

    def get_tecnico_estado(self, id_tecnico: int) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnicos")
            .select("id_tecnico, estado_validacion")
            .eq("id_tecnico", id_tecnico)
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None

    def update_tecnico_estado(self, id_tecnico: int, estado: str) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnicos")
            .update({"estado_validacion": estado})
            .eq("id_tecnico", id_tecnico)
            .select("id_tecnico, estado_validacion")
        )
        rows = result.data or []
        return rows[0] if rows else None

    @staticmethod
    def _count_all(table: str, id_column: str) -> int:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(client.table(table).select(id_column))
        return len(result.data or [])

    @staticmethod
    def _count_by_field(table: str, id_column: str, field: str, value: str) -> int:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table(table).select(id_column).eq(field, value)
        )
        return len(result.data or [])
