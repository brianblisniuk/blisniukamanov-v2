# Brand Kit · Blisniuk & Amanov

Documento canónico de identidad visual y de marca. Actualizar acá cuando cambie algo de design system.

---

## 🅰️ Logo

| Variante | Archivo | Dimensiones | Color | Uso |
|---|---|---|---|---|
| Horizontal (wordmark) | `assets/img/logo-horizontal.svg` | 1800×240 (ratio 7.5:1) | `#141414` | Headers, materiales sobre fondo claro |
| Horizontal raster | `assets/img/logo-horizontal.png` | 1200×240 | `#141414` | Fallback |
| Isotipo (monograma "B&A") | `assets/img/logo-isotipo.svg` | 512×512 | `#FFFFFF` | Footers oscuros, redes sociales |
| Isotipo raster | `assets/img/logo-isotipo.png` | 512×512 | `#FFFFFF` | Fallback |
| Favicon SVG | `assets/favicon.svg` | viewBox 384×384 | Isotipo blanco sobre verde laurel | Pestaña del navegador |
| Favicon PNG | `assets/favicon-{16,32,512}.png` | varios | idem | Pestañas (PNG fallback) |
| Apple touch icon | `assets/apple-touch-icon.png` | 180×180 | idem | iOS home screen |

**Wordmark alternativo en texto** (lo que usa el sitio hoy):
- Familia: GT Sectra Display, weight 300, letter-spacing 0.34em, uppercase
- "&" en GT Sectra Display itálico (más caligráfico)

---

## 🎨 Paleta de color

### Primarios — Verde laurel mediterráneo
| Token | HEX | Rol |
|---|---|---|
| `--laurel` | **#3D5A3E** | Color primario · botones, links, branding |
| `--laurel-deep` | #1F2E20 | Profundidad · footer, fondos oscuros |
| `--laurel-soft` | #4A6A4B | Estado hover |

### Neutros — Papel y tinta
| Token | HEX | Rol |
|---|---|---|
| `--bone` (paper) | **#F5F1E8** | Fondo principal del sitio (hueso/papel) |
| `--bone-2` (paper-2) | #ECE6D8 | Fondo alternativo · secciones |
| `--white` | #FFFFFF | Cards, fondos limpios |
| `--ink` | **#1A1A1A** | Tipografía principal |
| `--ink-2` | #2B2B2B | Tipografía secundaria |
| `--stone` (ink-mute) | #8B8478 | Tipografía suave · captions, meta |
| `--black` | #0E0E0E | Máximo contraste donde haga falta |

### Acento
| Token | HEX | Rol |
|---|---|---|
| `--brass` | **#B8945A** | Acentos (latón envejecido) · usar con cuidado |

### Líneas
| Token | HEX | Rol |
|---|---|---|
| `--line` | #E5DED0 | Bordes, separadores |
| `--line-soft` | #EFE9DA | Bordes más sutiles |

---

## 🔤 Tipografía

### Familias
| Variable | Familia | Carga | Usos |
|---|---|---|---|
| `--serif` | **GT Sectra Display** (fallback: Cormorant Garamond, Times New Roman) | Local + Google fallback | Títulos, h1-h3, blockquotes, marca |
| `--sans` | **Inter** (fallback: Sohne, system-ui) | Google Fonts | Cuerpo de texto, UI |
| `--mono` | **IBM Plex Mono** | Google Fonts | Eyebrows, datos pequeños |

### Pesos disponibles
- GT Sectra Display: Regular 400, Light Italic 300 (`assets/fonts/GT-Sectra-Display-*.woff2`)
- Sohne: Bold Italic 700 (local)
- Inter: 300, 400, 500, 600, 700 (Google)
- IBM Plex Mono: 400, 500 (Google)
- Cormorant Garamond: 300, 300 italic (Google, fallback)

### Jerarquía visual típica
- H1 hero: GT Sectra Display, `clamp(42px, 6vw, 72px)`, line-height 1.05
- H2 secciones: GT Sectra Display ~48px
- H3 cards: GT Sectra Display ~28px / 500
- Eyebrows: IBM Plex Mono o Inter 600, uppercase, letter-spacing 0.18em, ~12px
- Cuerpo: Inter 400, 17px, line-height 1.6
- Cita destacada: GT Sectra Display 300 italic

---

## 🎤 Voz y tono editorial

### Cómo escribimos
- **Editorial, sensorial, sin reloj.** Narrativa, no planilla operativa
- **Cursivas para acentos emocionales** (`<em>`)
- **Sin coloquialismos**: nada de "callecitas", "jugando de local", "se arma sola", "en casa" para la villa
- **Frases declarativas, paralelismos**: *"En la naturaleza · En la mesa · En la historia"*, *"Una sola casa, una sola cocina"*
- **Tono small-group A&K-tier**: "grupo reducido", "nunca más de ocho", "intimidad y camaradería", "lejos del circuito de los tours"

### Claims firmados
- **Posicionamiento**: *"Casa de viajes en pequeño grupo y a medida"*
- **Cita del fundador** (Brian Blisniuk): *"No vendemos viajes; ayudamos a la gente a recordar mejor el resto de su vida."*
- **Recurring line del home**: *"Experiencias que se quedan a vivir."*
- **CTA banner**: *"Viajes para recordar mejor."*

### Claims a NO usar hasta verificar
- ❌ "Diecisiete años premiados por Travesía Magazine"
- ❌ "Cuarenta y siete proyectos en veinticinco países"
- ❌ "Más de cuatrocientos guías formados en casa"

---

## 📞 Ficha de empresa

- **Razón social**: Blisniuk & Amanov S.A.
- **Teléfono**: +54 11 6139 5550
- **Dirección**: Manuel Ugarte 2035, Buenos Aires
- **Registro**: RNAV Legajo 20943
- **Email**: `info@blisniukamanov.com`
- **Instagram**: [`@blisniukamanov`](https://www.instagram.com/blisniukamanov)
- **TikTok**: `@blisniukamanov`
- **Idioma del sitio**: Español (`es` / `es_AR`)

---

## 🧱 Tokens UI

- **Border radius**: `--r: 6px`
- **Container max-width**: `--maxw: 1380px`
- **Gutter responsive**: `clamp(20px, 4vw, 60px)`
- **Header height**: 86px desktop / 64px mobile
- **Transiciones**:
  - `--t-fast: 200ms ease`
  - `--t-med: 380ms cubic-bezier(.22,.61,.36,1)`
  - `--t-slow: 700ms cubic-bezier(.22,.61,.36,1)`

---

## 📁 Archivos de marca en el repo

```
assets/
├── favicon.svg                                  ← isotipo blanco sobre verde
├── favicon-16.png · favicon-32.png · favicon-512.png
├── apple-touch-icon.png                         ← 180×180 iOS
├── fonts/
│   ├── GT-Sectra-Display-Regular.{woff2,woff,ttf}
│   ├── GT-Sectra-Display-LightItalic.{woff2,woff,ttf}
│   └── Sohne-BoldItalic.{woff2,woff,ttf}
└── img/
    ├── logo-horizontal.{svg,png}                ← wordmark oscuro
    └── logo-isotipo.{svg,png}                   ← isotipo blanco
```
