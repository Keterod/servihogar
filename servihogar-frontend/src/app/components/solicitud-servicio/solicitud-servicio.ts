import { Component, computed, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-solicitud-servicio',
  imports: [RouterLink],
  templateUrl: './solicitud-servicio.html',
  styleUrl: './solicitud-servicio.css',
})
export class SolicitudServicio {
  readonly categorias = [
    'Gasfitería menor',
    'Electricidad básica',
    'Mantenimiento de PC',
    'Armado de muebles',
    'Pintura básica',
    'Reparaciones menores',
  ];

  readonly zonas = ['Huancayo Centro', 'El Tambo', 'Chilca', 'San Carlos'];

  readonly horarios = ['Mañana (8am-12pm)', 'Tarde (12pm-5pm)', 'Noche (5pm-8pm)'];

  readonly categoria = signal('');
  readonly zona = signal('');
  readonly descripcion = signal('');
  readonly fechaTentativa = signal('');
  readonly horarioPreferido = signal('');
  readonly direccion = signal('');

  readonly enviado = signal(false);

  readonly puedeEnviar = computed(
    () =>
      this.categoria().trim() !== '' &&
      this.zona().trim() !== '' &&
      this.descripcion().trim() !== '' &&
      this.fechaTentativa().trim() !== '' &&
      this.horarioPreferido().trim() !== '' &&
      this.direccion().trim() !== ''
  );

  constructor(private router: Router) {}

  enviarSolicitud(): void {
    if (!this.puedeEnviar()) {
      return;
    }
    this.enviado.set(true);
  }

  irAlPanel(): void {
    this.router.navigate(['/panel-cliente']);
  }
}
