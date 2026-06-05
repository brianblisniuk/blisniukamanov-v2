# Imágenes del sitio — pipeline (precedente)

Toda foto que se suba a `assets/img/` pasa por el mismo tratamiento que se
aplicó a las 143 iniciales: se convierte a **WebP** optimizado y se generan
versiones **responsivas** (480 / 960 / 1440 px de ancho), para que cada
dispositivo descargue el tamaño justo. En la práctica: un celular baja ~64 KB
en vez de ~270 KB por imagen.

## Procesar fotos nuevas

1. Poné las fotos (`.jpg`, `.jpeg`, `.png`) en `assets/img/`.
   - Si es el hero de una página, nombralo `hero-*.jpg`: se sirve a `100vw`
     y carga con prioridad (`fetchpriority="high"`).
2. Corré:

   ```
   python3 tools/optimize-images.py --apply-srcset
   ```

   - Genera el `.webp` + los tamaños responsivos de lo que falte
     (es idempotente: no reprocesa lo ya hecho).
   - Agrega `srcset` / `sizes` a los `<img>` que todavía no lo tengan
     (no pisa los que ya están).
3. Commiteá los `.webp` nuevos y el HTML modificado.

## Notas

- `og:image` / `twitter:image` se dejan en `.jpg` a propósito: los previews de
  WhatsApp y redes los renderizan mejor que WebP. Por eso se conservan los JPG.
- Los tiers se nombran `nombre-480.webp`, `nombre-960.webp`, `nombre-1440.webp`.
- El manifiesto `assets/img/_srcset.json` lo mantiene el script; no se edita a mano.
