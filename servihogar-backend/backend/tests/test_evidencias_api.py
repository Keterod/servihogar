from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.schemas.auth import AuthMeResponse, TipoUsuario
from src.schemas.solicitud import ImagenSolicitudResponse
from src.schemas.tecnico import PortafolioItemResponse
from src.services.solicitudes_service import ImagenError, SolicitudesService
from src.services.tecnicos_service import PortafolioError, TecnicosService

client = TestClient(app, raise_server_exceptions=False)

PRODUCTION_ORIGIN = "https://servihogar-frontend.onrender.com"

CLIENTE = AuthMeResponse(
    id_usuario=1,
    auth_user_id=UUID("11111111-1111-1111-1111-111111111111"),
    nombres="Ana",
    apellidos="Cliente",
    email="ana@test.com",
    tipo_usuario=TipoUsuario.cliente,
    estado="activo",
    id_cliente=10,
    id_tecnico=None,
    id_administrador=None,
    estado_validacion=None,
)

TECNICO = AuthMeResponse(
    id_usuario=2,
    auth_user_id=UUID("22222222-2222-2222-2222-222222222222"),
    nombres="Carlos",
    apellidos="Tecnico",
    email="carlos@test.com",
    tipo_usuario=TipoUsuario.tecnico,
    estado="activo",
    id_cliente=None,
    id_tecnico=20,
    id_administrador=None,
    estado_validacion="validado",
)

NOW = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)


def test_post_imagen_solicitud_sin_auth_retorna_401():
    response = client.post(
        "/solicitudes/1/imagenes",
        json={"imagen_url": "solicitudes/1/test.jpg"},
    )
    assert response.status_code == 401


def test_get_imagenes_solicitud_sin_auth_retorna_401():
    response = client.get("/solicitudes/1/imagenes")
    assert response.status_code == 401


@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_post_imagen_solicitud_usuario_tecnico_retorna_403(mock_auth):
    mock_auth.return_value = TECNICO
    response = client.post(
        "/solicitudes/1/imagenes",
        json={"imagen_url": "solicitudes/1/test.jpg"},
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 403


@patch("src.apis.solicitudes._service")
@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_post_imagen_solicitud_cliente_retorna_201(mock_auth, mock_service):
    mock_auth.return_value = CLIENTE
    mock_service.registrar_imagen.return_value = ImagenSolicitudResponse(
        id_imagen=1,
        imagen_url="solicitudes/1/123-foto.jpg",
        descripcion=None,
        fecha_subida=NOW,
    )

    response = client.post(
        "/solicitudes/1/imagenes",
        json={"imagen_url": "solicitudes/1/123-foto.jpg"},
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 201
    assert response.json()["imagen_url"] == "solicitudes/1/123-foto.jpg"


@patch("src.apis.solicitudes._service")
@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_get_imagenes_solicitud_sin_acceso_retorna_403(mock_auth, mock_service):
    mock_auth.return_value = CLIENTE
    mock_service.verificar_acceso_detalle.return_value = "forbidden"

    response = client.get(
        "/solicitudes/99/imagenes",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 403


@patch("src.apis.solicitudes._service")
@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_get_imagenes_solicitud_con_acceso_retorna_200(mock_auth, mock_service):
    mock_auth.return_value = CLIENTE
    mock_service.verificar_acceso_detalle.return_value = "ok"
    mock_service.listar_imagenes.return_value = [
        ImagenSolicitudResponse(
            id_imagen=1,
            imagen_url="solicitudes/1/foto.jpg",
            descripcion=None,
            fecha_subida=NOW,
        )
    ]

    response = client.get(
        "/solicitudes/1/imagenes",
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_mi_portafolio_sin_auth_retorna_401():
    response = client.get("/tecnicos/me/portafolio")
    assert response.status_code == 401


@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_get_mi_portafolio_cliente_retorna_403(mock_auth):
    mock_auth.return_value = CLIENTE
    response = client.get(
        "/tecnicos/me/portafolio",
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 403


@patch("src.apis.tecnicos._service")
@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_post_mi_portafolio_tecnico_retorna_201(mock_auth, mock_service):
    mock_auth.return_value = TECNICO
    mock_service.agregar_portafolio.return_value = PortafolioItemResponse(
        id_portafolio=1,
        titulo="Trabajo demo",
        descripcion=None,
        imagen_url="tecnicos/20/portafolio/123-foto.jpg",
        storage_path="tecnicos/20/portafolio/123-foto.jpg",
        estado="visible",
        fecha_subida=NOW,
    )

    response = client.post(
        "/tecnicos/me/portafolio",
        json={
            "titulo": "Trabajo demo",
            "imagen_url": "tecnicos/20/portafolio/123-foto.jpg",
        },
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 201
    assert response.json()["titulo"] == "Trabajo demo"


def test_registrar_imagen_valida_path_prefix():
    service = SolicitudesService()
    service._repo = MagicMock()
    service._imagenes_repo = MagicMock()
    service._repo.get_solicitud_by_id.return_value = {"id_cliente": 10}

    with pytest.raises(ImagenError) as exc:
        service.registrar_imagen(
            1,
            10,
            MagicMock(imagen_url="otro/path.jpg", descripcion=None),
        )
    assert exc.value.code == "validation"


def test_agregar_portafolio_valida_path_prefix():
    service = TecnicosService()
    service._repo = MagicMock()

    with pytest.raises(PortafolioError) as exc:
        service.agregar_portafolio(
            20,
            MagicMock(
                titulo="Test",
                imagen_url="solicitudes/1/foto.jpg",
                descripcion=None,
            ),
        )
    assert exc.value.code == "validation"


def test_options_imagenes_incluye_cors():
    response = client.options(
        "/solicitudes/1/imagenes",
        headers={
            "Origin": PRODUCTION_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == PRODUCTION_ORIGIN
    assert "POST" in (response.headers.get("access-control-allow-methods") or "")
    assert "authorization" in (response.headers.get("access-control-allow-headers") or "").lower()


@patch("src.apis.solicitudes._service")
@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_post_imagen_error_interno_incluye_cors(mock_auth, mock_service):
    mock_auth.return_value = CLIENTE
    mock_service.registrar_imagen.side_effect = RuntimeError("boom")

    response = client.post(
        "/solicitudes/1/imagenes",
        json={"imagen_url": "solicitudes/1/foto.jpg"},
        headers={
            "Authorization": "Bearer token",
            "Origin": PRODUCTION_ORIGIN,
        },
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo registrar la imagen"}
    assert response.headers.get("access-control-allow-origin") == PRODUCTION_ORIGIN


@patch("src.apis.tecnicos._service")
@patch("src.apis.deps._auth_service.obtener_usuario_actual")
def test_post_portafolio_error_interno_incluye_cors(mock_auth, mock_service):
    mock_auth.return_value = TECNICO
    mock_service.agregar_portafolio.side_effect = RuntimeError("boom")

    response = client.post(
        "/tecnicos/me/portafolio",
        json={
            "titulo": "Trabajo demo",
            "imagen_url": "tecnicos/20/portafolio/foto.jpg",
        },
        headers={
            "Authorization": "Bearer token",
            "Origin": PRODUCTION_ORIGIN,
        },
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo guardar el ítem de portafolio"}
    assert response.headers.get("access-control-allow-origin") == PRODUCTION_ORIGIN


def test_options_portafolio_incluye_cors():
    response = client.options(
        "/tecnicos/me/portafolio",
        headers={
            "Origin": PRODUCTION_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == PRODUCTION_ORIGIN
