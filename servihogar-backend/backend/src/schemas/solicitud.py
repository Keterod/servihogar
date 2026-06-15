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


class SolicitudDisponibleResponse(BaseModel):
    id_solicitud: int
    titulo: str
    descripcion: str
    direccion: str | None = None
    estado: str
    fecha_publicacion: datetime
    categoria_nombre: str
    zona_nombre: str
    cliente_nombre: str | None = None
    cotizaciones_count: int = 0
    ya_cotizada_por_tecnico: bool = False


class CotizacionDetalleResponse(BaseModel):
    id_cotizacion: int
    id_tecnico: int
    tecnico_nombre: str
    tecnico_descripcion: str | None = None
    precio: float
    tiempo_estimado: str | None = None
    descripcion_propuesta: str
    estado: str
    fecha_creacion: datetime


class SolicitudDetalleResponse(BaseModel):
    id_solicitud: int
    titulo: str
    descripcion: str
    direccion: str | None = None
    estado: str
    fecha_publicacion: datetime
    categoria_nombre: str
    zona_nombre: str
    cotizaciones: list[CotizacionDetalleResponse] = []
