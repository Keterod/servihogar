from pydantic import BaseModel


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: str | None = None
