# Estrategia: responsive, funcionalidades y deploy

Este documento explica tres cosas: cómo se adapta el sitio a distintos dispositivos, qué interacciones tiene y cómo subirlo a una web real.

---

## 1. Responsive (la palabra que buscabas)

**Responsive design** = el mismo HTML/CSS se adapta automáticamente al tamaño de la pantalla. Sin "versión móvil" separada: una sola web que reorganiza columnas, tipografías y espacios según el ancho.

### Cómo está hecho acá

`styles.css` define breakpoints en tres anchos:

| Breakpoint | Pensado para | Qué cambia |
|---|---|---|
| `> 1100px` | Desktop / laptop | Layout completo (5–6 columnas, hero a sangre) |
| `≤ 1100px` | Tablet horizontal | Grids reducen a 3–4 columnas, hero split colapsa a 1 columna, sidebar de filtros se vuelve estática |
| `≤ 800px` | Tablet vertical / móvil grande | 2 columnas máximo, header se reduce a hamburger + wordmark + búsqueda, las stat-cards del journey hero pasan a 2x2 abajo del hero |
| `≤ 520px` | Móvil estándar | Una columna, formularios apilados, día-a-día con número más pequeño, footer en columna única |

**Verificalo vos:**
- `_compare/04-home-mobile.png` (homepage 414px)
- `_compare/07-small-group-mobile.png`
- `_compare/08-gran-migracion-mobile.png`
- `_compare/09-destinations-mobile.png`

### Qué falta pulir en mobile

- El hamburguesa abre el drawer correctamente (probado en `script.js`), pero podríamos añadir un sub-acordeón para "Destinos" → "África / Asia / …".
- Las tablas de fechas en `gran-migracion.html` se ven apretadas en 360px. Sería mejor pasarlas a un layout de "tarjetas apiladas" cuando el ancho < 520px.
- La fila de stats absolutas que sobresale del hero (4 columnas) se rebaja a 2x2 en mobile, pero podríamos directamente convertirla en una lista `<dl>` para ahorrar espacio vertical.

---

## 2. Funcionalidad

### Lo que ya está vivo en `script.js`

| Componente | Comportamiento |
|---|---|
| **Header sticky** | Sombra sutil aparece al scrollear (`.scrolled`) |
| **Menú móvil** | Hamburguesa abre drawer, ESC o tap fuera lo cierra, body se bloquea |
| **Hero spotlight** | Crossfade automático cada 7s + flechas manuales que reinician el timer |
| **Tabs "¿A dónde te llevamos?"** | Resaltan al click; preparado para mostrar/ocultar paneles `.tab-panel` |
| **Tabs de filtro recomendaciones** | Resaltan al click y disparan un flash de la lista |
| **Acordeones (Buena información, filtros, "no incluye")** | Funcionan nativos con `<details>` — sin JS, abren/cierran con animación CSS |
| **Filtros del sidebar** | Click sobre cualquier opción la marca como check (cuadradito cobre con tilde) y suma el contador al header del grupo: `Regiones (3)` |
| **Botón "Filtrar"** | En mobile abre/cierra el sidebar y hace scroll hasta él |
| **Newsletter / formulario de contacto** | Validan email, simulan envío y muestran un toast cobre o rojo |
| **Tabla "Reservar"** | El click muestra toast "tu solicitud para la salida del 14 marzo se envió a tu asesor" |
| **Subnav scroll-spy** | El enlace activo se resalta automáticamente según en qué sección estés |
| **Scroll smooth** | Anchor links offsetean por la altura del header |
| **Reveal on scroll** | Las cards aparecen con fade-up cuando entran al viewport |

### Lo que aún no funciona "de verdad"

- **Los formularios no envían a ningún sitio**. El `submit` está interceptado en JS y muestra un toast — no hay backend. Para que llegue a un correo de verdad hay que conectarlo a un servicio (siguiente sección).
- **Filtros del sidebar son visuales**: marcan como activos, cuentan, pero no filtran tarjetas. Para filtrar de verdad hay que asignar `data-tags` a cada `.j-card` y filtrar en JS según las activas.
- **Buscador del header** redirige a `journeys.html` pero no aplica búsqueda. Habría que pasar `?q=...` y leer el query param.
- **Tabs del homepage** sólo tienen un panel (`loved`); los otros tres (`now`, `offers`, `new`) no existen como contenido. Habría que duplicar el panel con cards distintas para cada uno.

