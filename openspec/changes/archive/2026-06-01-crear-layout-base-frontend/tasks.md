## 1. Estilos globales y documento base

- [x] 1.1 Agregar reset mínimo, variables CSS (`:root`) y estilos base en `servihogar-frontend/src/styles.css`
- [x] 1.2 Actualizar `servihogar-frontend/src/index.html`: `lang="es"` y título `ServiHogar`

## 2. Componente Footer

- [x] 2.1 Crear `servihogar-frontend/src/app/components/footer/footer.ts` como componente standalone
- [x] 2.2 Crear `footer.html` con nombre del proyecto y mención académica estática
- [x] 2.3 Crear `footer.css` con estilos del pie de página

## 3. Componente Navbar

- [x] 3.1 Crear `servihogar-frontend/src/app/components/navbar/navbar.ts` como componente standalone
- [x] 3.2 Crear `navbar.html` con logo/nombre ServiHogar y enlaces: Inicio (`/inicio`), Buscar técnicos (`/buscar-tecnicos`), Iniciar sesión (`/login`)
- [x] 3.3 Importar `RouterLink` y `RouterLinkActive` en el navbar; aplicar clase `.active` al enlace de la ruta activa
- [x] 3.4 Crear `navbar.css` con estilos de navegación y estado activo
- [x] 3.5 Verificar que no hay enlaces a paneles (cliente, técnico, administrador) en el navbar

## 4. Integración del shell en App

- [x] 4.1 Actualizar `app.ts` para importar componentes `Navbar` y `Footer`
- [x] 4.2 Actualizar `app.html` con estructura: navbar → `<main>` con `<router-outlet />` → footer
- [x] 4.3 Actualizar `app.css` con layout flex column (`min-height: 100dvh`, `main` con `flex: 1`)

## 5. Verificación

- [x] 5.1 Ejecutar `npm run build` y confirmar compilación sin errores
- [x] 5.2 Probar navegación SPA entre Inicio, Buscar técnicos e Iniciar sesión desde el navbar
- [x] 5.3 Confirmar enlace activo visible y layout responsive básico en viewport ~375px
- [x] 5.4 Confirmar que rutas de paneles (`/panel-cliente`, `/panel-tecnico`, `/panel-administrador`) siguen accesibles por URL directa
