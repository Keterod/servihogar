"""Tests for cotizaciones básicas RPC migration — repository.

Verifies the repository calls the correct RPC functions
and data mapping works correctly.
"""

from unittest.mock import MagicMock, patch

import pytest


FAKE_COTIZACION = {
    "id_cotizacion": 1,
    "id_solicitud": 10,
    "id_tecnico": 5,
    "monto": 150.00,
    "descripcion": "Propuesta de reparación",
    "tiempo_estimado": "2 días",
    "estado": "pendiente",
    "fecha_envio": "2026-06-15T10:00:00",
}

FAKE_COTIZACION_ACEPTADA = {
    "id_cotizacion": 2,
    "id_solicitud": 10,
    "id_tecnico": 5,
    "estado": "aceptada",
}


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


class TestCotizacionesRepositoryBasicas:
    # -- exists_for_tecnico --

    def test_exists_for_tecnico_true(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_exists_cotizacion_tecnico", True)

        repo = CotizacionesRepository()
        result = repo.exists_for_tecnico(10, 5)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_exists_cotizacion_tecnico",
            {"p_id_solicitud": 10, "p_id_tecnico": 5},
        )
        assert result is True

    def test_exists_for_tecnico_false(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_exists_cotizacion_tecnico", False)

        repo = CotizacionesRepository()
        result = repo.exists_for_tecnico(10, 5)

        assert result is False

    # -- get_by_id --

    def test_get_by_id_calls_rpc(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_get_cotizacion_by_id", FAKE_COTIZACION)

        repo = CotizacionesRepository()
        result = repo.get_by_id(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_get_cotizacion_by_id", {"p_id_cotizacion": 1}
        )
        assert result == FAKE_COTIZACION

    def test_get_by_id_not_found(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_get_cotizacion_by_id", None)

        repo = CotizacionesRepository()
        result = repo.get_by_id(999)

        assert result is None

    # -- has_accepted_for_solicitud --

    def test_has_accepted_true(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_has_cotizacion_aceptada_solicitud", True)

        repo = CotizacionesRepository()
        result = repo.has_accepted_for_solicitud(10)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_has_cotizacion_aceptada_solicitud", {"p_id_solicitud": 10}
        )
        assert result is True

    def test_has_accepted_false(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_has_cotizacion_aceptada_solicitud", False)

        repo = CotizacionesRepository()
        result = repo.has_accepted_for_solicitud(99)

        assert result is False

    # -- get_accepted_for_solicitud --

    def test_get_accepted_calls_rpc(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_get_cotizacion_aceptada_solicitud", FAKE_COTIZACION_ACEPTADA)

        repo = CotizacionesRepository()
        result = repo.get_accepted_for_solicitud(10)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_get_cotizacion_aceptada_solicitud", {"p_id_solicitud": 10}
        )
        assert result == FAKE_COTIZACION_ACEPTADA
        assert result["id_cotizacion"] == 2
        assert result["estado"] == "aceptada"

    def test_get_accepted_not_found(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_get_cotizacion_aceptada_solicitud", None)

        repo = CotizacionesRepository()
        result = repo.get_accepted_for_solicitud(99)

        assert result is None

    # -- insert --

    def test_insert_calls_rpc(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_insert_cotizacion", FAKE_COTIZACION)

        repo = CotizacionesRepository()
        payload = {
            "id_solicitud": 10,
            "id_tecnico": 5,
            "monto": 150.00,
            "descripcion": "Propuesta de reparación",
            "tiempo_estimado": "2 días",
        }
        result = repo.insert(payload)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_cotizacion",
            {
                "p_id_solicitud": 10,
                "p_id_tecnico": 5,
                "p_monto": 150.00,
                "p_descripcion": "Propuesta de reparación",
                "p_tiempo_estimado": "2 días",
            },
        )
        assert result == FAKE_COTIZACION

    def test_insert_sin_tiempo_estimado(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        FAKE_SIN_TIEMPO = {**FAKE_COTIZACION, "tiempo_estimado": None}
        mock_supabase("rpc_insert_cotizacion", FAKE_SIN_TIEMPO)

        repo = CotizacionesRepository()
        payload = {
            "id_solicitud": 10,
            "id_tecnico": 5,
            "monto": 150.00,
            "descripcion": "Propuesta",
        }
        result = repo.insert(payload)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_cotizacion",
            {
                "p_id_solicitud": 10,
                "p_id_tecnico": 5,
                "p_monto": 150.00,
                "p_descripcion": "Propuesta",
                "p_tiempo_estimado": None,
            },
        )
        assert result == FAKE_SIN_TIEMPO

    def test_insert_returns_none_when_no_data(self, mock_supabase):
        from src.repository.cotizaciones_repository import CotizacionesRepository

        mock_supabase("rpc_insert_cotizacion", None)

        repo = CotizacionesRepository()
        result = repo.insert({
            "id_solicitud": 10,
            "id_tecnico": 5,
            "monto": 150.00,
            "descripcion": "Propuesta",
        })

        assert result is None
