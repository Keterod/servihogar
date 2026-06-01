import { Component, computed, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

interface TecnicoSimulado {
  id: number;
  nombre: string;
  especialidad: string;
  categoria: string;
  zona: string;
  valoracion: number;
  servicios: number;
  perfilValidado?: boolean;
}

const CATEGORIAS_OFICIALES = [
  'Gasfitería menor',
  'Electricidad básica',
  'Mantenimiento de PC',
  'Armado de muebles',
  'Pintura básica',
  'Reparaciones menores',
] as const;

const TECNICOS_SIMULADOS: TecnicoSimulado[] = [
  {
    id: 1,
    nombre: 'Carlos Mendoza',
    especialidad: 'Gasfitería menor',
    categoria: 'Gasfitería menor',
    zona: 'Huancayo Centro',
    valoracion: 4.8,
    servicios: 42,
    perfilValidado: true,
  },
  {
    id: 2,
    nombre: 'Ana Ramírez',
    especialidad: 'Electricidad básica',
    categoria: 'Electricidad básica',
    zona: 'El Tambo',
    valoracion: 4.5,
    servicios: 28,
  },
  {
    id: 3,
    nombre: 'Roberto Salas',
    especialidad: 'Gasfitería menor',
    categoria: 'Gasfitería menor',
    zona: 'Chilca',
    valoracion: 4.2,
    servicios: 15,
  },
  {
    id: 4,
    nombre: 'María Gómez',
    especialidad: 'Pintura básica',
    categoria: 'Pintura básica',
    zona: 'Huancayo Centro',
    valoracion: 4.9,
    servicios: 36,
  },
  {
    id: 5,
    nombre: 'Pedro Sánchez',
    especialidad: 'Mantenimiento de PC',
    categoria: 'Mantenimiento de PC',
    zona: 'El Tambo',
    valoracion: 3.8,
    servicios: 19,
  },
];

@Component({
  selector: 'app-buscar-tecnicos',
  imports: [RouterLink],
  templateUrl: './buscar-tecnicos.html',
  styleUrl: './buscar-tecnicos.css',
})
export class BuscarTecnicos {
  readonly categorias = ['', ...CATEGORIAS_OFICIALES];
  readonly zonas = ['', 'Huancayo Centro', 'El Tambo', 'Chilca'];
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

  private readonly tecnicos = signal(TECNICOS_SIMULADOS);

  readonly tecnicosFiltrados = computed(() => {
    const busqueda = this.nombreBusqueda().trim().toLowerCase();
    return this.tecnicos().filter((tecnico) => {
      if (this.categoriaFiltro() && tecnico.categoria !== this.categoriaFiltro()) {
        return false;
      }
      if (this.zonaFiltro() && tecnico.zona !== this.zonaFiltro()) {
        return false;
      }
      if (this.calificacionMinima() > 0 && tecnico.valoracion < this.calificacionMinima()) {
        return false;
      }
      if (busqueda && !tecnico.nombre.toLowerCase().includes(busqueda)) {
        return false;
      }
      return true;
    });
  });

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
