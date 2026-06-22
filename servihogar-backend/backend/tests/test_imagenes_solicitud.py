"""Tests for imagenes solicitud RPC migration — repository.

Verifies the repository calls the correct RPC functions
and data mapping works correctly.
"""

from unittest.mock import MagicMock, patch

import pytest


FAKE_IMAGEN_INSERTADA = {
    "id_imagen": 10,
    "id_solicitud": 1,
    "imagen_url": "solicitudes/1/foto.jpg",
    "descripcion": "Foto del baño",
    "fecha_subida": "2026-06-15T12:00:00",
}

FAKE_LISTA_IMAGENES = [
    {
        "id_imagen": 1,
        "imagen_url": "solicitudes/1/foto1.jpg",
        "descripcion": "Foto 1",
        "fecha_subida": "2026-06-15T12:00:00",
    },
    {
        "id_imagen": 2,
        "imagen_url": "solicitudes/1/foto2.jpg",
        "descripcion": None,
        "fecha_subida": "2026-06-15T12:30:00",
    },
]


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


class TestImagenesSolicitudRepository:
    def test_insert_calls_rpc(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_insert_imagen_solicitud", FAKE_IMAGEN_INSERTADA)

        repo = ImagenesSolicitudRepository()
        result = repo.insert(1, "solicitudes/1/foto.jpg", "Foto del baño")

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_imagen_solicitud",
            {
                "p_id_solicitud": 1,
                "p_imagen_url": "solicitudes/1/foto.jpg",
                "p_descripcion": "Foto del baño",
            },
        )
        assert result == FAKE_IMAGEN_INSERTADA

    def test_insert_sin_descripcion(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        FAKE_SIN_DESC = {**FAKE_IMAGEN_INSERTADA, "descripcion": None}
        mock_supabase("rpc_insert_imagen_solicitud", FAKE_SIN_DESC)

        repo = ImagenesSolicitudRepository()
        result = repo.insert(1, "solicitudes/1/foto.jpg")

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_imagen_solicitud",
            {
                "p_id_solicitud": 1,
                "p_imagen_url": "solicitudes/1/foto.jpg",
            },
        )
        assert result == FAKE_SIN_DESC

    def test_insert_returns_none_when_no_data(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_insert_imagen_solicitud", None)

        repo = ImagenesSolicitudRepository()
        result = repo.insert(1, "solicitudes/1/foto.jpg")

        assert result is None

    def test_count_by_solicitud_calls_rpc(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_count_imagenes_solicitud", 3)

        repo = ImagenesSolicitudRepository()
        result = repo.count_by_solicitud(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_count_imagenes_solicitud", {"p_id_solicitud": 1}
        )
        assert result == 3

    def test_count_by_solicitud_zero(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_count_imagenes_solicitud", 0)

        repo = ImagenesSolicitudRepository()
        result = repo.count_by_solicitud(99)

        assert result == 0

    def test_list_by_solicitud_calls_rpc(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_listar_imagenes_solicitud", FAKE_LISTA_IMAGENES)

        repo = ImagenesSolicitudRepository()
        result = repo.list_by_solicitud(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_listar_imagenes_solicitud", {"p_id_solicitud": 1}
        )
        assert result == FAKE_LISTA_IMAGENES
        assert len(result) == 2
        assert result[0]["imagen_url"] == "solicitudes/1/foto1.jpg"
        assert result[1]["descripcion"] is None

    def test_list_by_solicitud_empty(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_listar_imagenes_solicitud", [])

        repo = ImagenesSolicitudRepository()
        result = repo.list_by_solicitud(99)

        assert result == []

    def test_list_by_solicitud_none_data(self, mock_supabase):
        from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository

        mock_supabase("rpc_listar_imagenes_solicitud", None)

        repo = ImagenesSolicitudRepository()
        result = repo.list_by_solicitud(99)

        assert result == []
