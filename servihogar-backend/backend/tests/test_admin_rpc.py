"""Tests for admin RPC migration — repository + service."""

from unittest.mock import MagicMock, patch

import pytest

# ── Mock data matching RPC JSON output ────────────────────

FAKE_RESUMEN = {
    "total_usuarios": 10,
    "total_clientes": 5,
    "total_tecnicos": 3,
    "total_solicitudes": 8,
    "solicitudes_pendientes": 3,
    "solicitudes_en_proceso": 2,
    "solicitudes_finalizadas": 3,
    "tecnicos_pendientes": 1,
    "tecnicos_validados": 2,
    "tecnicos_rechazados": 0,
    "total_cotizaciones": 6,
    "total_valoraciones": 4,
}

FAKE_TECNICO_PENDIENTE = {
    "id_tecnico": 1,
    "descripcion": "Técnico en espera",
    "experiencia_anios": 3,
    "estado_validacion": "pendiente",
    "fecha_solicitud_validacion": "2026-06-01T10:00:00+00:00",
    "usuarios": {
        "nombres": "Pedro",
        "apellidos": "López",
        "telefono": "999888777",
        "fecha_registro": "2026-05-01T10:00:00+00:00",
    },
    "tecnico_categorias": [
        {"categorias_servicio": {"nombre": "Electricidad básica"}},
    ],
    "tecnico_zonas": [
        {"zonas": {"nombre": "Huancayo Centro"}},
    ],
}

FAKE_TECNICO_ESTADO = {"id_tecnico": 1, "estado_validacion": "pendiente"}

FAKE_UPDATE_OK = {
    "ok": True,
    "tecnico": {"id_tecnico": 1, "estado_validacion": "validado"},
}

FAKE_UPDATE_NOT_FOUND = {"ok": False, "code": "not_found"}

FAKE_UPDATE_BAD_REQUEST = {"ok": False, "code": "bad_request"}


# ── Fixture ────────────────────────────────────────────────

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

