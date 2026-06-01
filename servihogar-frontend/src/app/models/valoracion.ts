export interface Valoracion {
  id: number;
  solicitudId: number;
  tecnicoId: number;
  puntuacion: number;
  comentario?: string;
}
