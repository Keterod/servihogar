export interface ImagenSolicitud {
  id_imagen: number;
  imagen_url: string;
  descripcion: string | null;
  fecha_subida: string;
}

export interface ImagenSolicitudRequest {
  imagen_url: string;
  descripcion?: string;
}

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

export interface SolicitudDisponible {
  id_solicitud: number;
  titulo: string;
  descripcion: string;
  direccion: string | null;
  estado: string;
  fecha_publicacion: string;
  categoria_nombre: string;
  zona_nombre: string;
  cliente_nombre: string | null;
  cotizaciones_count: number;
  ya_cotizada_por_tecnico: boolean;
}

export interface ServicioAceptado {
  id_solicitud: number;
  titulo: string;
  descripcion: string;
  direccion: string | null;
  estado: string;
  fecha_publicacion: string;
  categoria_nombre: string;
  zona_nombre: string;
  cliente_nombre: string | null;
  id_cotizacion: number;
  precio: number;
  tiempo_estimado: string | null;
  estado_cotizacion: string;
}

export interface CotizacionRequest {
  id_solicitud: number;
  precio: number;
  tiempo_estimado: string;
  descripcion_propuesta: string;
}

export interface CotizacionResponse {
  id_cotizacion: number;
  id_solicitud: number;
  id_tecnico: number;
  precio: number;
  tiempo_estimado: string | null;
  descripcion_propuesta: string;
  estado: string;
  fecha_creacion: string;
}

export interface CotizacionActionResponse {
  id_cotizacion: number;
  id_solicitud: number;
  precio: number;
  tiempo_estimado: string | null;
  descripcion_propuesta: string;
  estado: string;
  fecha_creacion: string;
  solicitud_estado: string;
}

export interface CotizacionDetalle {
  id_cotizacion: number;
  id_tecnico: number;
  tecnico_nombre: string;
  tecnico_descripcion: string | null;
  precio: number;
  tiempo_estimado: string | null;
  descripcion_propuesta: string;
  estado: string;
  fecha_creacion: string;
}

export interface SolicitudDetalle {
  id_solicitud: number;
  titulo: string;
  descripcion: string;
  direccion: string | null;
  estado: string;
  fecha_publicacion: string;
  categoria_nombre: string;
  zona_nombre: string;
  cotizaciones: CotizacionDetalle[];
  imagenes?: ImagenSolicitud[];
}

export interface ValoracionRequest {
  id_solicitud: number;
  calificacion: number;
  comentario?: string;
  puntualidad?: number;
  calidad?: number;
  trato?: number;
  precio?: number;
}

export interface ValoracionResponse {
  id_valoracion: number;
  id_cotizacion: number;
  id_solicitud: number;
  puntuacion: number;
  comentario: string | null;
  puntualidad: number | null;
  calidad: number | null;
  precio: number | null;
  trato: number | null;
  fecha_valoracion: string;
  solicitud_estado: string;
}
