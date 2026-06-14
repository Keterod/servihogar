import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/inicio', pathMatch: 'full' },
  { path: 'inicio', loadComponent: () => import('./components/home/home').then((m) => m.Home) },
  {
    path: 'buscar-tecnicos',
    loadComponent: () =>
      import('./components/buscar-tecnicos/buscar-tecnicos').then((m) => m.BuscarTecnicos),
  },
  {
    path: 'perfil-tecnico',
    loadComponent: () =>
      import('./components/perfil-tecnico/perfil-tecnico').then((m) => m.PerfilTecnico),
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./components/login-register/login-register').then((m) => m.LoginRegister),
  },
  {
    path: 'solicitud-servicio',
    loadComponent: () =>
      import('./components/solicitud-servicio/solicitud-servicio').then((m) => m.SolicitudServicio),
  },
  {
    path: 'panel-cliente',
    loadComponent: () =>
      import('./components/panel-cliente/panel-cliente').then((m) => m.PanelCliente),
  },
  {
    path: 'detalle-solicitud',
    loadComponent: () =>
      import('./components/detalle-solicitud/detalle-solicitud').then((m) => m.DetalleSolicitud),
  },
  {
    path: 'valorar-servicio',
    loadComponent: () =>
      import('./components/valorar-servicio/valorar-servicio').then((m) => m.ValorarServicio),
  },
  {
    path: 'panel-tecnico',
    loadComponent: () =>
      import('./components/panel-tecnico/panel-tecnico').then((m) => m.PanelTecnico),
  },
  {
    path: 'panel-administrador',
    loadComponent: () =>
      import('./components/panel-administrador/panel-administrador').then((m) => m.PanelAdministrador),
  },
];
