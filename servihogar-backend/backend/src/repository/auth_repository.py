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

    def delete_usuario(self, id_usuario: int) -> None:
        client = SupabaseClient.get()
        SupabaseClient.execute(
            client.table("usuarios").delete().eq("id_usuario", id_usuario),
            context="delete usuarios",
        )

    def insert_usuario(
        self,
        auth_user_id: str,
        nombres: str,
        apellidos: str,
        telefono: str | None,
    ) -> dict:
        client = SupabaseClient.get()
        payload = {
            "auth_user_id": auth_user_id,
            "nombres": nombres.strip(),
            "apellidos": apellidos.strip(),
            "telefono": telefono.strip() if telefono else None,
            "estado": "activo",
        }
        result = SupabaseClient.execute(
            client.table("usuarios").insert(payload).select("id_usuario, auth_user_id"),
            context="insert usuarios",
        )
        rows = result.data or []
        if not rows:
            raise RuntimeError("Insert en usuarios no devolvió filas")
        return rows[0]

    def insert_cliente(self, id_usuario: int) -> dict:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("clientes")
            .insert({"id_usuario": id_usuario, "estado": "activo"})
            .select("id_cliente"),
            context="insert clientes",
        )
        rows = result.data or []
        if not rows:
            raise RuntimeError("Insert en clientes no devolvió filas")
        return rows[0]

    def insert_tecnico(
        self,
        id_usuario: int,
        descripcion: str,
        experiencia_anios: int,
    ) -> dict:
        client = SupabaseClient.get()
        result = SupabaseClient.execute(
            client.table("tecnicos")
            .insert(
                {
                    "id_usuario": id_usuario,
                    "descripcion": descripcion.strip(),
                    "experiencia_anios": experiencia_anios,
                    "estado_validacion": "pendiente",
                }
            )
            .select("id_tecnico, estado_validacion"),
            context="insert tecnicos",
        )
        rows = result.data or []
        if not rows:
            raise RuntimeError("tecnico_insert_failed")
        return rows[0]

    def insert_tecnico_categorias(self, id_tecnico: int, id_categorias: list[int]) -> None:
        if not id_categorias:
            return

        client = SupabaseClient.get()
        rows = [{"id_tecnico": id_tecnico, "id_categoria": cid} for cid in id_categorias]
        SupabaseClient.execute(client.table("tecnico_categorias").insert(rows))

    def insert_tecnico_zonas(self, id_tecnico: int, id_zonas: list[int]) -> None:
        if not id_zonas:
            return

        client = SupabaseClient.get()
        rows = [{"id_tecnico": id_tecnico, "id_zona": zid} for zid in id_zonas]
        SupabaseClient.execute(client.table("tecnico_zonas").insert(rows))
