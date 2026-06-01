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

const TECNICOS_SIMULADOS: TecnicoSimulado[] = [
  {
    id: 1,
    nombre: 'Carlos Mendoza',
    especialidad: 'Fontanería general',
    categoria: 'Fontanería',
    zona: 'Norte',
    valoracion: 4.8,
  },
  {
    id: 2,
    nombre: 'Ana Ruiz',
    especialidad: 'Instalaciones eléctricas',
    categoria: 'Electricidad',
    zona: 'Centro',
    valoracion: 4.5,
  },
  {
    id: 3,
    nombre: 'Luis Torres',
    especialidad: 'Cerrajería y seguridad',
    categoria: 'Cerrajería',
    zona: 'Sur',
    valoracion: 4.2,
  },
  {
    id: 4,
    nombre: 'María Gómez',
    especialidad: 'Limpieza del hogar',
    categoria: 'Limpieza',
    zona: 'Norte',
    valoracion: 4.9,
  },
  {
    id: 5,
    nombre: 'Pedro Sánchez',
    especialidad: 'Reparaciones eléctricas',
    categoria: 'Electricidad',
    zona: 'Sur',
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
  readonly categorias = ['', 'Fontanería', 'Electricidad', 'Cerrajería', 'Limpieza'];
  readonly zonas = ['', 'Norte', 'Centro', 'Sur'];
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
