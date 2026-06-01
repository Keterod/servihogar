import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-solicitud-servicio',
  imports: [],
  templateUrl: './solicitud-servicio.html',
  styleUrl: './solicitud-servicio.css',
})
export class SolicitudServicio {
  readonly categorias = [
    'Gasfitería menor',
    'Electricidad básica',
    'Mantenimiento de computadoras',
    'Pintura básica',
    'Armado de muebles',
  ];

  readonly zonas = ['Huancayo Centro', 'El Tambo', 'Chilca', 'San Carlos'];

  readonly horarios = ['Mañana (8am-12pm)', 'Tarde (12pm-5pm)', 'Noche (5pm-8pm)'];

  categoria = signal('');
  zona = signal('');
  descripcion = signal('');
  fechaTentativa = signal('');
  horarioPreferido = signal('');
  direccion = signal('');

  enviado = signal(false);

  constructor(private router: Router) {}

  enviarSolicitud(): void {
    this.enviado.set(true);
  }

  irAlPanel(): void {
    this.router.navigate(['/panel-cliente']);
  }
}
