import importlib

import pytest
from fastapi.testclient import TestClient

from src.core.config import Settings, normalize_cors_origin

PRODUCTION_ORIGIN = "https://servihogar-frontend.onrender.com"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (PRODUCTION_ORIGIN, PRODUCTION_ORIGIN),
        (f"{PRODUCTION_ORIGIN}/", PRODUCTION_ORIGIN),
        (f'"{PRODUCTION_ORIGIN}"', PRODUCTION_ORIGIN),
        (f"'{PRODUCTION_ORIGIN}'", PRODUCTION_ORIGIN),
        (f"  {PRODUCTION_ORIGIN}  ", PRODUCTION_ORIGIN),
    ],
)
def test_normalize_cors_origin(raw: str, expected: str) -> None:
    assert normalize_cors_origin(raw) == expected


def test_get_cors_origins_single_production_url() -> None:
    settings = Settings(CORS_ORIGINS=PRODUCTION_ORIGIN)
    assert settings.get_cors_origins() == [PRODUCTION_ORIGIN]


def test_get_cors_origins_comma_separated() -> None:
    settings = Settings(
        CORS_ORIGINS=f"{PRODUCTION_ORIGIN}/, https://preview.example.com/"
    )
    assert settings.get_cors_origins() == [
        PRODUCTION_ORIGIN,
        "https://preview.example.com",
    ]


def test_get_cors_origins_default_is_production_only() -> None:
    settings = Settings()
    assert settings.get_cors_origins() == [PRODUCTION_ORIGIN]


def test_cors_preflight_returns_allow_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", PRODUCTION_ORIGIN)

    import src.core.config as config_module
    import src.main as main_module

    importlib.reload(config_module)
    importlib.reload(main_module)

    client = TestClient(main_module.app)
    response = client.options(
        "/health",
        headers={
            "Origin": PRODUCTION_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.headers.get("access-control-allow-origin") == PRODUCTION_ORIGIN
    assert "access-control-allow-credentials" not in response.headers


def test_cors_get_returns_allow_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", PRODUCTION_ORIGIN)

    import src.core.config as config_module
    import src.main as main_module

    importlib.reload(config_module)
    importlib.reload(main_module)

    client = TestClient(main_module.app)
    response = client.get("/health", headers={"Origin": PRODUCTION_ORIGIN})

    assert response.headers.get("access-control-allow-origin") == PRODUCTION_ORIGIN


def test_cors_rejects_unknown_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", PRODUCTION_ORIGIN)

    import src.core.config as config_module
    import src.main as main_module

    importlib.reload(config_module)
    importlib.reload(main_module)

    client = TestClient(main_module.app)
    response = client.get("/health", headers={"Origin": "https://evil.example.com"})

    assert "access-control-allow-origin" not in response.headers
