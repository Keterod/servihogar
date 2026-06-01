import { Routes } from '@angular/router';

import { BuscarTecnicos } from './components/buscar-tecnicos/buscar-tecnicos';
import { DetalleSolicitud } from './components/detalle-solicitud/detalle-solicitud';
import { Home } from './components/home/home';
import { LoginRegister } from './components/login-register/login-register';
import { PanelAdministrador } from './components/panel-administrador/panel-administrador';
import { PanelCliente } from './components/panel-cliente/panel-cliente';
import { PanelTecnico } from './components/panel-tecnico/panel-tecnico';
import { PerfilTecnico } from './components/perfil-tecnico/perfil-tecnico';
import { SolicitudServicio } from './components/solicitud-servicio/solicitud-servicio';
import { ValorarServicio } from './components/valorar-servicio/valorar-servicio';

export const routes: Routes = [
  { path: '', redirectTo: '/inicio', pathMatch: 'full' },
  { path: 'inicio', component: Home },
  { path: 'buscar-tecnicos', component: BuscarTecnicos },
  { path: 'perfil-tecnico', component: PerfilTecnico },
  { path: 'login', component: LoginRegister },
  { path: 'solicitud-servicio', component: SolicitudServicio },
  { path: 'panel-cliente', component: PanelCliente },
  { path: 'detalle-solicitud', component: DetalleSolicitud },
  { path: 'valorar-servicio', component: ValorarServicio },
  { path: 'panel-tecnico', component: PanelTecnico },
  { path: 'panel-administrador', component: PanelAdministrador },
];
