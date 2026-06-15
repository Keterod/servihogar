from src.repository.supabase_client import SupabaseClient


class TecnicosRepository:
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
