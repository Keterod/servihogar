import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { CategoriaServicioService } from '../../services/categoria-servicio.service';
import { ZonaService } from '../../services/zona.service';
import { TecnicoService } from '../../services/tecnico.service';
import { CategoriaServicio } from '../../models/categoria-servicio';
import { Zona } from '../../models/zona';
import { Tecnico } from '../../models/tecnico';

@Component({
  selector: 'app-buscar-tecnicos',
  imports: [RouterLink],
  templateUrl: './buscar-tecnicos.html',
  styleUrl: './buscar-tecnicos.css',
})
export class BuscarTecnicos implements OnInit {
  private readonly categoriaServicioService = inject(CategoriaServicioService);
  private readonly zonaService = inject(ZonaService);
  private readonly tecnicoService = inject(TecnicoService);

  readonly loading = signal(true);
  readonly error = signal(false);
  readonly categorias = signal<CategoriaServicio[]>([]);
  readonly zonas = signal<Zona[]>([]);
  readonly calificaciones = [
    { valor: 0, etiqueta: 'Todas' },
    { valor: 3.5, etiqueta: '3.5+' },
    { valor: 4, etiqueta: '4.0+' },
    { valor: 4.5, etiqueta: '4.5+' },
  ];

  readonly categoriaFiltro = signal('');
  readonly zonaFiltro = signal('');
  readonly calificacionMinima = signal(0);
  readonly nombreBusqueda = signal('');

  private readonly tecnicos = signal<Tecnico[]>([]);

  readonly tecnicosFiltrados = computed(() => {
    const busqueda = this.nombreBusqueda().trim().toLowerCase();
    const categoria = this.categoriaFiltro();
    const zona = this.zonaFiltro();

    return this.tecnicos().filter((tecnico) => {
      if (
        this.calificacionMinima() > 0 &&
        (tecnico.calificacion === null || tecnico.calificacion < this.calificacionMinima())
      ) {
        return false;
      }
      if (categoria && !tecnico.categorias.some((c) => c.nombre === categoria)) {
        return false;
      }
      if (zona && !tecnico.zonas.some((z) => z.nombre === zona)) {
        return false;
      }
      if (busqueda) {
        const nombreCompleto = `${tecnico.nombres} ${tecnico.apellidos}`.toLowerCase();
        if (!nombreCompleto.includes(busqueda)) {
          return false;
        }
      }
      return true;
    });
  });

  ngOnInit(): void {
    forkJoin({
      categorias: this.categoriaServicioService.obtenerCategorias(),
      zonas: this.zonaService.obtenerZonas(),
      tecnicos: this.tecnicoService.obtenerTecnicos(),
    }).subscribe({
      next: ({ categorias, zonas, tecnicos }) => {
        this.categorias.set(categorias);
        this.zonas.set(zonas);
        this.tecnicos.set(tecnicos);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }

  onCategoriaChange(event: Event): void {
    this.categoriaFiltro.set((event.target as HTMLSelectElement).value);
  }

  onZonaChange(event: Event): void {
    this.zonaFiltro.set((event.target as HTMLSelectElement).value);
  }

  onCalificacionChange(event: Event): void {
    this.calificacionMinima.set(Number((event.target as HTMLSelectElement).value));
  }

  onNombreBusquedaChange(event: Event): void {
    this.nombreBusqueda.set((event.target as HTMLInputElement).value);
  }

  getIniciales(nombre: string): string {
    return nombre
      .split(' ')
      .map((parte) => parte.charAt(0))
      .join('')
      .slice(0, 2)
      .toUpperCase();
  }
}
