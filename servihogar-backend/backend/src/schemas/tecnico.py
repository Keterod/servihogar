from pydantic import BaseModel


class TecnicoResponse(BaseModel):
    id_tecnico: int
    nombres: str
    apellidos: str
    descripcion: str | None = None
    experiencia_anios: int
    calificacion: float | None = None
