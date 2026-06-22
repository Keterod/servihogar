"""Tests for valoraciones RPC migration — repository.

Verifies the repository calls the correct RPC functions
and data mapping works correctly.
"""

from unittest.mock import MagicMock, patch

import pytest


FAKE_VALORACION = {
    "id_valoracion": 1,
    "id_cotizacion": 10,
    "puntuacion": 5,
    "comentario": "Excelente servicio",
    "puntualidad": 5,
    "calidad": 4,
    "precio": 5,
    "trato": 5,
    "fecha_valoracion": "2026-06-15T10:00:00",
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


class TestValoracionesRepository:
    def test_exists_true(self, mock_supabase):
        from src.repository.valoraciones_repository import ValoracionesRepository

        mock_supabase("rpc_exists_valoracion_cotizacion", True)

        repo = ValoracionesRepository()
        result = repo.exists_for_cotizacion(10)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_exists_valoracion_cotizacion", {"p_id_cotizacion": 10}
        )
        assert result is True

    def test_exists_false(self, mock_supabase):
        from src.repository.valoraciones_repository import ValoracionesRepository

        mock_supabase("rpc_exists_valoracion_cotizacion", False)

        repo = ValoracionesRepository()
        result = repo.exists_for_cotizacion(99)

        assert result is False

    def test_insert_calls_rpc(self, mock_supabase):
        from src.repository.valoraciones_repository import ValoracionesRepository

        mock_supabase("rpc_insert_valoracion", FAKE_VALORACION)

        repo = ValoracionesRepository()
        payload = {
            "id_cotizacion": 10,
            "puntuacion": 5,
            "comentario": "Excelente servicio",
            "puntualidad": 5,
            "calidad": 4,
            "precio": 5,
            "trato": 5,
        }
        result = repo.insert(payload)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_valoracion",
            {
                "p_id_cotizacion": 10,
                "p_puntuacion": 5,
                "p_comentario": "Excelente servicio",
                "p_puntualidad": 5,
                "p_calidad": 4,
                "p_precio": 5,
                "p_trato": 5,
            },
        )
        assert result == FAKE_VALORACION

    def test_insert_only_required_fields(self, mock_supabase):
        from src.repository.valoraciones_repository import ValoracionesRepository

        FAKE_MIN = {**FAKE_VALORACION, "comentario": None, "puntualidad": None, "calidad": None, "precio": None, "trato": None}
        mock_supabase("rpc_insert_valoracion", FAKE_MIN)

        repo = ValoracionesRepository()
        payload = {"id_cotizacion": 10, "puntuacion": 4}
        result = repo.insert(payload)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_valoracion",
            {
                "p_id_cotizacion": 10,
                "p_puntuacion": 4,
                "p_comentario": None,
                "p_puntualidad": None,
                "p_calidad": None,
                "p_precio": None,
                "p_trato": None,
            },
        )
        assert result == FAKE_MIN

    def test_insert_returns_none_when_no_data(self, mock_supabase):
        from src.repository.valoraciones_repository import ValoracionesRepository

        mock_supabase("rpc_insert_valoracion", None)

        repo = ValoracionesRepository()
        result = repo.insert({"id_cotizacion": 10, "puntuacion": 5})

        assert result is None