class TestAdminRepository:

    def test_get_resumen_calls_rpc(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_admin_resumen", FAKE_RESUMEN)

        repo = AdminRepository()
        result = repo.get_resumen_counts()

        SupabaseClient.get().rpc.assert_called_once_with("rpc_admin_resumen")
        assert result == FAKE_RESUMEN

    def test_get_resumen_empty(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_admin_resumen", None)

        repo = AdminRepository()
        result = repo.get_resumen_counts()

        SupabaseClient.get().rpc.assert_called_once_with("rpc_admin_resumen")
        assert result == {}

    def test_get_tecnicos_pendientes_calls_rpc(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_admin_tecnicos_pendientes", [FAKE_TECNICO_PENDIENTE])

        repo = AdminRepository()
        result = repo.get_tecnicos_pendientes()

        SupabaseClient.get().rpc.assert_called_once_with("rpc_admin_tecnicos_pendientes")
        assert result == [FAKE_TECNICO_PENDIENTE]

    def test_get_tecnicos_pendientes_empty(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository

        mock_supabase("rpc_admin_tecnicos_pendientes", [])

        repo = AdminRepository()
        result = repo.get_tecnicos_pendientes()
        assert result == []

    def test_get_tecnico_estado_calls_rpc(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_admin_get_tecnico_estado", FAKE_TECNICO_ESTADO)

        repo = AdminRepository()
        result = repo.get_tecnico_estado(1)

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_admin_get_tecnico_estado", {"p_id_tecnico": 1}
        )
        assert result == FAKE_TECNICO_ESTADO

    def test_get_tecnico_estado_not_found(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository

        mock_supabase("rpc_admin_get_tecnico_estado", None)

        repo = AdminRepository()
        result = repo.get_tecnico_estado(999)
        assert result is None

    def test_update_tecnico_estado_calls_rpc(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository
        from src.repository.supabase_client import SupabaseClient

        mock_supabase("rpc_admin_actualizar_estado_tecnico", FAKE_UPDATE_OK)

        repo = AdminRepository()
        result = repo.update_tecnico_estado(1, "validado")

        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_admin_actualizar_estado_tecnico",
            {"p_id_tecnico": 1, "p_estado_validacion": "validado"},
        )
        assert result == FAKE_UPDATE_OK

    def test_update_tecnico_estado_not_found(self, mock_supabase):
        from src.repository.admin_repository import AdminRepository

        mock_supabase("rpc_admin_actualizar_estado_tecnico", FAKE_UPDATE_NOT_FOUND)

        repo = AdminRepository()
        result = repo.update_tecnico_estado(999, "validado")

        assert result == FAKE_UPDATE_NOT_FOUND


# ── Service tests ──────────────────────────────────────────

class TestAdminService:

    def test_obtener_resumen_demo(self, mock_supabase):
        from src.services.admin_service import AdminService

        mock_supabase("rpc_admin_resumen", FAKE_RESUMEN)

        service = AdminService()
        result = service.obtener_resumen_demo()

        assert result.total_usuarios == 10
        assert result.total_clientes == 5
        assert result.solicitudes_pendientes == 3
        assert result.total_valoraciones == 4

    def test_obtener_tecnicos_pendientes_demo(self, mock_supabase):
        from src.services.admin_service import AdminService

        mock_supabase("rpc_admin_tecnicos_pendientes", [FAKE_TECNICO_PENDIENTE])

        service = AdminService()
        result = service.obtener_tecnicos_pendientes_demo()

        assert len(result) == 1
        t = result[0]
        assert t.id_tecnico == 1
        assert t.nombres == "Pedro"
        assert t.apellidos == "López"
        assert t.telefono == "999888777"
        assert t.experiencia_anios == 3
        assert t.estado_validacion == "pendiente"
        assert t.categorias == ["Electricidad básica"]
        assert t.zonas == ["Huancayo Centro"]

    def test_aprobar_tecnico_demo(self, mock_supabase):
        from src.services.admin_service import AdminService

        mock_supabase("rpc_admin_get_tecnico_estado", FAKE_TECNICO_ESTADO)
        mock_supabase("rpc_admin_actualizar_estado_tecnico", FAKE_UPDATE_OK)

        service = AdminService()
        result = service.aprobar_tecnico_demo(1)

        assert result.id_tecnico == 1
        assert result.estado_validacion == "validado"

    def test_rechazar_tecnico_demo(self, mock_supabase):
        from src.services.admin_service import AdminService
        from src.repository.supabase_client import SupabaseClient

        FAKE_UPDATE_RECHAZADO = {
            "ok": True,
            "tecnico": {"id_tecnico": 1, "estado_validacion": "rechazado"},
        }

        mock_supabase("rpc_admin_get_tecnico_estado", FAKE_TECNICO_ESTADO)
        mock_supabase("rpc_admin_actualizar_estado_tecnico", FAKE_UPDATE_RECHAZADO)

        service = AdminService()
        result = service.rechazar_tecnico_demo(1)

        SupabaseClient.get().rpc.assert_called_with(
            "rpc_admin_actualizar_estado_tecnico",
            {"p_id_tecnico": 1, "p_estado_validacion": "rechazado"},
        )
        assert result.id_tecnico == 1
        assert result.estado_validacion == "rechazado"

    def test_aprobar_tecnico_not_found(self, mock_supabase):
        from src.services.admin_service import AdminError, AdminService

        mock_supabase("rpc_admin_get_tecnico_estado", None)

        service = AdminService()
        with pytest.raises(AdminError) as exc:
            service.aprobar_tecnico_demo(999)
        assert exc.value.code == "not_found"

    def test_aprobar_tecnico_not_pending(self, mock_supabase):
        from src.services.admin_service import AdminError, AdminService

        FAKE_VALIDADO = {"id_tecnico": 2, "estado_validacion": "validado"}

        mock_supabase("rpc_admin_get_tecnico_estado", FAKE_VALIDADO)

        service = AdminService()
        with pytest.raises(AdminError) as exc:
            service.aprobar_tecnico_demo(2)
        assert exc.value.code == "conflict"