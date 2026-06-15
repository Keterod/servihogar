from uuid import UUID

from src.repository.supabase_client import SupabaseClient


class AuthRepository:
    def get_auth_user(self, access_token: str) -> dict | None:
        client = SupabaseClient.get()
        try:
            response = client.auth.get_user(access_token)
        except Exception:
            return None

        user = getattr(response, "user", None)
        if user is None:
            return None

        return {
            "id": str(user.id),
            "email": user.email or "",
        }

    def get_usuario_by_auth_user_id(self, auth_user_id: UUID | str) -> dict | None:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("usuarios")
            .select(
                "id_usuario, auth_user_id, nombres, apellidos, telefono, estado, "
                "clientes(id_cliente), "
                "tecnicos(id_tecnico, estado_validacion), "
                "administradores(id_administrador)"
            )
            .eq("auth_user_id", str(auth_user_id))
            .limit(1)
        )
        rows = result.data or []
        return rows[0] if rows else None
