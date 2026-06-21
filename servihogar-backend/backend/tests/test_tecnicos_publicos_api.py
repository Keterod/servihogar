"""Tests for técnicos públicos RPC migration — API endpoints.

These are in a separate file to avoid mock state interference
from the repository/service-level tests.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app, raise_server_exceptions=False)

# ── Must match test_tecnicos_publicos.py ───────────────────

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

        def _setup(return_data):
            mock_client.rpc = MagicMock()
            mock_client.rpc.return_value = MagicMock()
            mock_result = MagicMock()
            mock_result.data = return_data
            mock_exec.return_value = mock_result

        yield _setup


# ── API endpoint tests ─────────────────────────────────────

class TestTecnicosEndpoint:
    def test_get_tecnicos_returns_list(self, mock_supabase):
        mock_supabase(FAKE_LISTA)

        response = client.get("/tecnicos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id_tecnico"] == 1
        assert data[0]["nombres"] == "Juan"
        assert data[0]["calificacion"] == 4.5
        assert len(data[0]["categorias"]) == 1

    def test_get_tecnicos_empty(self, mock_supabase):
        mock_supabase([])

        response = client.get("/tecnicos")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_tecnico_by_id_returns_detail(self, mock_supabase):
        mock_supabase(FAKE_TECNICO_DETAIL)

        response = client.get("/tecnicos/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id_tecnico"] == 1
        assert data["calificacion"] == 4.5
        assert len(data["portafolio"]) == 2
        assert data["portafolio"][0]["titulo"] == "Reparación de caño"

    def test_get_tecnico_not_found(self, mock_supabase):
        mock_supabase(None)

        response = client.get("/tecnicos/999")
        assert response.status_code == 404

    def test_tecnico_sin_calificacion(self, mock_supabase):
        mock_supabase({**FAKE_TECNICO_2, "portafolio": []})

        response = client.get("/tecnicos/2")
        assert response.status_code == 200
        assert response.json()["calificacion"] is None
