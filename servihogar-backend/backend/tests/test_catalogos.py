"""Tests for categorías and zonas RPC migration.

Verifies that repositories call the correct RPC functions and
that the API endpoints return expected data through the service layer.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app, raise_server_exceptions=False)


# ── Mock data ──────────────────────────────────────────────

FAKE_CATEGORIAS = [
    {"id_categoria": 1, "nombre": "Electricidad básica", "descripcion": "Trabajos eléctricos simples", "estado": "activo", "fecha_creacion": "2025-01-01T00:00:00+00:00"},
    {"id_categoria": 2, "nombre": "Gasfitería menor", "descripcion": "Reparación de tuberías", "estado": "activo", "fecha_creacion": "2025-01-01T00:00:00+00:00"},
]

FAKE_ZONAS = [
    {"id_zona": 1, "id_ciudad": 1, "nombre": "Huancayo Centro", "estado": "activo"},
    {"id_zona": 2, "id_ciudad": 1, "nombre": "El Tambo", "estado": "activo"},
]


# ── Fixtures ───────────────────────────────────────────────

@pytest.fixture
def mock_supabase():
    """Mock SupabaseClient.get() and execute() to return fake data."""
    with patch("src.repository.supabase_client.SupabaseClient.get") as mock_get, \
         patch("src.repository.supabase_client.SupabaseClient.execute") as mock_exec:
        mock_client = MagicMock()
        mock_get.return_value = mock_client

        def _setup_rpc(name: str, return_data: list):
            rpc_builder = MagicMock()
            mock_client.rpc.return_value = rpc_builder
            mock_result = MagicMock()
            mock_result.data = return_data
            mock_exec.return_value = mock_result

        yield _setup_rpc


# ── Repository tests ───────────────────────────────────────

class TestCategoriasRepository:
    def test_calls_rpc_listar_categorias(self, mock_supabase):
        from src.repository.categorias_repository import CategoriasRepository

        mock_supabase("rpc_listar_categorias", FAKE_CATEGORIAS)

        repo = CategoriasRepository()
        result = repo.get_all()

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with("rpc_listar_categorias")
        assert result == FAKE_CATEGORIAS

    def test_returns_none_when_no_data(self, mock_supabase):
        from src.repository.categorias_repository import CategoriasRepository

        mock_supabase("rpc_listar_categorias", [])

        repo = CategoriasRepository()
        result = repo.get_all()
        assert result == []


class TestZonasRepository:
    def test_calls_rpc_listar_zonas(self, mock_supabase):
        from src.repository.zonas_repository import ZonasRepository

        mock_supabase("rpc_listar_zonas", FAKE_ZONAS)

        repo = ZonasRepository()
        result = repo.get_all()

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with("rpc_listar_zonas")
        assert result == FAKE_ZONAS

    def test_returns_none_when_no_data(self, mock_supabase):
        from src.repository.zonas_repository import ZonasRepository

        mock_supabase("rpc_listar_zonas", [])

        repo = ZonasRepository()
        result = repo.get_all()
        assert result == []


class TestCatalogoRepository:
    def test_list_categorias_calls_rpc(self, mock_supabase):
        from src.repository.catalogo_repository import CatalogoRepository

        mock_supabase("rpc_listar_categorias", FAKE_CATEGORIAS)

        repo = CatalogoRepository()
        result = repo.list_categorias()

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with("rpc_listar_categorias")
        assert result == FAKE_CATEGORIAS

    def test_list_zonas_calls_rpc(self, mock_supabase):
        from src.repository.catalogo_repository import CatalogoRepository

        mock_supabase("rpc_listar_zonas", FAKE_ZONAS)

        repo = CatalogoRepository()
        result = repo.list_zonas()

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with("rpc_listar_zonas")
        assert result == FAKE_ZONAS

    def test_list_categorias_returns_empty_list_when_no_data(self, mock_supabase):
        from src.repository.catalogo_repository import CatalogoRepository

        mock_supabase("rpc_listar_categorias", [])

        repo = CatalogoRepository()
        result = repo.list_categorias()
        assert result == []

    def test_list_zonas_returns_empty_list_when_none(self, mock_supabase):
        from src.repository.catalogo_repository import CatalogoRepository

        mock_supabase("rpc_listar_zonas", None)

        repo = CatalogoRepository()
        result = repo.list_zonas()
        assert result == []


# ── API endpoint integration tests ────────────────────────

class TestCategoriasEndpoint:
    def test_get_categorias_returns_list(self, mock_supabase):
        mock_supabase("rpc_listar_categorias", FAKE_CATEGORIAS)

        response = client.get("/categorias")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id_categoria"] == 1
        assert data[0]["nombre"] == "Electricidad básica"

    def test_get_categorias_empty(self, mock_supabase):
        mock_supabase("rpc_listar_categorias", [])

        response = client.get("/categorias")
        assert response.status_code == 200
        assert response.json() == []


class TestZonasEndpoint:
    def test_get_zonas_returns_list(self, mock_supabase):
        mock_supabase("rpc_listar_zonas", FAKE_ZONAS)

        response = client.get("/zonas")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id_zona"] == 1
        assert data[0]["nombre"] == "Huancayo Centro"

    def test_get_zonas_empty(self, mock_supabase):
        mock_supabase("rpc_listar_zonas", [])

        response = client.get("/zonas")
        assert response.status_code == 200
        assert response.json() == []
