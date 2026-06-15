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
  readonly origen = signal<'cliente' | 'tecnico'>('cliente');
  readonly accionCotizacionId = signal<number | null>(null);
  readonly errorAccion = signal<string | null>(null);

  readonly esVistaCliente = computed(() => this.origen() === 'cliente');

  readonly volverRuta = computed(() =>
    this.origen() === 'tecnico' ? '/panel-tecnico' : '/panel-cliente',
  );

  readonly volverTexto = computed(() =>
    this.origen() === 'tecnico' ? 'Volver al panel técnico' : 'Volver a mis solicitudes',
  );

  readonly cotizacionAceptada = computed(() =>
    this.cotizaciones().find((c) => c.estado === 'aceptada'),
  );

  readonly hayAceptada = computed(() => !!this.cotizacionAceptada());

  readonly puedeValorar = computed(() => {
    if (!this.esVistaCliente()) {
      return false;
    }
    const estado = this.estadoDisplay();
    return estado === 'en_proceso' || estado === 'finalizada';
  });

  readonly selectedCotizacion = computed(() =>
    this.cotizaciones().find((c) => c.id_cotizacion === this.selectedCotizacionId()),
  );

  readonly estadoDisplay = computed(() => this.solicitud()?.estado ?? 'pendiente');

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
    const from = this.route.snapshot.queryParamMap.get('from');
    if (from === 'tecnico') {
      this.origen.set('tecnico');
    }

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
    this.errorAccion.set(null);

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
    this.errorAccion.set(null);
  }

  esPasoCompletado(paso: PasoTimeline): boolean {
    const orden: PasoTimeline[] = ['pendiente', 'cotizada', 'aceptada', 'en_proceso', 'finalizada'];
    return orden.indexOf(paso) <= orden.indexOf(this.pasoActual());
  }

  esPasoActual(paso: PasoTimeline): boolean {
    return this.pasoActual() === paso;
  }

  accionEnCurso(id: number): boolean {
    return this.accionCotizacionId() === id;
  }

  aceptarCotizacion(id: number): void {
    if (!this.esVistaCliente() || this.accionCotizacionId() !== null || this.hayAceptada()) {
      return;
    }

    this.accionCotizacionId.set(id);
    this.errorAccion.set(null);

    this.solicitudService.aceptarCotizacion(id).subscribe((resultado) => {
      this.accionCotizacionId.set(null);

      if (resultado === 'not_found') {
        this.errorAccion.set('La cotización no existe o ya no está disponible.');
        return;
      }
      if (resultado === 'bad_request') {
        this.errorAccion.set('Esta cotización ya no se puede aceptar.');
        return;
      }
      if (resultado === 'conflict') {
        this.errorAccion.set('Esta solicitud ya tiene una cotización aceptada.');
        return;
      }
      if (resultado === null) {
        this.errorAccion.set(
          'No se pudo aceptar la cotización. Verifica que el backend esté disponible.',
        );
        return;
      }

      this.cotizaciones.update((items) =>
        items.map((c) => ({
          ...c,
          estado: (c.id_cotizacion === id
            ? 'aceptada'
            : c.estado === 'pendiente'
              ? 'rechazada'
              : c.estado) as CotizacionEstado,
        })),
      );
      this.solicitud.update((s) =>
        s ? { ...s, estado: resultado.solicitud_estado } : s,
      );
      this.selectedCotizacionId.set(id);
      this.errorAccion.set(null);
    });
  }

  rechazarCotizacion(id: number): void {
    if (!this.esVistaCliente() || this.accionCotizacionId() !== null || this.hayAceptada()) {
      return;
    }

    this.accionCotizacionId.set(id);
    this.errorAccion.set(null);

    this.solicitudService.rechazarCotizacion(id).subscribe((resultado) => {
      this.accionCotizacionId.set(null);

      if (resultado === 'not_found') {
        this.errorAccion.set('La cotización no existe o ya no está disponible.');
        return;
      }
      if (resultado === 'bad_request') {
        this.errorAccion.set('Esta cotización ya no se puede rechazar.');
        return;
      }
      if (resultado === null) {
        this.errorAccion.set(
          'No se pudo rechazar la cotización. Verifica que el backend esté disponible.',
        );
        return;
      }

      this.cotizaciones.update((items) =>
        items.map((c) =>
          c.id_cotizacion === id ? { ...c, estado: 'rechazada' as CotizacionEstado } : c,
        ),
      );
      this.errorAccion.set(null);
    });
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
    const id = this.solicitud()?.id_solicitud;
    if (!id) {
      return;
    }
    this.router.navigate(['/valorar-servicio'], {
      queryParams: { idSolicitud: id },
    });
  }
}
