from datetime import datetime

from pydantic import BaseModel, Field


class CotizacionRequest(BaseModel):
    id_solicitud: int
    precio: float = Field(gt=0)
    tiempo_estimado: str = Field(min_length=1, max_length=100)
    descripcion_propuesta: str = Field(min_length=1)


class CotizacionResponse(BaseModel):
    id_cotizacion: int
    id_solicitud: int
    id_tecnico: int
    precio: float
    tiempo_estimado: str | None = None
    descripcion_propuesta: str
    estado: str
    fecha_creacion: datetime


class CotizacionActionResponse(BaseModel):
    id_cotizacion: int
    id_solicitud: int
    precio: float
    tiempo_estimado: str | None = None
    descripcion_propuesta: str
    estado: str
    fecha_creacion: datetime
    solicitud_estado: str
