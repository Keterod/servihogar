from uuid import UUID

from src.repository.auth_repository import AuthRepository
from src.schemas.auth import AuthMeResponse, TipoUsuario


class AuthError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class AuthService:
    def __init__(self):
        self._repo = AuthRepository()

    def obtener_usuario_actual(self, authorization: str | None) -> AuthMeResponse:
        token = self._extract_bearer_token(authorization)
        if not token:
            raise AuthError("unauthorized", "Token de autenticación requerido")

        auth_user = self._repo.get_auth_user(token)
        if auth_user is None:
            raise AuthError("unauthorized", "Token inválido o expirado")

        usuario = self._repo.get_usuario_by_auth_user_id(auth_user["id"])
        if usuario is None:
            raise AuthError(
                "not_found",
                "No existe un perfil de ServiHogar vinculado a este usuario",
            )

        return self._build_response(usuario, auth_user["email"])

    @staticmethod
    def _extract_bearer_token(authorization: str | None) -> str | None:
        if not authorization:
            return None

        parts = authorization.strip().split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        token = parts[1].strip()
        return token or None

    def _build_response(self, usuario: dict, email: str) -> AuthMeResponse:
        tipo_usuario, id_cliente, id_tecnico, id_administrador, estado_validacion = (
            self._derive_role(usuario)
        )

        return AuthMeResponse(
            id_usuario=usuario["id_usuario"],
            auth_user_id=UUID(str(usuario["auth_user_id"])),
            nombres=usuario["nombres"],
            apellidos=usuario["apellidos"],
            email=email,
            tipo_usuario=tipo_usuario,
            estado=usuario["estado"],
            id_cliente=id_cliente,
            id_tecnico=id_tecnico,
            id_administrador=id_administrador,
            estado_validacion=estado_validacion,
        )

    def _derive_role(
        self, usuario: dict
    ) -> tuple[TipoUsuario, int | None, int | None, int | None, str | None]:
        administrador = self._unwrap_embedded(usuario.get("administradores"))
        if administrador:
            return (
                TipoUsuario.administrador,
                None,
                None,
                administrador.get("id_administrador"),
                None,
            )

        tecnico = self._unwrap_embedded(usuario.get("tecnicos"))
        if tecnico:
            return (
                TipoUsuario.tecnico,
                None,
                tecnico.get("id_tecnico"),
                None,
                tecnico.get("estado_validacion"),
            )

        cliente = self._unwrap_embedded(usuario.get("clientes"))
        if cliente:
            return (
                TipoUsuario.cliente,
                cliente.get("id_cliente"),
                None,
                None,
                None,
            )

        raise AuthError(
            "not_found",
            "El usuario no tiene un perfil de cliente, técnico o administrador",
        )

    @staticmethod
    def _unwrap_embedded(value):
        if value is None:
            return None
        if isinstance(value, list):
            return value[0] if value else None
        return value
