from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TipoUsuario(str, Enum):
    cliente = "cliente"
    tecnico = "tecnico"
    administrador = "administrador"


class AuthMeResponse(BaseModel):
    id_usuario: int
    auth_user_id: UUID
    nombres: str
    apellidos: str
    email: str
    tipo_usuario: TipoUsuario
    estado: str
    id_cliente: int | None = None
    id_tecnico: int | None = None
    id_administrador: int | None = None
    estado_validacion: str | None = None
