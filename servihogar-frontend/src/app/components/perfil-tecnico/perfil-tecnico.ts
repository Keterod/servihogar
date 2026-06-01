import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

interface TecnicoPerfil {
  nombre: string;
  especialidad: string;
  experiencia: string;
  zona: string;
  valoracion: number;
  descripcion: string;
  servicios: string[];
  serviciosCompletados: number;
  perfilValidado: boolean;
}

interface RatingBar {
  etiqueta: string;
  porcentaje: number;
}

interface GaleriaItem {
  id: number;
  alt: string;
}

@Component({
  selector: 'app-perfil-tecnico',
  imports: [RouterLink],
  templateUrl: './perfil-tecnico.html',
  styleUrl: './perfil-tecnico.css',
})
export class PerfilTecnico {
  readonly tecnico: TecnicoPerfil = {
    nombre: 'Carlos Mendoza',
    especialidad: 'Gasfitería menor',
    experiencia: '8 años de experiencia en reparaciones domésticas',
    zona: 'Huancayo Centro',
    valoracion: 4.8,
    descripcion:
      'Técnico independiente especializado en gasfitería menor. Atiendo reparaciones de agua, grifos y desagüe en hogares de Huancayo.',
    servicios: [
      'Reparación de tuberías',
      'Instalación de grifos',
      'Desagües obstruidos',
      'Mantenimiento preventivo',
      'Cambio de llaves de paso',
      'Detección de fugas',
    ],
    serviciosCompletados: 42,
    perfilValidado: true,
  };

  readonly galeria: GaleriaItem[] = [
    { id: 1, alt: 'Trabajo de gasfitería 1' },
    { id: 2, alt: 'Trabajo de gasfitería 2' },
    { id: 3, alt: 'Trabajo de gasfitería 3' },
    { id: 4, alt: 'Trabajo de gasfitería 4' },
  ];

  readonly ratingBars: RatingBar[] = [
    { etiqueta: 'Puntualidad', porcentaje: 92 },
    { etiqueta: 'Calidad del trabajo', porcentaje: 96 },
    { etiqueta: 'Trato al cliente', porcentaje: 88 },
    { etiqueta: 'Limpieza', porcentaje: 85 },
    { etiqueta: 'Cumplimiento de precio', porcentaje: 90 },
  ];

  getIniciales(nombre: string): string {
    return nombre
      .split(' ')
      .map((parte) => parte.charAt(0))
      .join('')
      .slice(0, 2)
      .toUpperCase();
  }
}
