from fastapi import FastAPI

from src.apis.health import router as health_router

app = FastAPI(title="ServiHogar API", version="0.1.0")

app.include_router(health_router)
