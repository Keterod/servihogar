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
}

export interface LoginResult {
  ok: boolean;
  profile?: AuthProfile;
  error?: string;
  pendingTechnician?: boolean;
}
