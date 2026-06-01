import { Component, signal, computed } from '@angular/core';
import { Router } from '@angular/router';

interface Solicitud {
  id: number;
  categoria: string;
  descripcion: string;
  zona: string;
  fechaTentativa: string;
  estado: 'pendiente' | 'en_proceso' | 'finalizado' | 'cancelado';
  cotizaciones: number;
}

@Component({
  selector: 'app-panel-cliente',
  imports: [],
  templateUrl: './panel-cliente.html',
  styleUrl: './panel-cliente.css',
})
export class PanelCliente {
  readonly solicitudes = signal<Solicitud[]>([
    {
      id: 1,
      categoria: 'Gasfitería menor',
      descripcion: 'Fuga de agua en cocina',
      zona: 'Huancayo Centro',
      fechaTentativa: '2026-06-05',
      estado: 'pendiente',
      cotizaciones: 2,
    },
    {
      id: 2,
      categoria: 'Electricidad básica',
      descripcion: 'Cortocircuito en enchufe del living',
      zona: 'El Tambo',
      fechaTentativa: '2026-06-03',
      estado: 'en_proceso',
      cotizaciones: 3,
    },
    {
      id: 3,
      categoria: 'Pintura básica',
      descripcion: 'Pintar habitación principal',
      zona: 'Chilca',
      fechaTentativa: '2026-05-28',
      estado: 'finalizado',
      cotizaciones: 4,
    },
  ]);

  readonly pendientes = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'pendiente').length
  );

  readonly enProceso = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'en_proceso').length
  );

  readonly finalizadas = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'finalizado').length
  );

  readonly canceladas = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'cancelado').length
  );

  constructor(private router: Router) {}

  verDetalle(): void {
    this.router.navigate(['/detalle-solicitud']);
  }

  getEstadoLabel(estado: string): string {
    const labels: Record<string, string> = {
      pendiente: 'Pendiente',
      en_proceso: 'En proceso',
      finalizado: 'Finalizado',
      cancelado: 'Cancelado',
    };
    return labels[estado] || estado;
  }
}
