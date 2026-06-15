import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

interface Cotizacion {
  id: number;
  tecnicoNombre: string;
  especialidad: string;
  calificacion: number;
  precio: number;
  tiempoEstimado: string;
  propuesta: string;
  includes: string[];
  excludes: string[];
  estado: 'pendiente' | 'aceptada' | 'rechazada';
}

type PasoTimeline = 'pendiente' | 'cotizada' | 'aceptada' | 'en_proceso' | 'finalizada';

@Component({
  selector: 'app-detalle-solicitud',
  imports: [RouterLink],
  templateUrl: './detalle-solicitud.html',
  styleUrl: './detalle-solicitud.css',
})
export class DetalleSolicitud implements OnInit {
  private readonly route = inject(ActivatedRoute);

  readonly solicitudEstado = signal<'pendiente' | 'en_proceso'>('pendiente');

  readonly solicitud = signal({
    id: 1,
    categoria: 'Gasfitería menor',
    descripcion:
      'Fuga de agua en cocina, debajo del lavadero. El agua gotea constantemente y ha comenzado a dañar el mueble.',
    fechaTentativa: '2026-06-05',
    fechaCreacion: '2026-06-01',
    zona: 'Huancayo Centro',
    direccion: 'Jr. Los Olivos 123, Huancayo',
  });

  readonly cotizaciones = signal<Cotizacion[]>([
    {
      id: 1,
      tecnicoNombre: 'Carlos Mendoza',
      especialidad: 'Gasfitería menor',
      calificacion: 4.8,
      precio: 85,
      tiempoEstimado: '2 horas',
      propuesta:
        'Reparación completa de la fuga, reemplazo de lavadero si es necesario, revisión de tuberías.',
      includes: ['Materiales básicos de sellado', 'Revisión de tuberías', 'Limpieza del área'],
      excludes: ['Repuesto de lavadero (adicional)', 'Trabajos en techo'],
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
      includes: ['Sellado de fuga', 'Limpieza del área'],
      excludes: ['Repuestos', 'Pintura o acabados'],
      estado: 'pendiente',
    },
    {
      id: 3,
      tecnicoNombre: 'Roberto Salas',
      especialidad: 'Gasfitería menor',
      calificacion: 4.2,
      precio: 95,
      tiempoEstimado: '3 horas',
      propuesta:
        'Diagnóstico completo del sistema de agua, reparación de la fuga y prevención de futuros problemas.',
      includes: ['Diagnóstico completo', 'Reparación de fuga', 'Prevención futura', 'Materiales premium'],
      excludes: ['Instalación de tuberías nuevas'],
      estado: 'pendiente',
    },
  ]);

  readonly selectedCotizacionId = signal(1);

  readonly cotizacionAceptada = computed(() =>
    this.cotizaciones().find((c) => c.estado === 'aceptada')
  );

  readonly hayAceptada = computed(() => !!this.cotizacionAceptada());

  readonly selectedCotizacion = computed(() =>
    this.cotizaciones().find((c) => c.id === this.selectedCotizacionId())
  );

  readonly pasoActual = computed((): PasoTimeline => {
    const estado = this.solicitudEstado();
    if (estado === 'en_proceso') return 'en_proceso';
    if (this.hayAceptada()) return 'aceptada';
    if (this.cotizaciones().length > 0) return 'cotizada';
    return 'pendiente';
  });

  readonly pasosTimeline: { key: PasoTimeline; label: string }[] = [
    { key: 'pendiente', label: 'Pendiente' },
    { key: 'cotizada', label: 'Cotizada' },
    { key: 'aceptada', label: 'Aceptada' },
    { key: 'en_proceso', label: 'En proceso' },
    { key: 'finalizada', label: 'Finalizada' },
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id > 0) {
      this.solicitud.update((actual) => ({ ...actual, id }));
    }
  }

  selectCotizacion(id: number): void {
    this.selectedCotizacionId.set(id);
  }

  esPasoCompletado(paso: PasoTimeline): boolean {
    const orden: PasoTimeline[] = ['pendiente', 'cotizada', 'aceptada', 'en_proceso', 'finalizada'];
    return orden.indexOf(paso) <= orden.indexOf(this.pasoActual());
  }

  esPasoActual(paso: PasoTimeline): boolean {
    return this.pasoActual() === paso;
  }

  aceptarCotizacion(id: number): void {
    this.cotizaciones.update((cotizaciones) =>
      cotizaciones.map((c) => ({
        ...c,
        estado: c.id === id ? 'aceptada' : 'rechazada',
      }))
    );
    this.solicitudEstado.set('en_proceso');
    this.selectedCotizacionId.set(id);
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
