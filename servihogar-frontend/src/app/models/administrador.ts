import { Usuario } from './usuario';

export interface Administrador extends Usuario {}

export interface AdminResumen {
  total_usuarios: number;
  total_clientes: number;
  total_tecnicos: number;
  total_solicitudes: number;
  solicitudes_pendientes: number;
  solicitudes_en_proceso: number;
  solicitudes_finalizadas: number;
  tecnicos_pendientes: number;
  tecnicos_validados: number;
  tecnicos_rechazados: number;
  total_cotizaciones: number;
  total_valoraciones: number;
}

export interface TecnicoPendienteAdmin {
  id_tecnico: number;
  nombres: string;
  apellidos: string;
  email: string | null;
  telefono: string | null;
  descripcion: string | null;
  experiencia_anios: number;
  fecha_registro: string;
  estado_validacion: 'pendiente';
  categorias: string[];
  zonas: string[];
}

export interface TecnicoValidacionAdminResponse {
  id_tecnico: number;
  estado_validacion: 'validado' | 'rechazado' | string;
}

export type TipoReporte = 'usuarios' | 'solicitudes' | 'cotizaciones' | 'finalizados' | 'tecnicos-activos';

export interface ReporteUsuarioItem {
  id_usuario: number;
  nombres: string;
  apellidos: string;
  telefono: string | null;
  estado: string;
  fecha_registro: string;
  rol: string;
}

export interface ReporteSolicitudItem {
  id_solicitud: number;
  titulo: string;
  categoria: string;
  zona: string;
  cliente: string;
  estado: string;
  fecha_publicacion: string;
}

export interface ReporteCotizacionItem {
  id_cotizacion: number;
  solicitud: string;
  tecnico: string;
  monto: number;
  estado: string;
  fecha_envio: string;
}

export interface ReporteFinalizadoItem {
  id_solicitud: number;
  titulo: string;
  cliente: string;
  tecnico: string;
  estado: string;
  fecha_publicacion: string;
}

export interface ReporteTecnicoActivoItem {
  id_tecnico: number;
  nombres: string;
  apellidos: string;
  telefono: string | null;
  experiencia_anios: number;
  categorias: string[];
  zonas: string[];
  fecha_validacion: string | null;
}
