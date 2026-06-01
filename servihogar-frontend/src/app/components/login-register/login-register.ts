import { Component } from '@angular/core';

type ModoPantalla = 'login' | 'register';
type RolUsuario = 'cliente' | 'tecnico';

@Component({
  selector: 'app-login-register',
  imports: [],
  templateUrl: './login-register.html',
  styleUrl: './login-register.css',
})
export class LoginRegister {
  modo: ModoPantalla = 'login';
  rol: RolUsuario = 'cliente';

  setModo(modo: ModoPantalla): void {
    this.modo = modo;
  }

  setRol(rol: RolUsuario): void {
    this.rol = rol;
  }

  get tituloFormulario(): string {
    if (this.modo === 'login') {
      return this.rol === 'cliente' ? 'Iniciar sesión como cliente' : 'Iniciar sesión como técnico';
    }
    return this.rol === 'cliente' ? 'Crear cuenta de cliente' : 'Crear cuenta de técnico';
  }

  get textoBoton(): string {
    return this.modo === 'login' ? 'Iniciar sesión' : 'Crear cuenta';
  }
}
