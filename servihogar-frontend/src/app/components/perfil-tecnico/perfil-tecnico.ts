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
    ],
  };
}
