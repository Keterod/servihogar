"""Tests for aceptar/rechazar cotización RPC migration — repository + service.

Verifies the repository calls the correct RPC functions,
error codes map correctly, and service raises proper exceptions.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


FAKE_ACCEPT_OK = {
    "ok": True,
    "cotizacion": {
        "id_cotizacion": 1,
        "id_solicitud": 10,
        "id_tecnico": 5,
        "monto": 150.00,
        "descripcion": "Propuesta aceptada",
        "tiempo_estimado": "2 días",
        "estado": "aceptada",
        "fecha_envio": "2026-06-15T10:00:00",
    },
    "solicitud_estado": "en_proceso",
}

FAKE_REJECT_OK = {
    "ok": True,
    "cotizacion": {**FAKE_ACCEPT_OK["cotizacion"], "estado": "rechazada"},
    "solicitud_estado": "pendiente",
}

FAKE_NOT_FOUND = {"ok": False, "code": "not_found"}
FAKE_FORBIDDEN = {"ok": False, "code": "forbidden"}
FAKE_BAD_REQUEST = {"ok": False, "code": "bad_request"}
FAKE_CONFLICT = {"ok": False, "code": "conflict"}


@pytest.fixture
def mock_supabase():
    with patch("src.repository.supabase_client.SupabaseClient.get") as mock_get, \
         patch("src.repository.supabase_client.SupabaseClient.execute") as mock_exec:
        mock_client = MagicMock()
        mock_get.return_value = mock_client

        def _setup(rpc_name: str, return_data):
            rpc_builder = MagicMock()
            mock_client.rpc.return_value = rpc_builder
            mock_result = MagicMock()
            mock_result.data = return_data
            mock_exec.return_value = mock_result

        yield _setup


# ── Repository tests ──────────────────────────────────────

class TestCotizacionesRepositoryAcceptReject:
    def test_aceptar_calls_rpc(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_ACCEPT_OK)

        repo = CotizacionesRepository()
        result = repo.aceptar_cotizacion_cliente(1, 10)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_aceptar_cotizacion_cliente",
            {"p_id_cotizacion": 1, "p_id_cliente": 10},
        )
        assert result == FAKE_ACCEPT_OK
        assert result["ok"] is True
        assert result["cotizacion"]["estado"] == "aceptada"
        assert result["solicitud_estado"] == "en_proceso"

    def test_rechazar_calls_rpc(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_rechazar_cotizacion_cliente", FAKE_REJECT_OK)

        repo = CotizacionesRepository()
        result = repo.rechazar_cotizacion_cliente(1, 10)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_rechazar_cotizacion_cliente",
            {"p_id_cotizacion": 1, "p_id_cliente": 10},
        )
        assert result == FAKE_REJECT_OK
        assert result["ok"] is True
        assert result["cotizacion"]["estado"] == "rechazada"

    def test_aceptar_not_found(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_NOT_FOUND)

        repo = CotizacionesRepository()
        result = repo.aceptar_cotizacion_cliente(999, 10)
        assert result["ok"] is False
        assert result["code"] == "not_found"

    def test_rechazar_forbidden(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_rechazar_cotizacion_cliente", FAKE_FORBIDDEN)

        repo = CotizacionesRepository()
        result = repo.rechazar_cotizacion_cliente(1, 99)
        assert result["ok"] is False
        assert result["code"] == "forbidden"

    def test_aceptar_conflict(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_CONFLICT)

        repo = CotizacionesRepository()
        result = repo.aceptar_cotizacion_cliente(1, 10)
        assert result["ok"] is False
        assert result["code"] == "conflict"

    def test_aceptar_bad_request(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_BAD_REQUEST)

        repo = CotizacionesRepository()
        result = repo.aceptar_cotizacion_cliente(1, 10)
        assert result["ok"] is False
        assert result["code"] == "bad_request"


# ── Service tests ─────────────────────────────────────────

class TestCotizacionesServiceAcceptReject:
    def test_aceptar_ok(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionesService

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_ACCEPT_OK)

        service = CotizacionesService()
        result = service.aceptar_cotizacion_para_cliente(1, 10)

        assert result.id_cotizacion == 1
        assert result.precio == 150.00
        assert result.estado == "aceptada"
        assert result.solicitud_estado == "en_proceso"

    def test_rechazar_ok(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionesService

        mock_supabase("rpc_rechazar_cotizacion_cliente", FAKE_REJECT_OK)

        service = CotizacionesService()
        result = service.rechazar_cotizacion_para_cliente(1, 10)

        assert result.id_cotizacion == 1
        assert result.estado == "rechazada"
        assert result.solicitud_estado == "pendiente"

    def test_aceptar_not_found_raises(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionError, CotizacionesService

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_NOT_FOUND)

        service = CotizacionesService()
        with pytest.raises(CotizacionError) as exc:
            service.aceptar_cotizacion_para_cliente(999, 10)
        assert exc.value.code == "not_found"

    def test_rechazar_forbidden_raises(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionError, CotizacionesService

        mock_supabase("rpc_rechazar_cotizacion_cliente", FAKE_FORBIDDEN)

        service = CotizacionesService()
        with pytest.raises(CotizacionError) as exc:
            service.rechazar_cotizacion_para_cliente(1, 99)
        assert exc.value.code == "forbidden"

    def test_aceptar_conflict_raises(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionError, CotizacionesService

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_CONFLICT)

        service = CotizacionesService()
        with pytest.raises(CotizacionError) as exc:
            service.aceptar_cotizacion_para_cliente(1, 10)
        assert exc.value.code == "conflict"

    def test_aceptar_bad_request_raises(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionError, CotizacionesService

        mock_supabase("rpc_aceptar_cotizacion_cliente", FAKE_BAD_REQUEST)

        service = CotizacionesService()
        with pytest.raises(CotizacionError) as exc:
            service.aceptar_cotizacion_para_cliente(1, 10)
        assert exc.value.code == "bad_request"

    def test_rechazar_bad_request_raises(self, mock_supabase):
        from src.services.cotizaciones_service import CotizacionError, CotizacionesService

        mock_supabase("rpc_rechazar_cotizacion_cliente", FAKE_BAD_REQUEST)

        service = CotizacionesService()
        with pytest.raises(CotizacionError) as exc:
            service.rechazar_cotizacion_para_cliente(1, 10)
        assert exc.value.code == "bad_request"
