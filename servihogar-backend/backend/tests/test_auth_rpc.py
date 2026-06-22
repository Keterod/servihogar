"""Tests for auth/registro RPC migration — repository + service."""

from unittest.mock import MagicMock, patch

import pytest

from src.repository.auth_repository import AuthRepository
from src.schemas.auth import AuthRegisterRequest, TipoUsuario

# ── Mock data matching RPC JSON output ────────────────────

FAKE_CLIENTE_PROFILE = {
    "id_usuario": 1,
    "auth_user_id": "eb65fb3b-d00b-40b5-82e8-933cd3cd346c",
    "nombres": "Ana",
    "apellidos": "Torres",
    "telefono": "999888777",
    "estado": "activo",
    "clientes": [{"id_cliente": 10}],
    "tecnicos": [],
    "administradores": [],
}

FAKE_TECNICO_VALIDADO_PROFILE = {
    "id_usuario": 2,
    "auth_user_id": "9ce2ac73-1b61-40de-ac53-bafc12b3eb29",
    "nombres": "Carlos",
    "apellidos": "Mendoza",
    "telefono": "999888666",
    "estado": "activo",
    "clientes": [],
    "tecnicos": [{"id_tecnico": 20, "estado_validacion": "validado"}],
    "administradores": [],
}

FAKE_TECNICO_PENDIENTE_PROFILE = {
    "id_usuario": 3,
    "auth_user_id": "3ce2ac73-1b61-40de-ac53-bafc12b3eb29",
    "nombres": "Pedro",
    "apellidos": "López",
    "telefono": "999888555",
    "estado": "activo",
    "clientes": [],
    "tecnicos": [{"id_tecnico": 30, "estado_validacion": "pendiente"}],
    "administradores": [],
}

FAKE_ADMIN_PROFILE = {
    "id_usuario": 4,
    "auth_user_id": "4ce2ac73-1b61-40de-ac53-bafc12b3eb29",
    "nombres": "Admin",
    "apellidos": "Sistema",
    "telefono": None,
    "estado": "activo",
    "clientes": [],
    "tecnicos": [],
    "administradores": [{"id_administrador": 1}],
}

FAKE_INSERT_CLIENTE_OK = {
    "ok": True,
    "usuario": {"id_usuario": 1, "auth_user_id": "eb65fb3b-d00b-40b5-82e8-933cd3cd346c"},
    "cliente": {"id_cliente": 10},
}

FAKE_INSERT_TECNICO_OK = {
    "ok": True,
    "usuario": {"id_usuario": 3, "auth_user_id": "3ce2ac73-1b61-40de-ac53-bafc12b3eb29"},
    "tecnico": {"id_tecnico": 30, "estado_validacion": "pendiente"},
}

FAKE_DUPLICATE = {"ok": False, "code": "duplicate"}

FAKE_DELETE_OK = {"ok": True}


# ── Fixture (repository tests) ────────────────────────────

@pytest.fixture
def mock_supabase():
    _rpc_data: dict[str, object] = {}

    def _setup(rpc_name: str, return_data):
        _rpc_data[rpc_name] = return_data

    with patch("src.repository.supabase_client.SupabaseClient.get") as mock_get, \
         patch("src.repository.supabase_client.SupabaseClient.execute") as mock_exec:
        mock_client = MagicMock()
        mock_get.return_value = mock_client

        def rpc_side_effect(*args, **kwargs):
            name = args[0] if args else ""
            builder = MagicMock()
            builder._rpc_name_ = name
            return builder

        mock_client.rpc.side_effect = rpc_side_effect

        def exec_side_effect(builder, **kwargs):
            name = getattr(builder, "_rpc_name_", "")
            data = _rpc_data.get(name)
            result = MagicMock()
            result.data = data
            return result

        mock_exec.side_effect = exec_side_effect

        yield _setup


# ── Repository tests ───────────────────────────────────────

