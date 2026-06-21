"""Tests for técnicos públicos RPC migration — repository + service.

Verifies that the repository calls the correct RPC functions
and the service processes the response correctly.
"""

from unittest.mock import MagicMock, patch

import pytest

# ── Mock data matching RPC JSON output ────────────────────

FAKE_TECNICO_1 = {
    "id_tecnico": 1,
    "descripcion": "Experto en gasfitería",
    "experiencia_anios": 5,
    "usuarios": {"id_usuario": 10, "nombres": "Juan", "apellidos": "Pérez"},
    "tecnico_categorias": [
        {"categorias_servicio": {"id_categoria": 2, "nombre": "Gasfitería menor"}},
    ],
    "tecnico_zonas": [
        {"zonas": {"id_zona": 1, "nombre": "Huancayo Centro"}},
        {"zonas": {"id_zona": 2, "nombre": "El Tambo"}},
    ],
    "calificacion": 4.5,
}

FAKE_TECNICO_2 = {
    "id_tecnico": 2,
    "descripcion": "Electricista certificado",
    "experiencia_anios": 8,
    "usuarios": {"id_usuario": 11, "nombres": "María", "apellidos": "López"},
    "tecnico_categorias": [
        {"categorias_servicio": {"id_categoria": 1, "nombre": "Electricidad básica"}},
        {"categorias_servicio": {"id_categoria": 3, "nombre": "Instalaciones"}},
    ],
    "tecnico_zonas": [
        {"zonas": {"id_zona": 1, "nombre": "Huancayo Centro"}},
    ],
    "calificacion": None,
}

FAKE_TECNICO_DETAIL = {
    **FAKE_TECNICO_1,
    "portafolio": [
        {
            "id_portafolio": 1,
            "titulo": "Reparación de caño",
            "descripcion": "Antes y después",
            "imagen_url": "tecnicos/1/portafolio/foto1.jpg",
        },
        {
            "id_portafolio": 2,
            "titulo": "Instalación de lavatorio",
            "descripcion": None,
            "imagen_url": "tecnicos/1/portafolio/foto2.jpg",
        },
    ],
}

FAKE_LISTA = [FAKE_TECNICO_1, FAKE_TECNICO_2]


# ── Fixture ────────────────────────────────────────────────

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


# ── Repository tests ───────────────────────────────────────

class TestTecnicosRepositoryPublicos:
    def test_get_all_calls_rpc(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_listar_tecnicos_publicos", FAKE_LISTA)

        repo = TecnicosRepository()
        result = repo.get_all()

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with("rpc_listar_tecnicos_publicos")
        assert result == FAKE_LISTA

    def test_get_all_empty(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_listar_tecnicos_publicos", [])

        repo = TecnicosRepository()
        result = repo.get_all()
        assert result == []

    def test_get_all_none(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_listar_tecnicos_publicos", None)

        repo = TecnicosRepository()
        result = repo.get_all()
        assert result is None

    def test_get_by_id_calls_rpc(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_get_tecnico_publico_by_id", FAKE_TECNICO_DETAIL)

        repo = TecnicosRepository()
        result = repo.get_by_id(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_get_tecnico_publico_by_id", {"p_id_tecnico": 1}
        )
        assert result == FAKE_TECNICO_DETAIL

    def test_get_by_id_not_found(self, mock_supabase):
        from src.repository.tecnicos_repository import TecnicosRepository

        mock_supabase("rpc_get_tecnico_publico_by_id", None)

        repo = TecnicosRepository()
        result = repo.get_by_id(999)
        assert result is None


# ── Service tests ──────────────────────────────────────────

class TestTecnicosServicePublicos:
    def test_obtener_todos(self, mock_supabase):
        from src.services.tecnicos_service import TecnicosService

        mock_supabase("rpc_listar_tecnicos_publicos", FAKE_LISTA)

        service = TecnicosService()
        result = service.obtener_todos()

        assert len(result) == 2
        t1 = result[0]
        assert t1.id_tecnico == 1
        assert t1.nombres == "Juan"
        assert t1.calificacion == 4.5
        assert len(t1.categorias) == 1
        assert t1.categorias[0].nombre == "Gasfitería menor"
        assert len(t1.zonas) == 2

        t2 = result[1]
        assert t2.id_tecnico == 2
        assert t2.calificacion is None

    def test_obtener_por_id(self, mock_supabase):
        from src.services.tecnicos_service import TecnicosService

        mock_supabase("rpc_get_tecnico_publico_by_id", FAKE_TECNICO_DETAIL)

        service = TecnicosService()
        result = service.obtener_por_id(1)

        assert result is not None
        assert result.id_tecnico == 1
        assert result.calificacion == 4.5
        assert len(result.portafolio) == 2
        assert result.portafolio[0].titulo == "Reparación de caño"

    def test_obtener_por_id_not_found(self, mock_supabase):
        from src.services.tecnicos_service import TecnicosService

        mock_supabase("rpc_get_tecnico_publico_by_id", None)

        service = TecnicosService()
        result = service.obtener_por_id(999)
        assert result is None
