import { Component, computed, signal } from '@angular/core';

type ModoPantalla = 'login' | 'register';
type RolUsuario = 'cliente' | 'tecnico';

@Component({
  selector: 'app-login-register',
  imports: [],
  templateUrl: './login-register.html',
  styleUrl: './login-register.css',
})
export class LoginRegister {
  readonly modo = signal<ModoPantalla>('login');
  readonly rol = signal<RolUsuario>('cliente');

  readonly tituloFormulario = computed(() => {
    if (this.modo() === 'login') {
      return this.rol() === 'cliente'
        ? 'Iniciar sesión como cliente'
        : 'Iniciar sesión como técnico';
    }
    return this.rol() === 'cliente' ? 'Crear cuenta de cliente' : 'Crear cuenta de técnico';
  });

  readonly textoBoton = computed(() =>
    this.modo() === 'login' ? 'Iniciar sesión' : 'Crear cuenta'
  );

  setModo(modo: ModoPantalla): void {
    this.modo.set(modo);
  }

  setRol(rol: RolUsuario): void {
    this.rol.set(rol);
  }
}
