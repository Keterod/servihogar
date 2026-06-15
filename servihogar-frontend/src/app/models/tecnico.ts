export interface TecnicoCategoriaRef {
  id_categoria: number;
  nombre: string;
}

export interface TecnicoZonaRef {
  id_zona: number;
  nombre: string;
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
