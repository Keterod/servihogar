import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { SolicitudService } from '../../services/solicitud.service';
import { CotizacionDetalle, SolicitudDetalle } from '../../models/solicitud';

type PasoTimeline = 'pendiente' | 'cotizada' | 'aceptada' | 'en_proceso' | 'finalizada';
type CotizacionEstado = CotizacionDetalle['estado'];

@Component({
  selector: 'app-detalle-solicitud',
  imports: [RouterLink, DatePipe],
  templateUrl: './detalle-solicitud.html',
  styleUrl: './detalle-solicitud.css',
})
export class DetalleSolicitud implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly solicitudService = inject(SolicitudService);

  readonly loading = signal(true);
  readonly error = signal(false);
  readonly notFound = signal(false);
  readonly solicitud = signal<SolicitudDetalle | null>(null);
  readonly cotizaciones = signal<CotizacionDetalle[]>([]);
  readonly selectedCotizacionId = signal<number | null>(null);
  readonly localEstadoOverride = signal<string | null>(null);

  readonly cotizacionAceptada = computed(() =>
    this.cotizaciones().find((c) => c.estado === 'aceptada'),
  );

  readonly hayAceptada = computed(() => !!this.cotizacionAceptada());

  readonly selectedCotizacion = computed(() =>
    this.cotizaciones().find((c) => c.id_cotizacion === this.selectedCotizacionId()),
  );

  readonly estadoDisplay = computed(() => {
    const override = this.localEstadoOverride();
    if (override) return override;
    return this.solicitud()?.estado ?? 'pendiente';
  });

  readonly pasoActual = computed((): PasoTimeline => {
    const estado = this.estadoDisplay();
    if (estado === 'finalizada') return 'finalizada';
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

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.notFound.set(true);
      this.loading.set(false);
      return;
    }
    this.cargarDetalle(id);
  }

  private cargarDetalle(id: number): void {
    this.loading.set(true);
    this.error.set(false);
    this.notFound.set(false);
    this.localEstadoOverride.set(null);

    this.solicitudService.obtenerDetalle(id).subscribe({
      next: (data) => {
        this.loading.set(false);
        if (data === null) {
          this.notFound.set(true);
          return;
        }
        this.solicitud.set(data);
        this.cotizaciones.set(data.cotizaciones);
        this.selectedCotizacionId.set(
          data.cotizaciones.length > 0 ? data.cotizaciones[0].id_cotizacion : null,
        );
      },
      error: () => {
        this.loading.set(false);
        this.error.set(true);
      },
    });
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
    this.cotizaciones.update((items) =>
      items.map((c) => ({
        ...c,
        estado: (c.id_cotizacion === id ? 'aceptada' : 'rechazada') as CotizacionEstado,
      })),
    );
    this.localEstadoOverride.set('en_proceso');
    this.selectedCotizacionId.set(id);
  }

  rechazarCotizacion(id: number): void {
    if (this.hayAceptada()) return;

    this.cotizaciones.update((items) =>
      items.map((c) =>
        c.id_cotizacion === id ? { ...c, estado: 'rechazada' as CotizacionEstado } : c,
      ),
    );
  }

  getEstadoLabel(estado: string): string {
    const labels: Record<string, string> = {
      pendiente: 'Pendiente',
      en_proceso: 'En proceso',
      finalizada: 'Finalizado',
      cancelada: 'Cancelado',
    };
    return labels[estado] || estado;
  }

  getCotizacionEstadoLabel(estado: string): string {
    const labels: Record<string, string> = {
      pendiente: 'Pendiente',
      aceptada: 'Aceptada',
      rechazada: 'Rechazada',
      retirada: 'Retirada',
    };
    return labels[estado] || estado;
  }

  irAValorar(): void {
    this.router.navigate(['/valorar-servicio']);
  }
}
