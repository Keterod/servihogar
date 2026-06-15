from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class TipoUsuario(str, Enum):
    cliente = "cliente"
    tecnico = "tecnico"
    administrador = "administrador"


class AuthRegisterRequest(BaseModel):
    nombres: str = Field(min_length=1, max_length=100)
    apellidos: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=6, max_length=128)
    tipo_usuario: TipoUsuario
    telefono: str | None = Field(default=None, max_length=20)
    descripcion: str | None = None
    experiencia_anios: int | None = Field(default=None, ge=0)
    id_categorias: list[int] = Field(default_factory=list)
    id_zonas: list[int] = Field(default_factory=list)

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("Correo electrónico inválido")
        return email

    @field_validator("tipo_usuario")
    @classmethod
    def solo_cliente_o_tecnico(cls, value: TipoUsuario) -> TipoUsuario:
        if value == TipoUsuario.administrador:
            raise ValueError("No se puede registrar un administrador por este endpoint")
        return value

    @model_validator(mode="after")
    def validar_campos_tecnico(self) -> "AuthRegisterRequest":
        if self.tipo_usuario != TipoUsuario.tecnico:
            return self

        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripción es obligatoria para técnicos")

        if self.experiencia_anios is None:
            raise ValueError("Los años de experiencia son obligatorios para técnicos")

        return self


class AuthRegisterResponse(BaseModel):
    id_usuario: int
    auth_user_id: UUID
    email: str
    tipo_usuario: TipoUsuario
    id_cliente: int | None = None
    id_tecnico: int | None = None
    estado_validacion: str | None = None
    mensaje: str


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
