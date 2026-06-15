from pydantic import BaseModel


class TecnicoCategoriaRef(BaseModel):
    id_categoria: int
    nombre: str


class TecnicoZonaRef(BaseModel):
    id_zona: int
    nombre: str


class TecnicoResponse(BaseModel):
    id_tecnico: int
    nombres: str
    apellidos: str
    descripcion: str | None = None
    experiencia_anios: int
    calificacion: float | None = None
    categorias: list[TecnicoCategoriaRef] = []
    zonas: list[TecnicoZonaRef] = []
