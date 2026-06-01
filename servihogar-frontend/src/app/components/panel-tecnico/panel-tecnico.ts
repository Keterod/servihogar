import { Component, computed, signal } from '@angular/core';

interface Tecnico {
  nombre: string;
  especialidad: string;
  zona: string;
  calificacion: number;
}

interface Solicitud {
  id: number;
  categoria: string;
  descripcion: string;
  zona: string;
  fechaTentativa: string;
  direccion: string;
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
  imports: [],
  templateUrl: './panel-tecnico.html',
  styleUrl: './panel-tecnico.css',
})
export class PanelTecnico {
  readonly tecnico = signal<Tecnico>({
    nombre: 'Carlos Mendoza',
    especialidad: 'Gasfitería menor / Fontanería general',
    zona: 'Huancayo Centro',
    calificacion: 4.8,
  });

  readonly estadoValidacion = signal<EstadoValidacion>('validado');

  readonly solicitudesDisponibles = signal<Solicitud[]>([
    {
      id: 2,
      categoria: 'Gasfitería menor',
      descripcion: 'Cambio de llave de paso',
      zona: 'El Tambo',
      fechaTentativa: '2026-06-06',
      direccion: 'Av. Progreso 456, El Tambo',
    },
    {
      id: 3,
      categoria: 'Gasfitería menor',
      descripcion: 'Reparación de desagüe en baño',
      zona: 'Chilca',
      fechaTentativa: '2026-06-07',
      direccion: 'Calle Los Pinos 78, Chilca',
    },
  ]);

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

  readonly solicitudSeleccionada = signal<Solicitud | null>(null);

  readonly formCotizacion = signal<FormCotizacion>({
    precio: '',
    tiempo: '',
    propuesta: '',
  });

  private nextCotizacionId = 2;

  readonly totalSolicitudesDisponibles = computed(
    () => this.solicitudesDisponibles().length
  );

  readonly totalCotizacionesEnviadas = computed(
    () => this.cotizacionesEnviadas().length
  );

  readonly totalServiciosAceptados = computed(
    () => this.serviciosAceptados().length
  );

  readonly puedeEnviarCotizacion = computed(() => {
    if (this.estadoValidacion() !== 'validado') {
      return false;
    }
    if (!this.solicitudSeleccionada()) {
      return false;
    }
    const form = this.formCotizacion();
    const precio = Number(form.precio);
    return (
      precio > 0 &&
      form.tiempo.trim() !== '' &&
      form.propuesta.trim() !== ''
    );
  });

  seleccionarSolicitud(solicitud: Solicitud): void {
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
      solicitudId: solicitud.id,
      categoria: solicitud.categoria,
      descripcion: solicitud.descripcion,
      precio: Number(form.precio),
      tiempoEstimado: form.tiempo.trim(),
      propuesta: form.propuesta.trim(),
      estado: 'pendiente',
      fechaEnvio: new Date().toISOString().slice(0, 10),
    };

    this.cotizacionesEnviadas.update((lista) => [...lista, nuevaCotizacion]);
    this.solicitudesDisponibles.update((lista) =>
      lista.filter((s) => s.id !== solicitud.id)
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
    return this.solicitudSeleccionada()?.id === id;
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
