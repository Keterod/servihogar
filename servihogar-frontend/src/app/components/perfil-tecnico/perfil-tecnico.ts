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
    especialidad: 'Fontanería general',
    experiencia: '8 años de experiencia en reparaciones domésticas',
    zona: 'Norte',
    valoracion: 4.8,
    descripcion:
      'Técnico independiente especializado en fontanería residencial. Atiendo emergencias menores, instalación de grifería y detección de filtraciones.',
    servicios: [
      'Reparación de tuberías',
      'Instalación de grifos',
      'Detección de filtraciones',
      'Mantenimiento preventivo',
    ],
  };
}
