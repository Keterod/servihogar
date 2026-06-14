from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from supabase._sync.client import SupabaseException

from src.apis.categorias import router as categorias_router
from src.apis.health import router as health_router
from src.apis.tecnicos import router as tecnicos_router
from src.apis.zonas import router as zonas_router

app = FastAPI(title="ServiHogar API", version="0.1.0")


@app.exception_handler(SupabaseException)
async def supabase_exception_handler(_request: Request, exc: SupabaseException):
    return JSONResponse(status_code=503, content={"detail": str(exc)})


app.include_router(health_router)
app.include_router(categorias_router)
app.include_router(zonas_router)
app.include_router(tecnicos_router)
