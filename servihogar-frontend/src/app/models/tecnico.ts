export interface TecnicoCategoriaRef {
  id_categoria: number;
  nombre: string;
}

export interface TecnicoZonaRef {
  id_zona: number;
  nombre: string;
}

export interface PortafolioItem {
  id_portafolio: number;
  titulo: string;
  descripcion: string | null;
  imagen_url: string;
  storage_path?: string | null;
}

export interface PortafolioCreateRequest {
  titulo: string;
  imagen_url: string;
  descripcion?: string;
}

export interface PortafolioItemPanel extends PortafolioItem {
  estado: string;
  fecha_subida: string;
}

export interface Tecnico {
  id_tecnico: number;
  nombres: string;
  apellidos: string;
  descripcion: string | null;
  experiencia_anios: number;
  calificacion: number | null;
  categorias: TecnicoCategoriaRef[];
  zonas: TecnicoZonaRef[];
}

export interface TecnicoDetalle extends Tecnico {
  portafolio: PortafolioItem[];
}

export type TecnicoPerfil = TecnicoDetalle;
