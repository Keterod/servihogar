from datetime import datetime

from pydantic import BaseModel


class AdminResumenResponse(BaseModel):
    total_usuarios: int
    total_clientes: int
    total_tecnicos: int
    total_solicitudes: int
    solicitudes_pendientes: int
    solicitudes_en_proceso: int
    solicitudes_finalizadas: int
    tecnicos_pendientes: int
    tecnicos_validados: int
    tecnicos_rechazados: int
    total_cotizaciones: int
    total_valoraciones: int


class TecnicoPendienteAdminResponse(BaseModel):
    id_tecnico: int
    nombres: str
    apellidos: str
    email: str | None = None
    telefono: str | None = None
    descripcion: str | None = None
    experiencia_anios: int
    fecha_registro: datetime
    estado_validacion: str
    categorias: list[str] = []
    zonas: list[str] = []


class TecnicoValidacionResponse(BaseModel):
    id_tecnico: int
    estado_validacion: str


class ReporteUsuarioItem(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    telefono: str | None = None
    estado: str
    fecha_registro: datetime
    rol: str


class ReporteSolicitudItem(BaseModel):
    id_solicitud: int
    titulo: str
    categoria: str
    zona: str
    cliente: str
    estado: str
    fecha_publicacion: datetime


class ReporteCotizacionItem(BaseModel):
    id_cotizacion: int
    solicitud: str
    tecnico: str
    monto: float
    estado: str
    fecha_envio: datetime


class ReporteFinalizadoItem(BaseModel):
    id_solicitud: int
    titulo: str
    cliente: str
    tecnico: str
    estado: str
    fecha_publicacion: datetime


class ReporteTecnicoActivoItem(BaseModel):
    id_tecnico: int
    nombres: str
    apellidos: str
    telefono: str | None = None
    experiencia_anios: int
    categorias: list[str] = []
    zonas: list[str] = []
    fecha_validacion: datetime | None = None
