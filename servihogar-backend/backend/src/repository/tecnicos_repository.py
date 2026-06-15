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
