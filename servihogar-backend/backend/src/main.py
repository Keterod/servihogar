import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from supabase._sync.client import SupabaseException

logger = logging.getLogger(__name__)

from src.apis.admin import router as admin_router
from src.apis.auth import router as auth_router
from src.apis.categorias import router as categorias_router
from src.apis.cotizaciones import router as cotizaciones_router
from src.apis.health import router as health_router
from src.apis.solicitudes import router as solicitudes_router
from src.apis.tecnicos import router as tecnicos_router
from src.apis.valoraciones import router as valoraciones_router
from src.apis.zonas import router as zonas_router

app = FastAPI(title="ServiHogar API", version="0.1.0")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

ALLOWED_ORIGINS = [
    "http://localhost:4300",
    "http://127.0.0.1:4300",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

ALLOWED_METHODS = ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]

ALLOWED_HEADERS = ["Authorization", "Content-Type"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


@app.exception_handler(SupabaseException)
async def supabase_exception_handler(request: Request, exc: SupabaseException):
    logger.exception("SupabaseException no capturada en %s", request.url.path)
    detail = str(exc)
    status_code = 422 if "query failed" in detail.lower() else 503
    return JSONResponse(status_code=status_code, content={"detail": detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Excepción no capturada en %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"},
    )


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(zonas_router)
app.include_router(tecnicos_router)
app.include_router(solicitudes_router)
app.include_router(cotizaciones_router)
app.include_router(valoraciones_router)
app.include_router(admin_router)
