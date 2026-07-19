# Pasaporte Negro — sitio web

Sitio estático de Pasaporte Negro («Turismo de lujo»). Once expediciones por año en grupos de hasta diez viajeros, con dos accesos de la casa en cada una.

- **Páginas de expedición**: generadas desde Supabase (`trips.public_content` + `data.meta`) vía `pn_export_v2()`. La fuente de verdad es la base; las páginas se regeneran, no se editan a mano.
- **Marca**: paleta monocroma (Abismo `#0A0A0B`, Carbón `#101012`, Marfil `#E8E6E0`, Humo `#8A8F97`, Grafito `#3A3B3F`), tipografías Marcellus · Cormorant Garamond · Jost. Overrides en `pn.css`.
- **Formularios**: newsletter → edge function `public-subscribe`; consultas → `public-lead` (CRM). Netlify Forms queda como fallback.
- **Imágenes**: material de terceros con licencia (ver `attributions.txt`) hasta contar con material propio por destino.
