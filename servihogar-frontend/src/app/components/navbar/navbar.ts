import { Component, computed, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  readonly isLoggedIn = computed(() => this.authService.isLoggedIn());

  readonly displayName = computed(() => this.authService.displayName());

  readonly panelRoute = computed((): string | null => {
    const user = this.authService.getCurrentUser();
    if (!user) {
      return null;
    }
    if (user.tipo_usuario === 'tecnico' && user.estado_validacion !== 'validado') {
      return null;
    }
    switch (user.tipo_usuario) {
      case 'cliente':
        return '/panel-cliente';
      case 'tecnico':
        return '/panel-tecnico';
      case 'administrador':
        return '/panel-administrador';
      default:
        return null;
    }
  });

  readonly pendingMessage = computed((): string | null => {
    const user = this.authService.getCurrentUser();
    if (!this.isLoggedIn() || user?.tipo_usuario !== 'tecnico') {
      return null;
    }
    if (user.estado_validacion === 'validado') {
      return null;
    }
    return 'Tu cuenta de técnico está pendiente de validación.';
  });

  irAMiPanel(): void {
    const route = this.panelRoute();
    if (route) {
      void this.router.navigateByUrl(route);
      return;
    }

    const user = this.authService.getCurrentUser();
    if (user?.tipo_usuario === 'tecnico' && user.estado_validacion !== 'validado') {
      void this.router.navigateByUrl('/panel-tecnico');
    }
  }

  async cerrarSesion(): Promise<void> {
    await this.authService.logout();
    await this.router.navigateByUrl('/login');
  }
}
