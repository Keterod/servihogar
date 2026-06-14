from pydantic import BaseModel


class ZonaResponse(BaseModel):
    id_zona: int
    nombre: str
    id_ciudad: int
