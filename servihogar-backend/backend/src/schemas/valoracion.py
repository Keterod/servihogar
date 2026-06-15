from datetime import datetime

from pydantic import BaseModel, Field


class ValoracionRequest(BaseModel):
    id_solicitud: int
    calificacion: int = Field(ge=1, le=5)
    comentario: str | None = None
    puntualidad: int | None = Field(default=None, ge=1, le=5)
    calidad: int | None = Field(default=None, ge=1, le=5)
    trato: int | None = Field(default=None, ge=1, le=5)
    precio: int | None = Field(default=None, ge=1, le=5)


class ValoracionResponse(BaseModel):
    id_valoracion: int
    id_cotizacion: int
    id_solicitud: int
    puntuacion: int
    comentario: str | None = None
    puntualidad: int | None = None
    calidad: int | None = None
    precio: int | None = None
    trato: int | None = None
    fecha_valoracion: datetime
    solicitud_estado: str
