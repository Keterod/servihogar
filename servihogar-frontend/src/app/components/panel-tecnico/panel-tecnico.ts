import { Component, computed, DestroyRef, inject, OnInit, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DatePipe } from '@angular/common';
import { NavigationEnd, Router, RouterLink } from '@angular/router';
import { Subject, forkJoin, switchMap } from 'rxjs';
import { filter, tap } from 'rxjs/operators';

import { SolicitudService } from '../../services/solicitud.service';
import { ServicioAceptado, SolicitudDisponible } from '../../models/solicitud';

interface Tecnico {
  nombre: string;
  especialidad: string;
  zona: string;
  calificacion: number;
}

interface FormCotizacion {
  precio: string;
  tiempo: string;
  propuesta: string;
}

interface CotizacionEnviada {
  id: number;
  solicitudId: number;
  categoria: string;
  descripcion: string;
  precio: number;
  tiempoEstimado: string;
  propuesta: string;
  estado: 'pendiente' | 'aceptada' | 'rechazada';
  fechaEnvio: string;
}

type EstadoValidacion = 'pendiente' | 'validado' | 'rechazado';

@Component({
  selector: 'app-panel-tecnico',
  imports: [RouterLink, DatePipe],
  templateUrl: './panel-tecnico.html',
  styleUrl: './panel-tecnico.css',
})
export class PanelTecnico implements OnInit {
  private readonly solicitudService = inject(SolicitudService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private readonly recargar = new Subject<void>();

  readonly tecnico = signal<Tecnico>({
    nombre: 'Carlos Mendoza',
    especialidad: 'Gasfitería menor',
    zona: 'Huancayo Centro',
    calificacion: 4.8,
  });

  readonly estadoValidacion = signal<EstadoValidacion>('validado');

  readonly solicitudesDisponibles = signal<SolicitudDisponible[]>([]);
  readonly cargando = signal(true);
  readonly error = signal(false);

  readonly serviciosAceptados = signal<ServicioAceptado[]>([]);
  readonly cargandoAceptados = signal(true);
  readonly errorAceptados = signal(false);

  readonly cotizacionesEnviadas = signal<CotizacionEnviada[]>([
    {
      id: 1,
      solicitudId: 1,
      categoria: 'Gasfitería menor',
      descripcion: 'Fuga de agua en cocina',
      precio: 85,
      tiempoEstimado: '2 horas',
      propuesta:
        'Reparación completa de la fuga, reemplazo de lavadero si es necesario, revisión de tuberías.',
      estado: 'pendiente',
      fechaEnvio: '2026-06-01',
    },
  ]);

  readonly solicitudActivaId = signal<number | null>(null);
  readonly solicitudFormulario = signal<SolicitudDisponible | null>(null);

  readonly solicitudSeleccionada = computed(
    () => this.solicitudFormulario() ?? this._buscarSolicitudEnLista(this.solicitudActivaId()),
  );

  readonly formCotizacion = signal<FormCotizacion>({
    precio: '',
    tiempo: '',
    propuesta: '',
  });

  readonly enviandoCotizacion = signal(false);
  readonly errorCotizacion = signal<string | null>(null);
  readonly exitoCotizacion = signal(false);

  readonly totalSolicitudesDisponibles = computed(() => this.solicitudesDisponibles().length);

  readonly pendientesDeCotizar = computed(() =>
    this.solicitudesDisponibles().filter((s) => !s.ya_cotizada_por_tecnico).length,
  );

  readonly yaCotizadas = computed(() =>
    this.solicitudesDisponibles().filter((s) => s.ya_cotizada_por_tecnico).length,
  );

  readonly totalCotizacionesEnviadas = computed(() => this.cotizacionesEnviadas().length);

  readonly totalServiciosAceptados = computed(() => this.serviciosAceptados().length);

  readonly mensajeAyudaFormulario = computed(() => {
    if (!this.solicitudSeleccionada()) {
      return 'Selecciona una solicitud y pulsa «Cotizar» para abrir el formulario.';
    }
    if (this.solicitudSeleccionada()!.ya_cotizada_por_tecnico) {
      return 'Esta solicitud ya tiene tu cotización.';
    }
    const form = this.formCotizacion();
    if (!form.precio.trim() || Number(form.precio) <= 0) {
      return 'Completa el precio estimado (mayor a 0).';
    }
    if (!form.tiempo.trim()) {
      return 'Completa el tiempo estimado.';
    }
    if (!form.propuesta.trim()) {
      return 'Completa la propuesta de trabajo.';
    }
    return 'Listo para enviar. Pulsa «Enviar cotización».';
  });

  ngOnInit(): void {
    this.recargar
      .pipe(
        tap(() => {
          this.cargando.set(true);
          this.error.set(false);
          this.cargandoAceptados.set(true);
          this.errorAceptados.set(false);
        }),
        switchMap(() =>
          forkJoin({
            disponibles: this.solicitudService.solicitudesDisponiblesTecnico(),
            aceptados: this.solicitudService.serviciosAceptadosTecnico(),
          }),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(({ disponibles, aceptados }) => {
        this.cargando.set(false);
        this.cargandoAceptados.set(false);

        if (disponibles === null) {
          this.error.set(true);
        } else {
          this.solicitudesDisponibles.set(disponibles);
        }

        if (aceptados === null) {
          this.errorAceptados.set(true);
        } else {
          this.serviciosAceptados.set(aceptados);
        }
      });

    this.recargar.next();

    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        filter(() => this.esRutaPanelTecnico()),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(() => this.recargar.next());
  }

  private esRutaPanelTecnico(): boolean {
    return this.router.url.split('?')[0] === '/panel-tecnico';
  }

  private _buscarSolicitudEnLista(id: number | null): SolicitudDisponible | null {
    if (id === null) {
      return null;
    }
    return this.solicitudesDisponibles().find((s) => s.id_solicitud === id) ?? null;
  }

  abrirFormularioCotizacion(solicitud: SolicitudDisponible): void {
    if (solicitud.ya_cotizada_por_tecnico) {
      this.solicitudActivaId.set(null);
      this.solicitudFormulario.set(null);
      this.formCotizacion.set({ precio: '', tiempo: '', propuesta: '' });
      this.errorCotizacion.set('Ya enviaste una cotización para esta solicitud.');
      this.exitoCotizacion.set(false);
      return;
    }

    this.solicitudActivaId.set(solicitud.id_solicitud);
    this.solicitudFormulario.set(solicitud);
    this.formCotizacion.set({ precio: '', tiempo: '', propuesta: '' });
    this.errorCotizacion.set(null);
    this.exitoCotizacion.set(false);

    queueMicrotask(() => {
      document.getElementById('seccion-cotizacion')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    });
  }

  enviarCotizacion(): void {
    if (this.enviandoCotizacion()) {
      return;
    }

    const idSolicitud = this.solicitudActivaId();
    const solicitud = this.solicitudFormulario() ?? this._buscarSolicitudEnLista(idSolicitud);

    if (idSolicitud === null || solicitud === null) {
      this.errorCotizacion.set('Selecciona una solicitud antes de enviar la cotización.');
      this.exitoCotizacion.set(false);
      return;
    }

    if (solicitud.ya_cotizada_por_tecnico) {
      this.errorCotizacion.set('Ya enviaste una cotización para esta solicitud.');
      this.exitoCotizacion.set(false);
      return;
    }

    if (this.estadoValidacion() !== 'validado') {
      this.errorCotizacion.set('Tu perfil debe estar validado para enviar cotizaciones.');
      this.exitoCotizacion.set(false);
      return;
    }

    const form = this.formCotizacion();
    const precio = Number(form.precio);
    if (!form.precio.trim() || Number.isNaN(precio) || precio <= 0) {
      this.errorCotizacion.set('Ingresa un precio válido mayor a 0.');
      this.exitoCotizacion.set(false);
      return;
    }
    if (!form.tiempo.trim()) {
      this.errorCotizacion.set('Ingresa el tiempo estimado.');
      this.exitoCotizacion.set(false);
      return;
    }
    if (!form.propuesta.trim()) {
      this.errorCotizacion.set('Ingresa una propuesta de trabajo.');
      this.exitoCotizacion.set(false);
      return;
    }

    this.enviandoCotizacion.set(true);
    this.errorCotizacion.set(null);
    this.exitoCotizacion.set(false);

    const payload = {
      id_solicitud: idSolicitud,
      precio: Number(form.precio),
      tiempo_estimado: form.tiempo.trim(),
      descripcion_propuesta: form.propuesta.trim(),
    };

    this.solicitudService.crearCotizacion(payload).subscribe((resultado) => {
      this.enviandoCotizacion.set(false);

      if (resultado === 'duplicate') {
        this.marcarComoCotizada(idSolicitud);
        this.errorCotizacion.set('Ya enviaste una cotización para esta solicitud.');
        this.exitoCotizacion.set(false);
        return;
      }

      if (resultado === 'not_found') {
        this.errorCotizacion.set(
          'La solicitud seleccionada no existe o ya no está disponible. Recarga el panel e inténtalo de nuevo.',
        );
        return;
      }

      if (resultado === 'bad_request') {
        this.errorCotizacion.set(
          'Esta solicitud ya no se puede cotizar (estado o categoría/zona no válidos). Recarga el panel.',
        );
        return;
      }

      if (resultado === null) {
        this.errorCotizacion.set(
          'No se pudo enviar la cotización. Verifica que el backend esté disponible.',
        );
        return;
      }

      this.marcarComoCotizada(idSolicitud);
      this.cotizacionesEnviadas.update((lista) => [
        ...lista,
        {
          id: resultado.id_cotizacion,
          solicitudId: resultado.id_solicitud,
          categoria: solicitud.categoria_nombre,
          descripcion: solicitud.descripcion,
          precio: resultado.precio,
          tiempoEstimado: resultado.tiempo_estimado ?? form.tiempo.trim(),
          propuesta: resultado.descripcion_propuesta,
          estado: 'pendiente',
          fechaEnvio: resultado.fecha_creacion.slice(0, 10),
        },
      ]);
      this.exitoCotizacion.set(true);
      this.errorCotizacion.set(null);
    });
  }

  private marcarComoCotizada(idSolicitud: number): void {
    this.solicitudesDisponibles.update((lista) =>
      lista.map((s) =>
        s.id_solicitud === idSolicitud
          ? {
              ...s,
              ya_cotizada_por_tecnico: true,
              cotizaciones_count: s.cotizaciones_count + (s.ya_cotizada_por_tecnico ? 0 : 1),
            }
          : s,
      ),
    );

    if (this.solicitudActivaId() === idSolicitud) {
      this.solicitudActivaId.set(null);
      this.solicitudFormulario.set(null);
      this.formCotizacion.set({ precio: '', tiempo: '', propuesta: '' });
    }
  }

  actualizarPrecio(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;
    this.formCotizacion.update((form) => ({ ...form, precio: valor }));
  }

  actualizarTiempo(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;
    this.formCotizacion.update((form) => ({ ...form, tiempo: valor }));
  }

  actualizarPropuesta(event: Event): void {
    const valor = (event.target as HTMLTextAreaElement).value;
    this.formCotizacion.update((form) => ({ ...form, propuesta: valor }));
  }

  esSolicitudActiva(id: number): boolean {
    return this.solicitudActivaId() === id;
  }

  getEstadoDisponibleLabel(solicitud: SolicitudDisponible): string {
    return solicitud.ya_cotizada_por_tecnico ? 'Cotizada' : 'Disponible';
  }

  getEstadoValidacionLabel(estado: EstadoValidacion): string {
    const labels: Record<EstadoValidacion, string> = {
      pendiente: 'Pendiente de validación',
      validado: 'Validado',
      rechazado: 'Rechazado',
    };
    return labels[estado];
  }

  getEstadoValidacionClass(estado: EstadoValidacion): string {
    return `badge-validacion badge-${estado}`;
  }

  getEstadoCotizacionLabel(estado: CotizacionEnviada['estado']): string {
    const labels: Record<CotizacionEnviada['estado'], string> = {
      pendiente: 'Pendiente',
      aceptada: 'Aceptada',
      rechazada: 'Rechazada',
    };
    return labels[estado];
  }

  getEstadoServicioLabel(estado: string): string {
    const labels: Record<string, string> = {
      en_proceso: 'En proceso',
      finalizada: 'Finalizada',
      finalizado: 'Finalizado',
    };
    return labels[estado] ?? estado;
  }

  formatPrecio(precio: number): string {
    return `S/ ${precio.toFixed(2)}`;
  }
}
