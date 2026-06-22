"""Tests for solicitudes técnico RPC migration — repository + service.

Verifies the repository calls the correct RPC functions
and the service processes responses correctly.
"""

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from src.main import app


FAKE_DISPONIBLE = {
    "id_solicitud": 1,
    "titulo": "Arreglar fuga de agua",
    "descripcion": "Tubería del baño gotea",
    "direccion_referencia": "Jr. Real 123",
    "estado": "pendiente",
    "fecha_publicacion": "2026-06-15T10:00:00",
    "categoria_nombre": "Gasfitería",
    "zona_nombre": "Huancayo Centro",
    "cliente_nombre": "Ana Torres",
    "cotizaciones_count": 2,
    "ya_cotizada_por_tecnico": False,
}

FAKE_DISPONIBLE_COTIZADA = {**FAKE_DISPONIBLE, "id_solicitud": 2, "ya_cotizada_por_tecnico": True}

FAKE_LISTA_DISPONIBLES = [FAKE_DISPONIBLE, FAKE_DISPONIBLE_COTIZADA]

FAKE_ACEPTADO = {
    "id_solicitud": 3,
    "titulo": "Instalación eléctrica",
    "descripcion": "Cambiar cableado",
    "direccion_referencia": "Av. Principal 456",
    "estado": "en_proceso",
    "fecha_publicacion": "2026-06-14T15:30:00",
    "categoria_nombre": "Electricidad",
    "zona_nombre": "El Tambo",
    "cliente_nombre": "Carlos López",
    "id_cotizacion": 10,
    "precio": 250.00,
    "tiempo_estimado": "3 días",
    "estado_cotizacion": "aceptada",
}

FAKE_LISTA_ACEPTADOS = [FAKE_ACEPTADO]


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

class TestSolicitudesTecnicoRepository:
    def test_disponibles_calls_rpc(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_solicitudes_disponibles_tecnico", FAKE_LISTA_DISPONIBLES)

        repo = SolicitudesRepository()
        result = repo.get_disponibles_for_tecnico(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_solicitudes_disponibles_tecnico", {"p_id_tecnico": 1}
        )
        assert result == FAKE_LISTA_DISPONIBLES
        assert len(result) == 2
        assert result[0]["ya_cotizada_por_tecnico"] is False
        assert result[1]["ya_cotizada_por_tecnico"] is True

    def test_disponibles_empty(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_solicitudes_disponibles_tecnico", [])

        repo = SolicitudesRepository()
        result = repo.get_disponibles_for_tecnico(99)

        assert result == []

    def test_disponibles_none_data(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_solicitudes_disponibles_tecnico", None)

        repo = SolicitudesRepository()
        result = repo.get_disponibles_for_tecnico(99)

        assert result == []

    def test_aceptados_calls_rpc(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_servicios_aceptados_tecnico", FAKE_LISTA_ACEPTADOS)

        repo = SolicitudesRepository()
        result = repo.get_servicios_aceptados_for_tecnico(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_servicios_aceptados_tecnico", {"p_id_tecnico": 1}
        )
        assert result == FAKE_LISTA_ACEPTADOS
        assert len(result) == 1
        assert result[0]["id_cotizacion"] == 10
        assert result[0]["precio"] == 250.00

    def test_aceptados_empty(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_servicios_aceptados_tecnico", [])

        repo = SolicitudesRepository()
        result = repo.get_servicios_aceptados_for_tecnico(99)

        assert result == []


# ── Service tests ─────────────────────────────────────────

class TestSolicitudesTecnicoService:
    def test_disponibles_maps_response(self, mock_supabase):
        from src.services.solicitudes_service import SolicitudesService

        mock_supabase("rpc_solicitudes_disponibles_tecnico", FAKE_LISTA_DISPONIBLES)

        service = SolicitudesService()
        result = service.obtener_solicitudes_disponibles_para_tecnico(1)

        assert len(result) == 2
        assert result[0].id_solicitud == 1
        assert result[0].categoria_nombre == "Gasfitería"
        assert result[0].cliente_nombre == "Ana Torres"
        assert result[0].ya_cotizada_por_tecnico is False
        assert result[1].ya_cotizada_por_tecnico is True

    def test_disponibles_empty(self, mock_supabase):
        from src.services.solicitudes_service import SolicitudesService

        mock_supabase("rpc_solicitudes_disponibles_tecnico", [])

        service = SolicitudesService()
        result = service.obtener_solicitudes_disponibles_para_tecnico(99)

        assert result == []

    def test_aceptados_maps_response(self, mock_supabase):
        from src.services.solicitudes_service import SolicitudesService

        mock_supabase("rpc_servicios_aceptados_tecnico", FAKE_LISTA_ACEPTADOS)

        service = SolicitudesService()
        result = service.obtener_servicios_aceptados_para_tecnico(1)

        assert len(result) == 1
        assert result[0].id_solicitud == 3
        assert result[0].categoria_nombre == "Electricidad"
        assert result[0].precio == 250.00
        assert result[0].estado_cotizacion == "aceptada"
