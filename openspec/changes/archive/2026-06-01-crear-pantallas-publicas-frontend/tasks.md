## 1. Página de inicio (home)

- [x] 1.1 Definir datos simulados en `home.ts` (categorías destacadas y cuatro pasos del flujo real de ServiHogar)
- [x] 1.2 Implementar `home.html`: hero con propósito, categorías destacadas, pasos (buscar → revisar perfiles → publicar solicitud → técnicos cotizan) y CTA a `/buscar-tecnicos`
- [x] 1.3 Crear `home.css` con diseño responsive reutilizando variables globales

## 2. Búsqueda de técnicos (buscar-tecnicos)

- [x] 2.1 Definir array de técnicos simulados y opciones de filtros (categoría, zona, calificación) en `buscar-tecnicos.ts`
- [x] 2.2 Implementar filtrado funcional mínimo en memoria al cambiar los filtros
- [x] 2.3 Implementar `buscar-tecnicos.html`: filtros y tarjetas de técnicos filtrados
- [x] 2.4 Añadir navegación con `routerLink` desde cada tarjeta hacia `/perfil-tecnico`
- [x] 2.5 Crear `buscar-tecnicos.css` con grid/listado responsive

## 3. Perfil del técnico (perfil-tecnico)

- [x] 3.1 Definir objeto de técnico simulado en `perfil-tecnico.ts` (nombre, especialidad, experiencia, zona, valoración)
- [x] 3.2 Implementar `perfil-tecnico.html`: información completa, botón **Solicitar servicio** y texto auxiliar *Inicia sesión como cliente para continuar*
- [x] 3.3 Configurar botón con `routerLink` hacia `/login` (sin acción de cotización)
- [x] 3.4 Crear `perfil-tecnico.css` con diseño responsive

## 4. Iniciar sesión / Crear cuenta (login-register)

- [x] 4.1 Implementar `login-register.ts` con estado para pestañas (Iniciar sesión / Crear cuenta) y selector de rol (cliente / técnico)
- [x] 4.2 Implementar `login-register.html`: una sola pantalla con pestañas, roles y formularios visuales sin submit funcional
- [x] 4.3 Verificar que no hay opción de registro o login para administrador
- [x] 4.4 Crear `login-register.css` con diseño responsive para pestañas y formulario

## 5. Verificación

- [x] 5.1 Ejecutar `npm run build` y confirmar compilación sin errores
- [x] 5.2 Probar flujo: inicio → buscar técnicos (filtros en memoria) → perfil técnico → login
- [x] 5.3 Confirmar CTA "Solicitar servicio" navega a `/login` con texto auxiliar visible
- [x] 5.4 Confirmar pestañas Iniciar sesión / Crear cuenta y roles cliente/técnico en una sola pantalla
- [x] 5.5 Confirmar ausencia de registro/login de administrador
- [x] 5.6 Confirmar navbar sigue navegando a Inicio, Buscar técnicos e Iniciar sesión
- [x] 5.7 Confirmar diseño responsive básico en viewport ~375px en las cuatro pantallas
