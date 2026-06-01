import { Usuario } from './usuario';

export interface Tecnico extends Usuario {
  especialidad?: string;
  zonaIds?: number[];
}
