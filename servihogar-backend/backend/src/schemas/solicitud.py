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
