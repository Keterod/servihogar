import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

interface CategoriaDestacada {
  nombre: string;
  descripcion: string;
  icono: string;
}

interface PasoUso {
  numero: number;
  titulo: string;
  descripcion: string;
}

@Component({
  selector: 'app-home',
  imports: [RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  readonly categoriasDestacadas: CategoriaDestacada[] = [
    {
      nombre: 'Fontanería',
      descripcion: 'Reparaciones de tuberías, grifos y filtraciones.',
      icono: '🔧',
    },
    {
      nombre: 'Electricidad',
      descripcion: 'Instalaciones eléctricas menores y mantenimiento.',
      icono: '⚡',
    },
    {
      nombre: 'Cerrajería',
      descripcion: 'Apertura de puertas y cambio de cerraduras.',
      icono: '🔑',
    },
    {
      nombre: 'Limpieza',
      descripcion: 'Servicios de limpieza del hogar y mantenimiento.',
      icono: '🧹',
    },
  ];

  readonly pasosUso: PasoUso[] = [
    {
      numero: 1,
      titulo: 'Busca técnicos',
      descripcion: 'Explora profesionales por categoría y zona de servicio.',
    },
    {
      numero: 2,
      titulo: 'Revisa perfiles',
      descripcion: 'Consulta especialidad, experiencia y valoraciones de otros clientes.',
    },
    {
      numero: 3,
      titulo: 'Publica una solicitud',
      descripcion: 'Describe el servicio que necesitas como cliente registrado.',
    },
    {
      numero: 4,
      titulo: 'Elige una cotización',
      descripcion: 'Los técnicos envían cotizaciones y tú seleccionas la mejor opción.',
    },
  ];
}
