import { Component, computed, DestroyRef, inject, OnInit, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DatePipe } from '@angular/common';
import { NavigationEnd, Router, RouterLink } from '@angular/router';
import { Subject, switchMap } from 'rxjs';
import { filter, tap } from 'rxjs/operators';

import { SolicitudService } from '../../services/solicitud.service';
import { SolicitudDisponible } from '../../models/solicitud';

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

interface ServicioAceptado {
  id: number;
  categoria: string;
  descripcion: string;
  zona: string;
  cliente: string;
  estado: 'en_proceso' | 'finalizado';
  fecha: string;
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

  readonly serviciosAceptados = signal<ServicioAceptado[]>([
    {
      id: 1,
      categoria: 'Gasfitería menor',
      descripcion: 'Instalación de grifería en lavadero',
      zona: 'Huancayo Centro',
      cliente: 'María López',
      estado: 'finalizado',
      fecha: '2026-05-20',
    },
  ]);

  readonly solicitudSeleccionada = signal<SolicitudDisponible | null>(null);

  readonly formCotizacion = signal<FormCotizacion>({
    precio: '',
    tiempo: '',
    propuesta: '',
  });

  private nextCotizacionId = 2;

  readonly totalSolicitudesDisponibles = computed(() => this.solicitudesDisponibles().length);

  readonly pendientesDeCotizar = computed(() =>
    this.solicitudesDisponibles().filter((s) => !s.ya_cotizada_por_tecnico).length,
  );

  readonly yaCotizadas = computed(() =>
    this.solicitudesDisponibles().filter((s) => s.ya_cotizada_por_tecnico).length,
  );

  readonly totalCotizacionesEnviadas = computed(() => this.cotizacionesEnviadas().length);

  readonly totalServiciosAceptados = computed(() => this.serviciosAceptados().length);

  readonly puedeEnviarCotizacion = computed(() => {
    if (this.estadoValidacion() !== 'validado') {
      return false;
    }
    const solicitud = this.solicitudSeleccionada();
    if (!solicitud || solicitud.ya_cotizada_por_tecnico) {
      return false;
    }
    const form = this.formCotizacion();
    const precio = Number(form.precio);
    return precio > 0 && form.tiempo.trim() !== '' && form.propuesta.trim() !== '';
  });

  ngOnInit(): void {
    this.recargar
      .pipe(
        tap(() => {
          this.cargando.set(true);
          this.error.set(false);
          this.solicitudesDisponibles.set([]);
        }),
        switchMap(() => this.solicitudService.solicitudesDisponiblesTecnico()),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((resultado) => {
        this.cargando.set(false);
        if (resultado === null) {
          this.error.set(true);
          return;
        }
        this.solicitudesDisponibles.set(resultado);
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

  seleccionarSolicitud(solicitud: SolicitudDisponible): void {
    this.solicitudSeleccionada.set(solicitud);
    this.formCotizacion.set({ precio: '', tiempo: '', propuesta: '' });
  }

  enviarCotizacion(): void {
    if (!this.puedeEnviarCotizacion()) {
      return;
    }

    const solicitud = this.solicitudSeleccionada();
    if (!solicitud) {
      return;
    }

    const form = this.formCotizacion();
    const nuevaCotizacion: CotizacionEnviada = {
      id: this.nextCotizacionId++,
      solicitudId: solicitud.id_solicitud,
      categoria: solicitud.categoria_nombre,
      descripcion: solicitud.descripcion,
      precio: Number(form.precio),
      tiempoEstimado: form.tiempo.trim(),
      propuesta: form.propuesta.trim(),
      estado: 'pendiente',
      fechaEnvio: new Date().toISOString().slice(0, 10),
    };

    this.cotizacionesEnviadas.update((lista) => [...lista, nuevaCotizacion]);
    this.solicitudesDisponibles.update((lista) =>
      lista.map((s) =>
        s.id_solicitud === solicitud.id_solicitud
          ? { ...s, ya_cotizada_por_tecnico: true }
          : s,
      ),
    );
    this.solicitudSeleccionada.set(null);
    this.formCotizacion.set({ precio: '', tiempo: '', propuesta: '' });
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
    return this.solicitudSeleccionada()?.id_solicitud === id;
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

  getEstadoServicioLabel(estado: ServicioAceptado['estado']): string {
    const labels: Record<ServicioAceptado['estado'], string> = {
      en_proceso: 'En proceso',
      finalizado: 'Finalizado',
    };
    return labels[estado];
  }

  formatPrecio(precio: number): string {
    return `S/ ${precio.toFixed(2)}`;
  }
}
