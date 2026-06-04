# Videos del spotlight hero

El home (`index.html`) tiene 3 slides en la sección spotlight, cada uno con
su propio video de fondo. Mientras los videos no existen, se muestra el
`poster` (la foto JPG) — el sitio funciona igual, solo que estático.

## Archivos esperados

| Archivo                | Slide | Poster fallback                       |
| ---------------------- | ----- | ------------------------------------- |
| `hero-1.mp4`           | 1     | `assets/img/hero-savannah.jpg`        |
| `hero-2.mp4`           | 2     | `assets/img/hero-piamonte-tartufo.jpg`|
| `hero-3.mp4`           | 3     | `assets/img/stay-sanctuari.jpg`       |

## Recomendaciones técnicas

- Formato: **MP4** (codec H.264, perfil baseline o main)
- Duración: **5-7 segundos** (loopean automáticamente)
- Dimensiones: **1920x1080** mínimo (el spotlight es 78vh, las fotos
  actuales son ~1920x1280)
- Peso: **3-5 MB** por video (más arriba degrada el LCP)
- **Sin audio**: el `<video>` está `muted` para que autoplay funcione
- Compresión sugerida con ffmpeg:

```bash
ffmpeg -i input.mov -an -c:v libx264 -preset slow -crf 28 \
       -movflags +faststart -vf "scale=1920:-2,fps=30" hero-1.mp4
```

## Exportar desde Canva

1. Abrí el diseño en Canva
2. **Share → Download**
3. Tipo: **MP4 Video**
4. Calidad: **1080p**
5. Renombrá al nombre esperado (`hero-1.mp4`, `hero-2.mp4` o `hero-3.mp4`)
6. Colocá en esta carpeta y commit + push

El cambio de slide se gatilla cada 7 segundos; el video se rebobina al
arrancar cada slide.
