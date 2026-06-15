import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { TecnicoPerfil } from '../../models/tecnico';
import { AuthService } from '../../services/auth.service';
import { TecnicoService } from '../../services/tecnico.service';

@Component({
  selector: 'app-perfil-tecnico',
  imports: [],
  templateUrl: './perfil-tecnico.html',
  styleUrl: './perfil-tecnico.css',
})
export class PerfilTecnico implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly authService = inject(AuthService);
  private readonly tecnicoService = inject(TecnicoService);

  readonly loading = signal<boolean>(true);
  readonly error = signal<string | null>(null);
  readonly notFound = signal<boolean>(false);
  readonly tecnico = signal<TecnicoPerfil | null>(null);
  readonly mensajeSolicitud = signal<string | null>(null);

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
        this.error.set('No se pudo conectar con el servidor. Intenta nuevamente más tarde.');
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

  async solicitarCotizacion(tecnico: TecnicoPerfil): Promise<void> {
    this.mensajeSolicitud.set(null);
    await this.authService.whenReady();

    if (!this.authService.isLoggedIn()) {
      await this.router.navigate(['/login']);
      return;
    }

    const perfil = this.authService.getCurrentUser();
    if (perfil?.tipo_usuario !== 'cliente') {
      this.mensajeSolicitud.set('Solo los clientes registrados pueden solicitar servicios.');
      return;
    }

    await this.router.navigate(['/solicitud-servicio'], {
      queryParams: {
        tecnicoId: tecnico.id_tecnico,
        tecnicoNombre: `${tecnico.nombres} ${tecnico.apellidos}`,
        ...(tecnico.categorias[0]?.id_categoria
          ? { categoriaId: tecnico.categorias[0].id_categoria }
          : {}),
      },
    });
  }
}