class TestAuthRepositoryRPC:

    def test_get_usuario_by_auth_user_id_calls_rpc(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_auth_get_profile_by_auth_user_id", FAKE_CLIENTE_PROFILE)

        repo = AuthRepository()
        result = repo.get_usuario_by_auth_user_id("eb65fb3b-d00b-40b5-82e8-933cd3cd346c")

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_auth_get_profile_by_auth_user_id",
            {"p_auth_user_id": "eb65fb3b-d00b-40b5-82e8-933cd3cd346c"},
        )
        assert result == FAKE_CLIENTE_PROFILE

    def test_get_usuario_by_auth_user_id_not_found(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository

        mock_supabase("rpc_auth_get_profile_by_auth_user_id", None)

        repo = AuthRepository()
        result = repo.get_usuario_by_auth_user_id("unknown-uuid")
        assert result is None

    def test_insert_cliente_completo_calls_rpc(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_auth_insert_cliente", FAKE_INSERT_CLIENTE_OK)

        repo = AuthRepository()
        result = repo.insert_cliente_completo(
            "eb65fb3b-d00b-40b5-82e8-933cd3cd346c",
            "Ana", "Torres", "999888777",
        )

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_auth_insert_cliente",
            {
                "p_auth_user_id": "eb65fb3b-d00b-40b5-82e8-933cd3cd346c",
                "p_nombres": "Ana",
                "p_apellidos": "Torres",
                "p_telefono": "999888777",
            },
        )
        assert result == FAKE_INSERT_CLIENTE_OK

    def test_insert_cliente_completo_duplicate(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository

        mock_supabase("rpc_auth_insert_cliente", FAKE_DUPLICATE)

        repo = AuthRepository()
        with pytest.raises(ValueError, match="auth_user_id ya existe"):
            repo.insert_cliente_completo(
                "eb65fb3b-d00b-40b5-82e8-933cd3cd346c",
                "Ana", "Torres", "999888777",
            )

    def test_insert_tecnico_completo_calls_rpc(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_auth_insert_tecnico", FAKE_INSERT_TECNICO_OK)

        repo = AuthRepository()
        result = repo.insert_tecnico_completo(
            "3ce2ac73-1b61-40de-ac53-bafc12b3eb29",
            "Pedro", "López", "999888555",
            "Técnico electricista", 5,
            [1, 2], [3],
        )

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_auth_insert_tecnico",
            {
                "p_auth_user_id": "3ce2ac73-1b61-40de-ac53-bafc12b3eb29",
                "p_nombres": "Pedro",
                "p_apellidos": "López",
                "p_telefono": "999888555",
                "p_descripcion": "Técnico electricista",
                "p_experiencia_anios": 5,
                "p_categoria_ids": [1, 2],
                "p_zona_ids": [3],
            },
        )
        assert result == FAKE_INSERT_TECNICO_OK

    def test_insert_tecnico_completo_duplicate(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository

        mock_supabase("rpc_auth_insert_tecnico", FAKE_DUPLICATE)

        repo = AuthRepository()
        with pytest.raises(ValueError, match="auth_user_id ya existe"):
            repo.insert_tecnico_completo(
                "existing-uuid", "Pedro", "López", None,
                "Desc", 3, [], [],
            )

    def test_delete_usuario_by_auth_user_id_calls_rpc(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_auth_delete_usuario_by_auth_user_id", FAKE_DELETE_OK)

        repo = AuthRepository()
        repo.delete_usuario_by_auth_user_id("some-uuid")

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_auth_delete_usuario_by_auth_user_id",
            {"p_auth_user_id": "some-uuid"},
        )

    def test_insert_cliente_completo_without_telefono(self, mock_supabase):
        from src.repository.auth_repository import AuthRepository
        from src.repository.supabase_client import SupabaseClient

        FAKE_OK = {
            "ok": True,
            "usuario": {"id_usuario": 5, "auth_user_id": "uuid-5"},
            "cliente": {"id_cliente": 50},
        }

        mock_supabase("rpc_auth_insert_cliente", FAKE_OK)

        repo = AuthRepository()
        result = repo.insert_cliente_completo("uuid-5", "Sin", "Teléfono", None)

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_auth_insert_cliente",
            {
                "p_auth_user_id": "uuid-5",
                "p_nombres": "Sin",
                "p_apellidos": "Teléfono",
                "p_telefono": None,
            },
        )
        assert result == FAKE_OK


# ── Service tests ──────────────────────────────────────────

class TestAuthServiceMe:

    def test_me_cliente(self):
        from src.services.auth_service import AuthService

        with (
            patch.object(AuthRepository, "get_auth_user",
                         return_value={"id": "eb65fb3b-d00b-40b5-82e8-933cd3cd346c", "email": "ana@test.com"}),
            patch.object(AuthRepository, "get_usuario_by_auth_user_id",
                         return_value=FAKE_CLIENTE_PROFILE),
        ):
            service = AuthService()
            result = service.obtener_usuario_actual("Bearer token")

        assert result.id_usuario == 1
        assert result.tipo_usuario == TipoUsuario.cliente
        assert result.id_cliente == 10
        assert result.id_tecnico is None
        assert result.id_administrador is None
        assert result.email == "ana@test.com"
        assert result.nombres == "Ana"

    def test_me_tecnico_validado(self):
        from src.services.auth_service import AuthService

        with (
            patch.object(AuthRepository, "get_auth_user",
                         return_value={"id": "9ce2ac73-1b61-40de-ac53-bafc12b3eb29", "email": "carlos@test.com"}),
            patch.object(AuthRepository, "get_usuario_by_auth_user_id",
                         return_value=FAKE_TECNICO_VALIDADO_PROFILE),
        ):
            service = AuthService()
            result = service.obtener_usuario_actual("Bearer token")

        assert result.id_usuario == 2
        assert result.tipo_usuario == TipoUsuario.tecnico
        assert result.id_tecnico == 20
        assert result.estado_validacion == "validado"

    def test_me_tecnico_pendiente(self):
        from src.services.auth_service import AuthService

        with (
            patch.object(AuthRepository, "get_auth_user",
                         return_value={"id": "3ce2ac73-1b61-40de-ac53-bafc12b3eb29", "email": "pedro@test.com"}),
            patch.object(AuthRepository, "get_usuario_by_auth_user_id",
                         return_value=FAKE_TECNICO_PENDIENTE_PROFILE),
        ):
            service = AuthService()
            result = service.obtener_usuario_actual("Bearer token")

        assert result.tipo_usuario == TipoUsuario.tecnico
        assert result.estado_validacion == "pendiente"

    def test_me_admin(self):
        from src.services.auth_service import AuthService

        with (
            patch.object(AuthRepository, "get_auth_user",
                         return_value={"id": "4ce2ac73-1b61-40de-ac53-bafc12b3eb29", "email": "admin@test.com"}),
            patch.object(AuthRepository, "get_usuario_by_auth_user_id",
                         return_value=FAKE_ADMIN_PROFILE),
        ):
            service = AuthService()
            result = service.obtener_usuario_actual("Bearer token")

        assert result.tipo_usuario == TipoUsuario.administrador
        assert result.id_administrador == 1
        assert result.id_cliente is None
        assert result.id_tecnico is None

    def test_me_no_profile(self):
        from src.services.auth_service import AuthError, AuthService

        with (
            patch.object(AuthRepository, "get_auth_user",
                         return_value={"id": "unknown", "email": "no@profile.com"}),
            patch.object(AuthRepository, "get_usuario_by_auth_user_id",
                         return_value=None),
        ):
            service = AuthService()
            with pytest.raises(AuthError) as exc:
                service.obtener_usuario_actual("Bearer token")
            assert exc.value.code == "not_found"

    def test_me_no_token(self):
        from src.services.auth_service import AuthError, AuthService

        service = AuthService()
        with pytest.raises(AuthError) as exc:
            service.obtener_usuario_actual(None)
        assert exc.value.code == "unauthorized"

    def test_me_invalid_token(self):
        from src.services.auth_service import AuthError, AuthService

        with patch.object(AuthRepository, "get_auth_user", return_value=None):
            service = AuthService()
            with pytest.raises(AuthError) as exc:
                service.obtener_usuario_actual("Bearer invalid")
            assert exc.value.code == "unauthorized"


# ── Registro service tests ─────────────────────────────────

class TestAuthServiceRegistro:

    FAKE_USER = {
        "id_usuario": 1,
        "auth_user_id": "eb65fb3b-d00b-40b5-82e8-933cd3cd346c",
    }

    def _cliente_request(self):
        return AuthRegisterRequest(
            nombres="Ana",
            apellidos="Torres",
            email="ana@test.com",
            password="123456",
            tipo_usuario=TipoUsuario.cliente,
            telefono="999888777",
        )

    def _tecnico_request(self):
        return AuthRegisterRequest(
            nombres="Pedro",
            apellidos="López",
            email="pedro@test.com",
            password="123456",
            tipo_usuario=TipoUsuario.tecnico,
            telefono="999888555",
            descripcion="Técnico electricista",
            experiencia_anios=5,
            id_categorias=[1, 2],
            id_zonas=[3],
        )

    def test_registro_cliente_exitoso(self):
        from src.services.auth_service import AuthService

        with (
            patch.object(AuthRepository, "create_auth_user",
                         return_value="eb65fb3b-d00b-40b5-82e8-933cd3cd346c"),
            patch.object(AuthRepository, "insert_cliente_completo",
                         return_value=FAKE_INSERT_CLIENTE_OK),
        ):
            service = AuthService()
            result = service.registrar_usuario(self._cliente_request())

        assert result.id_usuario == 1
        assert result.id_cliente == 10
        assert result.tipo_usuario == TipoUsuario.cliente
        assert "Cuenta de cliente" in result.mensaje

    def test_registro_tecnico_exitoso(self):
        from src.services.auth_service import AuthService

        with (
            patch.object(AuthRepository, "create_auth_user",
                         return_value="3ce2ac73-1b61-40de-ac53-bafc12b3eb29"),
            patch.object(AuthRepository, "insert_tecnico_completo",
                         return_value=FAKE_INSERT_TECNICO_OK),
        ):
            service = AuthService()
            result = service.registrar_usuario(self._tecnico_request())

        assert result.id_usuario == 3
        assert result.id_tecnico == 30
        assert result.estado_validacion == "pendiente"
        assert result.tipo_usuario == TipoUsuario.tecnico
        assert "pendiente de validación" in result.mensaje

    def test_registro_cliente_duplicate(self):
        from src.services.auth_service import AuthError, AuthService

        def _raise_duplicate(*args, **kwargs):
            raise ValueError("auth_user_id ya existe")

        with (
            patch.object(AuthRepository, "create_auth_user",
                         return_value="eb65fb3b-d00b-40b5-82e8-933cd3cd346c"),
            patch.object(AuthRepository, "insert_cliente_completo",
                         side_effect=_raise_duplicate),
            patch.object(AuthRepository, "delete_usuario_by_auth_user_id"),
            patch.object(AuthRepository, "delete_auth_user"),
        ):
            service = AuthService()
            with pytest.raises(AuthError) as exc:
                service.registrar_usuario(self._cliente_request())

            assert exc.value.code == "validation"

    def test_registro_rollback_on_error(self):
        from src.services.auth_service import AuthError, AuthService

        def _raise_runtime(*args, **kwargs):
            raise RuntimeError("DB error")

        with (
            patch.object(AuthRepository, "create_auth_user",
                         return_value="eb65fb3b-d00b-40b5-82e8-933cd3cd346c"),
            patch.object(AuthRepository, "insert_cliente_completo",
                         side_effect=_raise_runtime),
            patch.object(AuthRepository, "delete_usuario_by_auth_user_id") as mock_del_user,
            patch.object(AuthRepository, "delete_auth_user") as mock_del_auth,
        ):
            service = AuthService()
            with pytest.raises(AuthError):
                service.registrar_usuario(self._cliente_request())

            mock_del_user.assert_called_once_with("eb65fb3b-d00b-40b5-82e8-933cd3cd346c")
            mock_del_auth.assert_called_once_with("eb65fb3b-d00b-40b5-82e8-933cd3cd346c")

    def test_registro_tecnico_sin_categorias_ni_zonas(self):
        from src.services.auth_service import AuthService

        request = AuthRegisterRequest(
            nombres="Simple",
            apellidos="Tecnico",
            email="simple@test.com",
            password="123456",
            tipo_usuario=TipoUsuario.tecnico,
            telefono=None,
            descripcion="Técnico básico",
            experiencia_anios=1,
        )

        FAKE_SIMPLE = {
            "ok": True,
            "usuario": {"id_usuario": 5, "auth_user_id": "00000000-0000-0000-0000-000000000005"},
            "tecnico": {"id_tecnico": 50, "estado_validacion": "pendiente"},
        }

        with (
            patch.object(AuthRepository, "create_auth_user",
                         return_value="00000000-0000-0000-0000-000000000005"),
            patch.object(AuthRepository, "insert_tecnico_completo",
                         return_value=FAKE_SIMPLE),
        ):
            service = AuthService()
            result = service.registrar_usuario(request)

        assert result.id_tecnico == 50
        assert result.estado_validacion == "pendiente"

    def test_registro_email_duplicate(self):
        from src.services.auth_service import AuthError, AuthService

        with patch.object(AuthRepository, "create_auth_user",
                          side_effect=ValueError("email_exists")):
            service = AuthService()
            with pytest.raises(AuthError) as exc:
                service.registrar_usuario(self._cliente_request())
            assert exc.value.code == "conflict"
