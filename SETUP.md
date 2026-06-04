# Guía de setup — Blisniuk & Amanov

Este documento concentra todas las instrucciones operativas que vas a necesitar para terminar de poner el sitio en producción.

---

## 1. Conectar el dominio `blisniukamanov.com` a Netlify

Pasos en orden:

1. En Netlify, abrí el sitio (`blisniukamanov.netlify.app`).
2. **Site settings → Domain management → Add custom domain → `blisniukamanov.com`**.
3. Netlify te va a dar dos opciones:
   - **a)** Cambiar los **nameservers** del dominio a los de Netlify (más simple, recomendado). Esto significa que Netlify gestiona DNS completo. Vas a tu registrador del dominio y reemplazás los nameservers actuales por los que Netlify te muestra (algo como `dns1.p01.nsone.net`, etc.). Propagación: 1 a 24 hs.
   - **b)** Dejar tu DNS donde está y crear sólo dos registros: `A @ 75.2.60.5` y `CNAME www blisniukamanov.netlify.app`. Más control pero más manual.
4. En **HTTPS / SSL**: pulsá **Verify DNS configuration → Provision certificate**. Netlify te genera SSL Let's Encrypt automático.
5. Activá **Force HTTPS** y **Pretty URLs**.

Después de propagación, el sitio responde tanto en `blisniukamanov.com` como en `www.blisniukamanov.com`. La URL Netlify queda como respaldo.

---

## 2. Activar Netlify Identity + Decap CMS

El CMS te deja editar el contenido del sitio (textos generales, viajes, destinos) desde una interfaz web sin tocar código.

### 2.1 Activar Netlify Identity

1. Netlify dashboard → tu sitio → **Identity → Enable Identity**.
2. **Settings → Registration**: cambiar de "Open" a **"Invite only"** (sólo vos y quien autorices podés entrar).
3. **Settings → External providers**: opcional, podés agregar "Login con Google" para más comodidad.
4. **Services → Git Gateway → Enable Git Gateway**. Esto permite que el CMS commiteee al repo en tu nombre.

### 2.2 Invitarte como editor

1. **Identity → Invite users → tu correo**.
2. Te llega un mail con link de aceptación. Aceptás y definís contraseña.

### 2.3 Entrar al panel del CMS

URL: **`https://blisniukamanov.com/admin/`** (o `blisniukamanov.netlify.app/admin/` antes de tener el dominio).

Vas a ver tres colecciones en el panel:

- **⚙️ Configuración del sitio** — teléfono, email, dirección, horarios, RNAV, redes sociales. Editás un solo archivo.
- **🌍 Viajes** — cada viaje es una entrada con título, eyebrow, hero image, días, precio, intro, highlights, día a día, lodges, fechas. Cuando guardás, Decap commitea al repo.
- **📍 Destinos / regiones** — cada destino con imagen, descripción y región.

### 2.4 Importante: limitación actual

Por ahora, las páginas HTML del sitio **no leen automáticamente** los archivos que genera Decap (porque el sitio es estático sin build step). En un siguiente sprint puedo:

- **Opción simple (1 h)**: agregar un script JS que en cada página lee `content/site-settings.json` y reemplaza teléfono/email/horarios. Eso ya te deja editar la info global desde el CMS.
- **Opción completa (2 días)**: migrar a Astro o Eleventy (generadores estáticos) que en cada deploy regeneran el HTML con el contenido del CMS. Esto haría que **todo** sea editable desde el panel sin tocar nada.

Cuando lo decidas, lo agendamos.

---

## 3. Recibir las consultas por correo

Cada vez que alguien complete un formulario (newsletter, contacto, modal "Hablá con un experto") se guarda en Netlify Forms. Para que además te llegue por mail:

1. Netlify dashboard → tu sitio → **Forms → Form notifications → Add notification**.
2. **Email notification**:
   - Event: **New form submission**
   - Form: **Cualquier formulario** (o segmentado por nombre)
   - Email: `info@blisniukamanov.com`
3. Save.

A partir de ahí, cada consulta te llega al correo con todos los datos del formulario.

> **Opcional**: podés configurar **Slack notification** si tu equipo trabaja en Slack — Netlify lo soporta nativo.

---

## 4. Activar Google Analytics 4 (cuando lo tengas)

1. Crear propiedad en `analytics.google.com` → te da un **Measurement ID** (`G-XXXXXXXXXX`).
2. Pasámelo y lo agrego en 2 minutos. Lo cargo en `<head>` de todas las páginas con el script oficial.
3. En el mismo commit te dejo activado el banner de cookies (cuando hay tracking, conviene tener consent).

**Mi recomendación**: si recién arrancás, podés saltearte GA4 y empezar con **Plausible** (5 USD/mes, sin cookies, privacy-friendly, dashboard más simple). Si después querés sumarle GA4, lo agregamos en paralelo.

---

## 5. ¿Sirve tener banner de cookies?

Respuesta corta: **hoy, no**. El sitio sólo usa cookies técnicas (las que el navegador setea para mantener tu sesión y enviar el formulario sin duplicar). No hay trackers, no hay pixels de Facebook, no hay GA. La ley argentina (25.326) no exige consent para cookies estrictamente necesarias.

**Sí servirá** en cualquiera de estos casos:

- Activamos Google Analytics 4 (es la razón #1).
- Sumamos pixel de Meta Ads / Google Ads.
- Empezás a vender a viajeros europeos (GDPR exige consent explícito).
- Sumás chatbot que setea cookies (Intercom, Tidio, etc).

Cuando ocurra alguno de esos, te armo banner de cookies en una mañana — está la infraestructura preparada (ya hay `cookies.html` y la política redactada).

---

## 6. Imágenes reales

Está todo documentado en **[`IMAGES.md`](./IMAGES.md)**. Te dice exactamente qué imagen va en cada lugar, qué tamaño, qué representa. Cuando subas alguna, simplemente reemplazás el archivo con el mismo nombre en `assets/img/` y Netlify redespliega.

---

## 7. Sumar más viajes

Tres caminos:

- **Hoy (manual)**: cuando me pases los datos de un viaje nuevo (título, días, precio, lodges, fechas, copy), yo te genero la página HTML siguiendo el template de `gran-migracion.html`.
- **Después de Decap integrado**: vas vos al panel, click en "🌍 Viajes → Nuevo viaje", completás los campos, guardás. El sitio se regenera solo.
- **Híbrido**: por ahora hago yo las primeras 12 desde template; cuando Decap esté integrado, vos sumás las nuevas.

---

## 8. Checklist final pre-lanzamiento

Antes de mostrar el sitio a un cliente real, dejá de tildar:

- [ ] Dominio propio funcionando con HTTPS
- [ ] Netlify Forms enviando a `info@blisniukamanov.com`
- [ ] Identity invite aceptado (vos podés entrar al `/admin`)
- [ ] Al menos 12 imágenes reales (las "prioritarias" de IMAGES.md)
- [ ] Logo real subido y reemplazando el wordmark
- [ ] Favicon definitivo (te lo armo cuando tenga el logo)
- [ ] Textos legales revisados por tu abogado (los 3 archivos `terminos.html`, `privacidad.html`, `cookies.html`)
- [ ] Una vuelta entera por todas las páginas en celular + escritorio
- [ ] Probar el envío de cada formulario con datos reales
- [ ] Si vas a usar GA4 / Plausible: instalado y testeado
- [ ] (Opcional) Cuenta de Google Search Console + sitemap enviado
