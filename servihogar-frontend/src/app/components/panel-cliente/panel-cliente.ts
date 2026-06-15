import { Component, DestroyRef, inject, signal, computed, OnInit } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DatePipe } from '@angular/common';
import { NavigationEnd, Router, RouterLink, RouterLinkActive } from '@angular/router';
import { Subject, switchMap } from 'rxjs';
import { filter, tap } from 'rxjs/operators';

import { SolicitudService } from '../../services/solicitud.service';
import { SolicitudListResponse } from '../../models/solicitud';

@Component({
  selector: 'app-panel-cliente',
  imports: [RouterLink, RouterLinkActive, DatePipe],
  templateUrl: './panel-cliente.html',
  styleUrl: './panel-cliente.css',
})
export class PanelCliente implements OnInit {
  private readonly solicitudService = inject(SolicitudService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private readonly recargar = new Subject<void>();

  readonly solicitudes = signal<SolicitudListResponse[]>([]);
  readonly cargando = signal(true);
  readonly error = signal(false);

  readonly pendientes = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'pendiente').length,
  );

  readonly enProceso = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'en_proceso').length,
  );

  readonly finalizadas = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'finalizada').length,
  );

  readonly canceladas = computed(() =>
    this.solicitudes().filter((s) => s.estado === 'cancelada').length,
  );

  readonly totalCotizaciones = computed(() =>
    this.solicitudes().reduce((sum, s) => sum + s.cotizaciones_count, 0),
  );

  ngOnInit(): void {
    this.recargar
      .pipe(
        tap(() => {
          this.cargando.set(true);
          this.error.set(false);
          this.solicitudes.set([]);
        }),
        switchMap(() => this.solicitudService.solicitudesCliente()),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((resultado) => {
        this.cargando.set(false);
        if (resultado === null) {
          this.error.set(true);
          return;
        }
        this.solicitudes.set(resultado);
      });

    this.recargar.next();

    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        filter(() => this.esRutaPanelCliente()),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(() => this.recargar.next());
  }

  private esRutaPanelCliente(): boolean {
    return this.router.url.split('?')[0] === '/panel-cliente';
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
}
