import { Component, inject, signal } from '@angular/core';
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

  readonly isLoggedIn = this.authService.isLoggedIn;
  readonly displayName = this.authService.displayName;
  readonly panelRoute = this.authService.panelRoute;
  readonly isPendingTechnician = this.authService.isPendingTechnician;
  readonly pendingMessage = signal<string | null>(null);

  irAMiPanel(): void {
    const route = this.panelRoute();
    if (route) {
      void this.router.navigateByUrl(route);
      return;
    }
    if (this.isPendingTechnician()) {
      this.pendingMessage.set('Tu cuenta de técnico está pendiente de validación.');
    }
  }

  async cerrarSesion(): Promise<void> {
    this.pendingMessage.set(null);
    await this.authService.logout();
    await this.router.navigateByUrl('/login');
  }
}
