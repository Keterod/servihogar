import logging
from uuid import UUID

from postgrest.exceptions import APIError
from supabase._sync.client import SupabaseException

from src.repository.auth_repository import AuthRepository
from src.schemas.auth import AuthMeResponse, AuthRegisterRequest, AuthRegisterResponse, TipoUsuario

logger = logging.getLogger(__name__)


class AuthError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class AuthService:
    def __init__(self):
        self._repo = AuthRepository()

    def registrar_usuario(self, data: AuthRegisterRequest) -> AuthRegisterResponse:
        auth_user_id: str | None = None
        id_usuario: int | None = None

        try:
            auth_user_id = self._repo.create_auth_user(data.email, data.password)
            logger.info("Supabase Auth: usuario creado auth_user_id=%s email=%s", auth_user_id, data.email)
        except ValueError as exc:
            if str(exc) == "email_exists":
                raise AuthError("conflict", "El correo electrónico ya está registrado") from exc
            logger.warning("Validación en Supabase Auth: %s", exc)
            raise AuthError("validation", f"Supabase Auth: {exc}") from exc
        except Exception as exc:
            logger.exception("Error al crear usuario en Supabase Auth")
            raise self._map_auth_creation_error(exc) from exc

        try:
            usuario = self._repo.insert_usuario(
                auth_user_id,
                data.nombres,
                data.apellidos,
                data.telefono,
            )
            id_usuario = usuario["id_usuario"]
            logger.info("BD usuarios: fila creada id_usuario=%s", id_usuario)

            if data.tipo_usuario == TipoUsuario.cliente:
                cliente = self._repo.insert_cliente(id_usuario)
                logger.info("BD clientes: fila creada id_cliente=%s", cliente["id_cliente"])
                return AuthRegisterResponse(
                    id_usuario=id_usuario,
                    auth_user_id=UUID(auth_user_id),
                    email=data.email,
                    tipo_usuario=TipoUsuario.cliente,
                    id_cliente=cliente["id_cliente"],
                    mensaje="Cuenta de cliente creada correctamente. Ya puedes iniciar sesión.",
                )

            tecnico = self._repo.insert_tecnico(
                id_usuario,
                data.descripcion or "",
                data.experiencia_anios or 0,
            )
            id_tecnico = tecnico["id_tecnico"]
            logger.info("BD tecnicos: fila creada id_tecnico=%s", id_tecnico)

            if data.id_categorias:
                self._repo.insert_tecnico_categorias(id_tecnico, data.id_categorias)
            if data.id_zonas:
                self._repo.insert_tecnico_zonas(id_tecnico, data.id_zonas)

            return AuthRegisterResponse(
                id_usuario=id_usuario,
                auth_user_id=UUID(auth_user_id),
                email=data.email,
                tipo_usuario=TipoUsuario.tecnico,
                id_tecnico=id_tecnico,
                estado_validacion=tecnico["estado_validacion"],
                mensaje=(
                    "Tu cuenta fue creada y está pendiente de validación por un administrador."
                ),
            )
        except Exception as exc:
            logger.exception(
                "Error en registro tras auth_user_id=%s id_usuario=%s",
                auth_user_id,
                id_usuario,
            )
            self._rollback_registro(auth_user_id, id_usuario)
            raise self._map_registration_error(exc) from exc

    def _rollback_registro(self, auth_user_id: str | None, id_usuario: int | None) -> None:
        if id_usuario is not None:
            try:
                self._repo.delete_usuario(id_usuario)
                logger.info("Rollback: eliminado usuario id_usuario=%s", id_usuario)
            except Exception:
                logger.exception("Rollback: no se pudo eliminar usuario id_usuario=%s", id_usuario)

        if auth_user_id:
            try:
                self._repo.delete_auth_user(auth_user_id)
                logger.info("Rollback: eliminado auth user auth_user_id=%s", auth_user_id)
            except Exception:
                logger.exception("Rollback: no se pudo eliminar auth user auth_user_id=%s", auth_user_id)

    @staticmethod
    def _map_auth_creation_error(exc: Exception) -> AuthError:
        message = str(exc).lower()
        if "not configured" in message or "service_role" in message:
            return AuthError(
                "unavailable",
                "Supabase no está configurado en el backend. Revisa SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY.",
            )
        if "already" in message or "exists" in message or "registered" in message:
            return AuthError("conflict", "El correo electrónico ya está registrado")
        return AuthError("validation", f"Supabase Auth: {exc}")

    @staticmethod
    def _map_registration_error(exc: Exception) -> AuthError:
        if isinstance(exc, ValueError):
            return AuthError("validation", str(exc))

        if isinstance(exc, APIError):
            detail = AuthService._format_api_error(exc)
            return AuthError("validation", detail)

        if isinstance(exc, SupabaseException):
            detail = str(exc)
            if "query failed" in detail.lower():
                return AuthError("validation", detail)
            return AuthError("unavailable", detail)

        if isinstance(exc, RuntimeError):
            return AuthError("validation", str(exc))

        return AuthError("validation", f"{type(exc).__name__}: {exc}")

    @staticmethod
    def _format_api_error(exc: APIError) -> str:
        parts = []
        if exc.message:
            parts.append(exc.message)
        if exc.code:
            parts.append(f"code={exc.code}")
        if exc.details:
            parts.append(f"details={exc.details}")
        if exc.hint:
            parts.append(f"hint={exc.hint}")
        return "Supabase BD: " + (" | ".join(parts) if parts else str(exc))

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
