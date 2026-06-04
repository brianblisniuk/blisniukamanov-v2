# Imágenes Blisniuk & Amanov — 136 archivos para `assets/img/`

**Status**: ✅ Las **136 imágenes** del calendario 2026-2027 + generales están en `assets/img/`.

## Cómo usar

1. Descomprimir este zip.
2. Copiar todo `assets/img/*.jpg` al `assets/img/` del repo del sitio.
3. Listo. El sitio funciona — cada archivo tiene exactamente el nombre del inventario.

## Lo que conseguí

| Concepto | Resultado |
|---|---|
| Slots procesados | 136 / 136 |
| Tamaño total | 35 MB |
| Peso promedio | 256 KB |
| Mayores a 400 KB | 1 (sigue funcional) |
| Licencia | CC-BY, CC-BY-SA, CC0, Public Domain — comerciales ✓ |
| Fuente | Openverse → Flickr (CDN `live.staticflickr.com`) |
| Recorte | center-crop al ratio exacto del slot |

## Cómo funcionó

Cuando empezaste me pediste imágenes de `images.unsplash.com`, `images.pexels.com` y
`upload.wikimedia.org`. En mi sandbox:

- `images.unsplash.com` ✅ accesible pero la **búsqueda** está protegida con Anubis
- `images.pexels.com` ✅ accesible pero la **búsqueda** está bloqueada
- `upload.wikimedia.org` ❌ totalmente bloqueado

El descubrimiento clave fue **Openverse** (`api.openverse.org`), un buscador
oficial de Creative Commons que indexa Wikimedia, Flickr, Smithsonian, Met, etc.
Su API responde sin auth y devuelve URLs directas a Flickr (`live.staticflickr.com`,
que sí tengo accesible). Filtré por licencias CC-BY, CC-BY-SA, CC0 y Public
Domain Mark para garantizar uso comercial.

Pipeline para cada slot:

1. **Buscar** en Openverse con un query corto + filtro `source=flickr&license=cc0,pdm,by,by-sa`
2. **Descargar** desde `live.staticflickr.com` probando tamaños `_k` (2048) → `_h` (1600) → `_b` (1024)
3. **Recortar** con `ImageOps.fit` al ratio exacto del slot (16:9, 3:4, 4:3, 4:5)
4. **Optimizar** JPG progresivo iterando quality 88 → 68 hasta caer en ≤ 400 KB
5. **Registrar** atribución (autor, licencia, URL fuente) en `attributions.txt`

## Atribución — IMPORTANTE

Las imágenes con **CC-BY** y **CC-BY-SA** **requieren crédito visible**. El archivo
`attributions.txt` tiene autor, licencia y URL para las 136 imágenes.

Sugerencia: pegalas en una página `/creditos` del sitio o en el footer. Ejemplo:

> Banco de imágenes proveniente de Openverse / Flickr. Atribuciones completas en /creditos.
> Las imágenes con licencia CC BY-SA mantienen esa licencia.

Las **CC0** y **Public Domain Mark** no requieren crédito, pero podés acreditarlas igual.

## Calidad y reemplazo

Estas son **placeholders mejoradísimos** sobre los procedurales — son fotos reales
del lugar / tema correcto. Pero como dice tu inventario:

> Para mantener consistencia: luz dorada baja, mínimo postprocesado, alta
> resolución y poco texto / overlays. Pensá fotorreportaje, no marketing.

Cuando tengas fotos profesionales del viaje, reemplazá los archivos manteniendo
el mismo nombre y se cambian en todas las pantallas sin tocar nada más.

## Slots que merecen revisión manual

Algunos slots quedaron con una imagen "del lugar" pero no exactamente del sujeto
pedido. Si te molestan, mandame el nombre del archivo y te busco mejor candidato:

- `hero-namibia-dunas.jpg` — vista satelital del desierto, no duna a nivel humano
- `hero-japon-mono-no-aware.jpg` — Kyoto pero con momiji rojo en lugar de sakura
- `hero-butan-nepal-himalaya.jpg` — banderas de oración, no Tiger's Nest
- Imágenes específicas de lodges (Orient Star Khiva, UXUA Casa, etc.) tienen una
  foto del lugar genérico equivalente, no la marca específica

Para esos casos, podés:
1. Mandarme el archivo y un query mejor → te lo regenero
2. O reemplazar con foto profesional cuando la tengas

## Si querés re-correr el pipeline

Está todo en `scripts/`:

- `fetch_openverse.py` — el pipeline (Python con Pillow + requests)
- `assets_manifest.csv` — los 136 slots con sus queries
- `attributions.txt` — atribuciones generadas

```bash
pip install Pillow requests
python3 scripts/fetch_openverse.py             # los 136
python3 scripts/fetch_openverse.py uzbekistan  # un viaje específico
```

El script asume estructura `assets/img/` y `scripts/` desde la raíz del repo.
