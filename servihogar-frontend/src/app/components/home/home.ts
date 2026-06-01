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
      nombre: 'Gasfitería menor',
      descripcion: 'Reparaciones de agua, grifos y desagüe.',
      icono: '🔧',
    },
    {
      nombre: 'Electricidad básica',
      descripcion: 'Instalaciones eléctricas menores y mantenimiento.',
      icono: '⚡',
    },
    {
      nombre: 'Mantenimiento de computadoras',
      descripcion: 'Soporte técnico y mantenimiento de equipos.',
      icono: '💻',
    },
    {
      nombre: 'Pintura básica',
      descripcion: 'Pintura interior y exterior del hogar.',
      icono: '🎨',
    },
    {
      nombre: 'Armado de muebles',
      descripcion: 'Montaje de muebles y estanterías.',
      icono: '🪑',
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
    {
      numero: 5,
      titulo: 'Valora el servicio al finalizar',
      descripcion: 'Califica al técnico cuando el trabajo haya concluido.',
    },
  ];
}
