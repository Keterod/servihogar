import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

interface TecnicoSimulado {
  id: number;
  nombre: string;
  especialidad: string;
  categoria: string;
  zona: string;
  valoracion: number;
}

const CATEGORIAS_OFICIALES = [
  'Gasfitería menor',
  'Electricidad básica',
  'Mantenimiento de computadoras',
  'Pintura básica',
  'Armado de muebles',
] as const;

const TECNICOS_SIMULADOS: TecnicoSimulado[] = [
  {
    id: 1,
    nombre: 'Carlos Mendoza',
    especialidad: 'Gasfitería menor',
    categoria: 'Gasfitería menor',
    zona: 'Huancayo Centro',
    valoracion: 4.8,
  },
  {
    id: 2,
    nombre: 'Ana Ruiz',
    especialidad: 'Electricidad básica',
    categoria: 'Electricidad básica',
    zona: 'El Tambo',
    valoracion: 4.5,
  },
  {
    id: 3,
    nombre: 'Luis Torres',
    especialidad: 'Pintura básica',
    categoria: 'Pintura básica',
    zona: 'Chilca',
    valoracion: 4.2,
  },
  {
    id: 4,
    nombre: 'María Gómez',
    especialidad: 'Armado de muebles',
    categoria: 'Armado de muebles',
    zona: 'Huancayo Centro',
    valoracion: 4.9,
  },
  {
    id: 5,
    nombre: 'Pedro Sánchez',
    especialidad: 'Mantenimiento de computadoras',
    categoria: 'Mantenimiento de computadoras',
    zona: 'El Tambo',
    valoracion: 3.8,
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

  categoriaFiltro = '';
  zonaFiltro = '';
  calificacionMinima = 0;

  private readonly tecnicos = TECNICOS_SIMULADOS;

  get tecnicosFiltrados(): TecnicoSimulado[] {
    return this.tecnicos.filter((tecnico) => {
      if (this.categoriaFiltro && tecnico.categoria !== this.categoriaFiltro) {
        return false;
      }
      if (this.zonaFiltro && tecnico.zona !== this.zonaFiltro) {
        return false;
      }
      if (this.calificacionMinima > 0 && tecnico.valoracion < this.calificacionMinima) {
        return false;
      }
      return true;
    });
  }

  onCategoriaChange(event: Event): void {
    this.categoriaFiltro = (event.target as HTMLSelectElement).value;
  }

  onZonaChange(event: Event): void {
    this.zonaFiltro = (event.target as HTMLSelectElement).value;
  }

  onCalificacionChange(event: Event): void {
    this.calificacionMinima = Number((event.target as HTMLSelectElement).value);
  }
}
