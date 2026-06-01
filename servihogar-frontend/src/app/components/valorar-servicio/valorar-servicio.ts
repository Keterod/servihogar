import { Component, signal, computed } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-valorar-servicio',
  imports: [RouterLink],
  templateUrl: './valorar-servicio.html',
  styleUrl: './valorar-servicio.css',
})
export class ValorarServicio {
  readonly opcionesCalificacion = [1, 2, 3, 4, 5];

  puntualidad = signal(0);
  calidad = signal(0);
  trato = signal(0);
  limpieza = signal(0);
  cumplimientoPrecio = signal(0);

  comentario = signal('');
  volveriaContratar = signal(false);

  enviado = signal(false);

  readonly promedio = computed(() => {
    const valores = [
      this.puntualidad(),
      this.calidad(),
      this.trato(),
      this.limpieza(),
      this.cumplimientoPrecio(),
    ];
    const suma = valores.reduce((a, b) => a + b, 0);
    const cantidad = valores.filter((v) => v > 0).length;
    return cantidad > 0 ? (suma / cantidad).toFixed(1) : '0.0';
  });

  readonly todosCalificados = computed(() =>
    [this.puntualidad(), this.calidad(), this.trato(), this.limpieza(), this.cumplimientoPrecio()].every(
      (v) => v > 0
    )
  );

  constructor(private router: Router) {}

  setPuntualidad(valor: number): void {
    this.puntualidad.set(valor);
  }

  setCalidad(valor: number): void {
    this.calidad.set(valor);
  }

  setTrato(valor: number): void {
    this.trato.set(valor);
  }

  setLimpieza(valor: number): void {
    this.limpieza.set(valor);
  }

  setCumplimientoPrecio(valor: number): void {
    this.cumplimientoPrecio.set(valor);
  }

  enviarValoracion(): void {
    this.enviado.set(true);
  }

  irAlPanel(): void {
    this.router.navigate(['/panel-cliente']);
  }
}
