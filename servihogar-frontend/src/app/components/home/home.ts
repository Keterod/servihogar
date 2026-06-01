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
    { nombre: 'Gasfitería menor', descripcion: 'Reparaciones de agua y desagüe.', icono: '🔧' },
    { nombre: 'Electricidad básica', descripcion: 'Instalaciones eléctricas menores.', icono: '⚡' },
    { nombre: 'Mantenimiento de PC', descripcion: 'Soporte y mantenimiento de equipos.', icono: '💻' },
    { nombre: 'Armado de muebles', descripcion: 'Montaje de muebles y estanterías.', icono: '🪑' },
    { nombre: 'Pintura básica', descripcion: 'Pintura interior y exterior.', icono: '🎨' },
    { nombre: 'Reparaciones menores', descripcion: 'Arreglos generales del hogar.', icono: '🛠️' },
  ];

  readonly pasosUso: PasoUso[] = [
    {
      numero: 1,
      titulo: 'Publica tu solicitud',
      descripcion: 'Describe el servicio que necesitas y recibe cotizaciones de técnicos verificados.',
    },
    {
      numero: 2,
      titulo: 'Elige la mejor cotización',
      descripcion: 'Compara precios, tiempos y valoraciones para seleccionar al técnico ideal.',
    },
    {
      numero: 3,
      titulo: 'Valora al finalizar',
      descripcion: 'Califica el servicio recibido y ayuda a otros clientes a decidir.',
    },
  ];
}
