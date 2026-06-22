"""Tests for portafolio técnico RPC migration — repository.

Verifies the repository calls the correct RPC functions
and data mapping works correctly.
"""

from unittest.mock import MagicMock, patch

import pytest


FAKE_PORTAFOLIO_ITEM_1 = {
    "id_portafolio": 1,
    "titulo": "Reparación de caño",
    "descripcion": "Antes y después",
    "imagen_url": "tecnicos/1/portafolio/foto1.jpg",
    "estado": "visible",
    "fecha_subida": "2026-06-15T10:00:00",
}

FAKE_PORTAFOLIO_ITEM_2 = {
    "id_portafolio": 2,
    "titulo": "Instalación de lavatorio",
    "descripcion": None,
    "imagen_url": "tecnicos/1/portafolio/foto2.jpg",
    "estado": "visible",
    "fecha_subida": "2026-06-14T15:30:00",
}

FAKE_LISTA = [FAKE_PORTAFOLIO_ITEM_1, FAKE_PORTAFOLIO_ITEM_2]

FAKE_INSERTADO = {
    "id_portafolio": 3,
    "id_tecnico": 1,
    "titulo": "Nuevo trabajo",
    "descripcion": "Descripción del trabajo",
    "imagen_url": "tecnicos/1/portafolio/nuevo.jpg",
    "estado": "visible",
    "fecha_subida": "2026-06-16T10:00:00",
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


class TestPortafolioTecnicoRepository:
    def test_list_portafolio_calls_rpc(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_listar_portafolio_tecnico", FAKE_LISTA)

        repo = TecnicosRepository()
        result = repo.list_portafolio_for_tecnico(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_listar_portafolio_tecnico", {"p_id_tecnico": 1}
        )
        assert result == FAKE_LISTA
        assert len(result) == 2
        assert result[0]["titulo"] == "Reparación de caño"
        assert result[1]["estado"] == "visible"

    def test_list_portafolio_empty(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_listar_portafolio_tecnico", [])

        repo = TecnicosRepository()
        result = repo.list_portafolio_for_tecnico(99)

        assert result == []

    def test_list_portafolio_none_data(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_listar_portafolio_tecnico", None)

        repo = TecnicosRepository()
        result = repo.list_portafolio_for_tecnico(99)

        assert result == []

    def test_count_portafolio_visible_calls_rpc(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_count_portafolio_visible", 3)

        repo = TecnicosRepository()
        result = repo.count_portafolio_visible(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_count_portafolio_visible", {"p_id_tecnico": 1}
        )
        assert result == 3

    def test_count_portafolio_visible_zero(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_count_portafolio_visible", 0)

        repo = TecnicosRepository()
        result = repo.count_portafolio_visible(99)

        assert result == 0

    def test_insert_portafolio_calls_rpc(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_insert_portafolio_tecnico", FAKE_INSERTADO)

        repo = TecnicosRepository()
        result = repo.insert_portafolio(
            1, "Nuevo trabajo", "tecnicos/1/portafolio/nuevo.jpg", "Descripción del trabajo"
        )

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_portafolio_tecnico",
            {
                "p_id_tecnico": 1,
                "p_titulo": "Nuevo trabajo",
                "p_imagen_url": "tecnicos/1/portafolio/nuevo.jpg",
                "p_descripcion": "Descripción del trabajo",
            },
        )
        assert result == FAKE_INSERTADO

    def test_insert_portafolio_sin_descripcion(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        FAKE_SIN_DESC = {**FAKE_INSERTADO, "descripcion": None}
        mock_supabase("rpc_insert_portafolio_tecnico", FAKE_SIN_DESC)

        repo = TecnicosRepository()
        result = repo.insert_portafolio(1, "Título solo", "url.jpg")

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_insert_portafolio_tecnico",
            {
                "p_id_tecnico": 1,
                "p_titulo": "Título solo",
                "p_imagen_url": "url.jpg",
            },
        )
        assert result == FAKE_SIN_DESC

    def test_insert_portafolio_returns_none_when_no_data(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_insert_portafolio_tecnico", None)

        repo = TecnicosRepository()
        result = repo.insert_portafolio(1, "Fallo", "url.jpg")

        assert result is None
