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
