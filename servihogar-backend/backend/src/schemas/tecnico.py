from datetime import datetime

from pydantic import BaseModel, Field


class TecnicoCategoriaRef(BaseModel):
    id_categoria: int
    nombre: str


class TecnicoZonaRef(BaseModel):
    id_zona: int
    nombre: str


class PortafolioItem(BaseModel):
    id_portafolio: int
    titulo: str
    descripcion: str | None = None
    imagen_url: str
    storage_path: str | None = None


class PortafolioCreateRequest(BaseModel):
    titulo: str = Field(max_length=150)
    imagen_url: str
    descripcion: str | None = None


class PortafolioItemResponse(BaseModel):
    id_portafolio: int
    titulo: str
    descripcion: str | None = None
    imagen_url: str
    storage_path: str | None = None
    estado: str
    fecha_subida: datetime


class TecnicoResponse(BaseModel):
    id_tecnico: int
    nombres: str
    apellidos: str
    descripcion: str | None = None
    experiencia_anios: int
    calificacion: float | None = None
    categorias: list[TecnicoCategoriaRef] = []
    zonas: list[TecnicoZonaRef] = []


class TecnicoDetalleResponse(TecnicoResponse):
    portafolio: list[PortafolioItem] = []
