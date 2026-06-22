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
            client.rpc(
                "rpc_auth_get_profile_by_auth_user_id",
                {"p_auth_user_id": str(auth_user_id)},
            )
        )
        return result.data

    def create_auth_user(self, email: str, password: str) -> str:
        client = SupabaseClient.get()
        try:
            response = client.auth.admin.create_user(
                {
                    "email": email.strip().lower(),
                    "password": password,
                    "email_confirm": True,
                }
            )
        except Exception as exc:
            message = str(exc).lower()
            if "already" in message or "exists" in message or "registered" in message:
                raise ValueError("email_exists") from exc
            raise RuntimeError(f"Supabase Auth create_user falló: {exc}") from exc

        user = getattr(response, "user", None)
        if user is None:
            raise RuntimeError("Supabase Auth create_user no devolvió usuario")

        return str(user.id)

    def delete_auth_user(self, auth_user_id: str) -> None:
        client = SupabaseClient.get()
        try:
            client.auth.admin.delete_user(auth_user_id)
        except Exception:
            pass

    def delete_usuario_by_auth_user_id(self, auth_user_id: str) -> None:
        client = SupabaseClient.get()
        SupabaseClient.execute(
            client.rpc(
                "rpc_auth_delete_usuario_by_auth_user_id",
                {"p_auth_user_id": auth_user_id},
            ),
            context="delete usuarios by auth_user_id",
        )

    def insert_cliente_completo(
        self,
        auth_user_id: str,
        nombres: str,
        apellidos: str,
        telefono: str | None,
        foto_perfil_url: str | None = None,
    ) -> dict:
        client = SupabaseClient.get()
        params: dict = {
            "p_auth_user_id": auth_user_id,
            "p_nombres": nombres.strip(),
            "p_apellidos": apellidos.strip(),
            "p_telefono": telefono.strip() if telefono else None,
        }
        if foto_perfil_url is not None:
            params["p_foto_perfil_url"] = foto_perfil_url

        result = SupabaseClient.execute(
            client.rpc("rpc_auth_insert_cliente", params),
            context="insert cliente completo",
        )

        data = result.data
        if not data or not data.get("ok"):
            code = data.get("code", "failed") if data else "failed"
            if code == "duplicate":
                raise ValueError("auth_user_id ya existe")
            raise RuntimeError(f"Error al insertar cliente: {code}")

        return data

    def insert_tecnico_completo(
        self,
        auth_user_id: str,
        nombres: str,
        apellidos: str,
        telefono: str | None,
        descripcion: str,
        experiencia_anios: int,
        id_categorias: list[int] | None = None,
        id_zonas: list[int] | None = None,
        foto_perfil_url: str | None = None,
    ) -> dict:
        client = SupabaseClient.get()
        params: dict = {
            "p_auth_user_id": auth_user_id,
            "p_nombres": nombres.strip(),
            "p_apellidos": apellidos.strip(),
            "p_telefono": telefono.strip() if telefono else None,
            "p_descripcion": descripcion.strip(),
            "p_experiencia_anios": experiencia_anios,
        }
        if id_categorias:
            params["p_categoria_ids"] = id_categorias
        if id_zonas:
            params["p_zona_ids"] = id_zonas
        if foto_perfil_url is not None:
            params["p_foto_perfil_url"] = foto_perfil_url

        result = SupabaseClient.execute(
            client.rpc("rpc_auth_insert_tecnico", params),
            context="insert tecnico completo",
        )

        data = result.data
        if not data or not data.get("ok"):
            code = data.get("code", "failed") if data else "failed"
            if code == "duplicate":
                raise ValueError("auth_user_id ya existe")
            raise RuntimeError(f"Error al insertar técnico: {code}")

        return data
