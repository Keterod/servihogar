import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { CategoriaServicioService } from '../../services/categoria-servicio.service';
import { ZonaService } from '../../services/zona.service';
import { SolicitudService } from '../../services/solicitud.service';
import { CategoriaServicio } from '../../models/categoria-servicio';
import { Zona } from '../../models/zona';

@Component({
  selector: 'app-solicitud-servicio',
  imports: [RouterLink],
  templateUrl: './solicitud-servicio.html',
  styleUrl: './solicitud-servicio.css',
})
export class SolicitudServicio implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly categoriaServicioService = inject(CategoriaServicioService);
  private readonly zonaService = inject(ZonaService);
  private readonly solicitudService = inject(SolicitudService);

  readonly loading = signal(false);
  readonly success = signal(false);
  readonly error = signal(false);
  readonly categorias = signal<CategoriaServicio[]>([]);
  readonly zonas = signal<Zona[]>([]);
  readonly tecnicoNombre = signal<string | null>(null);
  readonly tecnicoId = signal<number | null>(null);

  readonly categoria = signal(0);
  readonly zona = signal(0);
  readonly descripcion = signal('');
  readonly fechaTentativa = signal('');
  readonly horarioPreferido = signal('');
  readonly direccion = signal('');

  readonly horarios = ['Mañana (8am-12pm)', 'Tarde (12pm-5pm)', 'Noche (5pm-8pm)'];

  readonly puedeEnviar = computed(
    () =>
      this.categoria() > 0 &&
      this.zona() > 0 &&
      this.descripcion().trim() !== '' &&
      this.fechaTentativa().trim() !== '' &&
      this.horarioPreferido().trim() !== '' &&
      this.direccion().trim() !== '',
  );

  private readonly selectedCategoriaNombre = computed(() => {
    const id = this.categoria();
    if (id <= 0) return null;
    return this.categorias().find((c) => c.id_categoria === id)?.nombre ?? null;
  });

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      if (params['tecnicoNombre']) {
        this.tecnicoNombre.set(decodeURIComponent(params['tecnicoNombre']));
      }
      if (params['tecnicoId']) {
        this.tecnicoId.set(Number(params['tecnicoId']));
      }
      if (params['categoriaId']) {
        this.categoria.set(Number(params['categoriaId']));
      }
    });

    this.categoriaServicioService.obtenerCategorias().subscribe({
      next: (cats) => this.categorias.set(cats),
    });
    this.zonaService.obtenerZonas().subscribe({
      next: (zs) => this.zonas.set(zs),
    });
  }

  onSubmit(): void {
    if (!this.puedeEnviar()) return;

    const categoriaNombre = this.selectedCategoriaNombre();
    this.loading.set(true);
    this.error.set(false);

    const data = {
      id_categoria: this.categoria()!,
      id_zona: this.zona()!,
      titulo: categoriaNombre ?? 'Solicitud de servicio',
      descripcion: this.descripcion(),
      direccion_referencia: this.direccion(),
      id_tecnico: this.tecnicoId() ?? undefined,
    };

    this.solicitudService.crearSolicitud(data).subscribe({
      next: (result) => {
        this.loading.set(false);
        if (result === null) {
          this.error.set(true);
        } else {
          this.success.set(true);
        }
      },
      error: () => {
        this.loading.set(false);
        this.error.set(true);
      },
    });
  }

  toNumber(value: unknown): number {
    return Number(value);
  }

  getInitials(name: string | null): string {
    if (!name) return '?';
    const parts = name.split(' ');
    return parts.map((p) => p.charAt(0)).join('').slice(0, 2).toUpperCase();
  }

  irAlPanel(): void {
    this.router.navigate(['/panel-cliente']);
  }
}
