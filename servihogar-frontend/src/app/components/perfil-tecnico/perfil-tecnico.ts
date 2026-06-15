import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { TecnicoService } from '../../services/tecnico.service';
import { TecnicoDetalle } from '../../models/tecnico';

interface RatingBar {
  etiqueta: string;
  porcentaje: number;
}

@Component({
  selector: 'app-perfil-tecnico',
  imports: [RouterLink],
  templateUrl: './perfil-tecnico.html',
  styleUrl: './perfil-tecnico.css',
})
export class PerfilTecnico implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly tecnicoService = inject(TecnicoService);

  readonly loading = signal(true);
  readonly error = signal(false);
  readonly notFound = signal(false);
  readonly tecnico = signal<TecnicoDetalle | null>(null);

  readonly ratingBars: RatingBar[] = [
    { etiqueta: 'Puntualidad', porcentaje: 92 },
    { etiqueta: 'Calidad del trabajo', porcentaje: 96 },
    { etiqueta: 'Trato al cliente', porcentaje: 88 },
    { etiqueta: 'Limpieza', porcentaje: 85 },
    { etiqueta: 'Cumplimiento de precio', porcentaje: 90 },
  ];

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.notFound.set(true);
      this.loading.set(false);
      return;
    }
    this.tecnicoService.obtenerTecnicoPorId(id).subscribe({
      next: (data) => {
        if (data === null) {
          this.notFound.set(true);
        } else {
          this.tecnico.set(data);
        }
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
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
