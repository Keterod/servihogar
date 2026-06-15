export type TipoUsuario = 'cliente' | 'tecnico' | 'administrador';

export interface AuthProfile {
  id_usuario: number;
  auth_user_id: string;
  nombres: string;
  apellidos: string;
  email: string;
  tipo_usuario: TipoUsuario;
  estado: string;
  id_cliente: number | null;
  id_tecnico: number | null;
  id_administrador: number | null;
  estado_validacion: string | null;
  ciudad?: string | null;
}

export interface LoginResult {
  ok: boolean;
  profile?: AuthProfile;
  error?: string;
  pendingTechnician?: boolean;
}

export interface RegisterPayload {
  nombres: string;
  apellidos: string;
  email: string;
  password: string;
  tipo_usuario: 'cliente' | 'tecnico';
  telefono?: string | null;
  descripcion?: string | null;
  experiencia_anios?: number | null;
  id_categorias?: number[];
  id_zonas?: number[];
}

export interface RegisterResponse {
  id_usuario: number;
  auth_user_id: string;
  email: string;
  tipo_usuario: TipoUsuario;
  id_cliente: number | null;
  id_tecnico: number | null;
  estado_validacion: string | null;
  mensaje: string;
}

export interface RegisterResult {
  ok: boolean;
  data?: RegisterResponse;
  error?: string;
}
