import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = async () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  await auth.whenReady();

  if (!auth.isAuthenticated()) {
    return router.createUrlTree(['/login']);
  }

  return true;
};

export const clienteGuard: CanActivateFn = async () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  await auth.whenReady();

  if (!auth.isAuthenticated()) {
    return router.createUrlTree(['/login']);
  }

  return auth.getCurrentUser()?.tipo_usuario === 'cliente'
    ? true
    : router.createUrlTree(['/login']);
};

export const tecnicoValidadoGuard: CanActivateFn = async () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  await auth.whenReady();

  if (!auth.isAuthenticated()) {
    return router.createUrlTree(['/login']);
  }

  const profile = auth.getCurrentUser();
  const isValidatedTechnician =
    profile?.tipo_usuario === 'tecnico' && profile.estado_validacion === 'validado';

  return isValidatedTechnician ? true : router.createUrlTree(['/login']);
};

export const adminGuard: CanActivateFn = async () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  await auth.whenReady();

  if (!auth.isAuthenticated()) {
    return router.createUrlTree(['/login']);
  }

  return auth.getCurrentUser()?.tipo_usuario === 'administrador'
    ? true
    : router.createUrlTree(['/login']);
};
