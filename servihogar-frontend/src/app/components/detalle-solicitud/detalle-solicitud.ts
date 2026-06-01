import { Component, signal, computed } from '@angular/core';
import { Router } from '@angular/router';

interface Cotizacion {
  id: number;
  tecnicoNombre: string;
  especialidad: string;
  calificacion: number;
  precio: number;
  tiempoEstimado: string;
  propuesta: string;
  estado: 'pendiente' | 'aceptada' | 'rechazada';
}

@Component({
  selector: 'app-detalle-solicitud',
  imports: [],
  templateUrl: './detalle-solicitud.html',
  styleUrl: './detalle-solicitud.css',
})
export class DetalleSolicitud {
  readonly solicitud = signal({
    categoria: 'Gasfitería menor',
    descripcion: 'Fuga de agua en cocina, debajo del lavadero. El agua gotea constantemente y ha comenzado a dañar el mueble.',
    estado: signal<'pendiente' | 'en_proceso'>('pendiente'),
    fechaTentativa: '2026-06-05',
    zona: 'Huancayo Centro',
    direccion: 'Jr. Los Olivos 123, Huancayo',
  });

  readonly cotizaciones = signal<Cotizacion[]>([
    {
      id: 1,
      tecnicoNombre: 'Carlos Mendoza',
      especialidad: 'Fontanería general',
      calificacion: 4.8,
      precio: 85,
      tiempoEstimado: '2 horas',
      propuesta: 'Reparación completa de la fuga, reemplazo de lavadero si es necesario, revisión de tuberías.',
      estado: 'pendiente',
    },
    {
      id: 2,
      tecnicoNombre: 'Luis Arango',
      especialidad: 'Reparaciones menores',
      calificacion: 4.5,
      precio: 70,
      tiempoEstimado: '1.5 horas',
      propuesta: 'Sellado de fuga con materiales resistentes, limpieza del área afectada.',
      estado: 'pendiente',
    },
    {
      id: 3,
      tecnicoNombre: 'Roberto Salas',
      especialidad: 'Gasfitería residencial',
      calificacion: 4.2,
      precio: 95,
      tiempoEstimado: '3 horas',
      propuesta: 'Diagnóstico completo del sistema de agua, reparación de la fuga y prevención de futuros problemas.',
      estado: 'pendiente',
    },
  ]);

  readonly cotizacionAceptada = computed(() =>
    this.cotizaciones().find((c) => c.estado === 'aceptada')
  );

  readonly hayAceptada = computed(() => !!this.cotizacionAceptada());

  constructor(private router: Router) {}

  aceptarCotizacion(id: number): void {
    this.cotizaciones.update((cotizaciones) =>
      cotizaciones.map((c) => ({
        ...c,
        estado: c.id === id ? 'aceptada' : 'rechazada',
      }))
    );
    this.solicitud().estado.set('en_proceso');
  }

  rechazarCotizacion(id: number): void {
    if (this.hayAceptada()) return;

    this.cotizaciones.update((cotizaciones) =>
      cotizaciones.map((c) => (c.id === id ? { ...c, estado: 'rechazada' } : c))
    );
  }

  irAValorar(): void {
    this.router.navigate(['/valorar-servicio']);
  }
}
