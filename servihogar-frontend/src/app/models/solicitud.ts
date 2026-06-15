export interface SolicitudRequest {
  id_categoria: number;
  id_zona: number;
  titulo: string;
  descripcion: string;
  direccion_referencia?: string;
  id_tecnico?: number;
}

export interface SolicitudResponse {
  id_solicitud: number;
  id_cliente: number;
  estado: string;
  fecha_publicacion: string;
}

export interface SolicitudListResponse {
  id_solicitud: number;
  titulo: string;
  descripcion: string;
  direccion: string | null;
  estado: string;
  fecha_publicacion: string;
  categoria_nombre: string;
  zona_nombre: string;
  cotizaciones_count: number;
}
