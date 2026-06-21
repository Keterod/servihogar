"""Tests for solicitudes cliente RPC migration — repository + service + API.

Verifies that the repository calls the correct RPC functions,
the service processes responses correctly, and API endpoints work.
"""

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from src.main import app

# ── Mock data matching RPC JSON output ────────────────────

FAKE_SOLICITUD_1 = {
    "id_solicitud": 1,
    "titulo": "Arreglar fuga de agua",
    "descripcion": "Tubería del baño principal gotea",
    "direccion_referencia": "Jr. Real 123",
    "estado": "pendiente",
    "fecha_publicacion": "2026-06-15T10:00:00",
    "categoria_nombre": "Gasfitería",
    "zona_nombre": "Huancayo Centro",
    "cotizaciones_count": 2,
}

FAKE_SOLICITUD_2 = {
    "id_solicitud": 2,
    "titulo": "Cambiar interruptor",
    "descripcion": "Interruptor de la sala no funciona",
    "direccion_referencia": "Av. Principal 456",
    "estado": "pendiente",
    "fecha_publicacion": "2026-06-14T15:30:00",
    "categoria_nombre": "Electricidad",
    "zona_nombre": "El Tambo",
    "cotizaciones_count": 0,
}

FAKE_LISTA = [FAKE_SOLICITUD_1, FAKE_SOLICITUD_2]

FAKE_SOLICITUD_DETALLE = {k: v for k, v in FAKE_SOLICITUD_1.items() if k != "cotizaciones_count"}


# ── Fixture (repository/service tests) ────────────────────

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

class TestSolicitudesRepositoryCliente:
    def test_get_by_cliente_id_calls_rpc(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_listar_solicitudes_cliente", FAKE_LISTA)

        repo = SolicitudesRepository()
        result = repo.get_by_cliente_id(1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_listar_solicitudes_cliente", {"p_id_cliente": 1}
        )
        assert result == FAKE_LISTA

    def test_get_by_cliente_id_empty(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_listar_solicitudes_cliente", [])

        repo = SolicitudesRepository()
        result = repo.get_by_cliente_id(99)

        assert result == []

    def test_get_by_cliente_id_none_data(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_listar_solicitudes_cliente", None)

        repo = SolicitudesRepository()
        result = repo.get_by_cliente_id(99)

        assert result == []

    def test_get_by_id_for_cliente_calls_rpc(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_get_solicitud_cliente_by_id", FAKE_SOLICITUD_DETALLE)

        repo = SolicitudesRepository()
        result = repo.get_by_id_for_cliente(1, 1)

        from src.repository.supabase_client import SupabaseClient
        SupabaseClient.get().rpc.assert_called_once_with(
            "rpc_get_solicitud_cliente_by_id",
            {"p_id_solicitud": 1, "p_id_cliente": 1},
        )
        assert result == FAKE_SOLICITUD_DETALLE

    def test_get_by_id_for_cliente_not_found(self, mock_supabase):
        from src.repository.solicitudes_repository import SolicitudesRepository

        mock_supabase("rpc_get_solicitud_cliente_by_id", None)

        repo = SolicitudesRepository()
        result = repo.get_by_id_for_cliente(999, 1)

        assert result is None


# ── Service tests ─────────────────────────────────────────

class TestSolicitudesServiceCliente:
    def test_obtener_por_cliente_id_maps_response(self, mock_supabase):
        from src.services.solicitudes_service import SolicitudesService

        mock_supabase("rpc_listar_solicitudes_cliente", FAKE_LISTA)

        service = SolicitudesService()
        result = service.obtener_por_cliente_id(1)

        assert len(result) == 2
        assert result[0].id_solicitud == 1
        assert result[0].titulo == "Arreglar fuga de agua"
        assert result[0].categoria_nombre == "Gasfitería"
        assert result[0].zona_nombre == "Huancayo Centro"
        assert result[0].cotizaciones_count == 2

    def test_obtener_por_cliente_id_empty(self, mock_supabase):
        from src.services.solicitudes_service import SolicitudesService

        mock_supabase("rpc_listar_solicitudes_cliente", [])

        service = SolicitudesService()
        result = service.obtener_por_cliente_id(99)

        assert result == []

    def test_obtener_por_cliente_maps_fields_correctly(self, mock_supabase):
        from src.services.solicitudes_service import SolicitudesService

        mock_supabase("rpc_listar_solicitudes_cliente", [
            {
                "id_solicitud": 5,
                "titulo": "Test",
                "descripcion": "Desc",
                "direccion_referencia": "Dir",
                "estado": "pendiente",
                "fecha_publicacion": "2026-06-15T10:00:00",
                "categoria_nombre": "Cat",
                "zona_nombre": "Zona",
                "cotizaciones_count": 3,
            }
        ])

        service = SolicitudesService()
        result = service.obtener_por_cliente_id(1)

        assert len(result) == 1
        item = result[0]
        assert item.id_solicitud == 5
        assert item.titulo == "Test"
        assert item.descripcion == "Desc"
        assert item.direccion == "Dir"
        assert item.estado == "pendiente"
        assert item.categoria_nombre == "Cat"
        assert item.zona_nombre == "Zona"
        assert item.cotizaciones_count == 3


# ── API endpoint tests ────────────────────────────────────

@pytest.fixture
def mock_demo_and_rpc():
    """Mock service layer for API tests.

    Mocks _service (the module-level singleton) so we don't
    need to wire up supabase client mocks through the entire
    call chain including get_demo_cliente_id().
    """
    with patch("src.apis.solicitudes._service") as mock_svc:
        yield mock_svc


class TestSolicitudesDemoEndpoint:
    def test_listar_solicitudes_demo_returns_list(self, mock_demo_and_rpc):
        mock_demo_and_rpc.obtener_por_cliente.return_value = [
            MagicMock(
                id_solicitud=1,
                titulo="Arreglar fuga de agua",
                descripcion="Tubería del baño principal gotea",
                direccion="Jr. Real 123",
                estado="pendiente",
                fecha_publicacion=datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc),
                categoria_nombre="Gasfitería",
                zona_nombre="Huancayo Centro",
                cotizaciones_count=2,
            ),
            MagicMock(
                id_solicitud=2,
                titulo="Cambiar interruptor",
                descripcion="Interruptor de la sala no funciona",
                direccion="Av. Principal 456",
                estado="pendiente",
                fecha_publicacion=datetime(2026, 6, 14, 15, 30, 0, tzinfo=timezone.utc),
                categoria_nombre="Electricidad",
                zona_nombre="El Tambo",
                cotizaciones_count=0,
            ),
        ]

        response = TestClient(app, raise_server_exceptions=False).get(
            "/clientes/demo/solicitudes"
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id_solicitud"] == 1
        assert data[0]["categoria_nombre"] == "Gasfitería"
        assert data[1]["cotizaciones_count"] == 0

    def test_listar_solicitudes_demo_empty(self, mock_demo_and_rpc):
        mock_demo_and_rpc.obtener_por_cliente.return_value = []

        response = TestClient(app, raise_server_exceptions=False).get(
            "/clientes/demo/solicitudes"
        )

        assert response.status_code == 200
        assert response.json() == []
