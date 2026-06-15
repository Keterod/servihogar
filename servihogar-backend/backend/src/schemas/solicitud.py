from datetime import datetime

from pydantic import BaseModel, Field


class SolicitudRequest(BaseModel):
    id_categoria: int
    id_zona: int
    titulo: str = Field(max_length=150)
    descripcion: str
    direccion_referencia: str | None = None
    id_tecnico: int | None = None


class SolicitudResponse(BaseModel):
    id_solicitud: int
    id_cliente: int
    estado: str
    fecha_publicacion: datetime


class SolicitudListResponse(BaseModel):
    id_solicitud: int
    titulo: str
    descripcion: str
    direccion: str | None = None
    estado: str
    fecha_publicacion: datetime
    categoria_nombre: str
    zona_nombre: str
    cotizaciones_count: int = 0
