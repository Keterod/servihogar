from pydantic import BaseModel


class CategoriaServicioResponse(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: str | None = None


class ZonaResponse(BaseModel):
    id_zona: int
    nombre: str
    id_ciudad: int
