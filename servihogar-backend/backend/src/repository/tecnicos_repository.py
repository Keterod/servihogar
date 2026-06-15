from src.repository.supabase_client import SupabaseClient

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
            client.table("tecnicos")
            .select(
                "id_tecnico, descripcion, experiencia_anios, "
                "usuarios!inner(id_usuario, nombres, apellidos), "
                "tecnico_categorias(categorias_servicio(id_categoria, nombre)), "
                "tecnico_zonas(zonas(id_zona, nombre))"
            )
            .eq("estado_validacion", "validado")
        )
        return result.data

    def get_by_id(self, id_tecnico: int):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnicos")
            .select(
                "id_tecnico, descripcion, experiencia_anios, "
                "usuarios!inner(id_usuario, nombres, apellidos), "
                "tecnico_categorias(categorias_servicio(id_categoria, nombre)), "
                "tecnico_zonas(zonas(id_zona, nombre))"
            )
            .eq("id_tecnico", id_tecnico)
            .eq("estado_validacion", "validado")
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None

    def get_portafolio(self, id_tecnico: int):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("portafolio_tecnico")
            .select("id_portafolio, titulo, descripcion, imagen_url")
            .eq("id_tecnico", id_tecnico)
            .eq("estado", "visible")
            .order("fecha_subida", desc=True)
        )
        return result.data
