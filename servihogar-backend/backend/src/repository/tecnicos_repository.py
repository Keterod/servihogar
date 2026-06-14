from src.repository.supabase_client import SupabaseClient


class TecnicosRepository:
    def get_all(self):
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnicos")
            .select(
                "id_tecnico, descripcion, experiencia_anios, "
                "usuarios!inner(id_usuario, nombres, apellidos)"
            )
            .eq("estado_validacion", "validado")
        )
        return result.data