---

## 3. Despliegue (subirlo a una web real)

El proyecto es un **sitio estático**: sólo HTML, CSS, JS e imágenes. Eso facilita mucho el deploy. No hace falta servidor ni base de datos.

### Opción recomendada: **Netlify** o **Cloudflare Pages**

Las dos son gratuitas para uso personal e incluyen:
- HTTPS automático
- CDN global (carga rápido desde cualquier país)
- Conexión directa a GitHub: cada `git push` redespliega el sitio
- Soporte de **forms** sin backend (Netlify Forms con un atributo HTML)
- Subdominio gratis (`blisniukamanov.netlify.app`) y posibilidad de conectar dominio propio

**Pasos para Netlify (15 minutos):**

1. Cuenta en [netlify.com](https://netlify.com) (free tier)
2. **"Add new site" → "Import an existing project" → GitHub**
3. Seleccionás `brianblisniuk/blisniukamanov` y la rama `claude/recreate-website-design-anwpt`
4. Build settings: dejarlo vacío (no hay build), publish directory: `/`
5. Deploy → en 30s tenés URL pública
6. **Para los formularios**, sólo agregar `netlify` como atributo:
   ```html
   <form class="newsletter" netlify name="newsletter">
   ```
   Netlify intercepta el submit y los mensajes aparecen en su dashboard. Puede reenviarlos a tu correo.

### Opción 2: **GitHub Pages** (más básico, gratis)

- En GitHub: **Settings → Pages → Branch: `claude/recreate-website-design-anwpt` → Save**
- En 1–2 minutos: `https://brianblisniuk.github.io/blisniukamanov/`
- ❌ No tiene soporte de formularios. Habría que conectar **Formspree** (free para 50 envíos/mes) o **Web3Forms**:
  ```html
  <form action="https://formspree.io/f/TU_ID" method="POST">
  ```

### Opción 3: **Vercel**

Igual de bueno que Netlify, también gratis. Mejor si en el futuro quisieras pasar a Next.js.

### Para conectar tu propio dominio

1. Comprar dominio en Namecheap, GoDaddy, Cloudflare Registrar (~10 €/año)
2. En el panel de Netlify/Vercel: **Domain settings → Add custom domain**
3. Te dan dos registros DNS (A y CNAME) que cargás en el panel del registrador
4. En 10 minutos a 24 h: tu sitio en `blisniukamanov.com`

---

## 4. Mejoras antes de mostrarlo a clientes reales

| Prioridad | Tarea | Esfuerzo |
|---|---|---|
| 🔴 alta | **Reemplazar imágenes proceduales por fotos reales**. Las gradientes funcionan para diseñar pero no venden. Comprar pack en Unsplash+, contratar fotógrafo o pedirlas al cliente. | 2-4h |
| 🔴 alta | Conectar **Netlify Forms** o Formspree al newsletter, suscripción y "Solicitar catálogo". | 30 min |
| 🟡 media | Optimizar imágenes: convertir a WebP, generar variantes responsive (`srcset`). Ahorra ~70% del peso. | 2h |
| 🟡 media | **SEO**: agregar `<meta og:image>`, `<meta og:title>`, sitemap.xml, robots.txt | 1h |
| 🟡 media | Filtros funcionales en el explorer (con `data-tags` en cada `.j-card`) | 2h |
| 🟢 baja | Si hay > 50 viajes, migrar a un generador estático (Astro o Eleventy) que monte cada `j-card` desde una hoja de cálculo o markdown | 1-2 días |
| 🟢 baja | Sistema de contenido (CMS) sin backend: **Decap CMS** o **TinaCMS**, libre, edita Markdown directamente en el repo | 1 día |
| 🟢 baja | Analytics: **Plausible** (privacy-friendly, ~5 €/mes) o **GA4** gratis | 15 min |

---

## 5. Para no salir del flujo actual

Cada vez que termino una pasada de cambios:

1. Editamos HTML/CSS/JS
2. Corremos:
   ```bash
   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node tools/screenshot.js
   ```
3. Las PNG nuevas viven en `_compare/`
4. Commit + push → si conectaste Netlify, en 30s ya está online

Cuando me digas "estoy listo para enseñárselo a clientes" hacemos un sprint para los 5 puntos de prioridad alta y media de la tabla de arriba.
