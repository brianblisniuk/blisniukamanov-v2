# Prompt para pegar en claude.ai (web)

Copiá todo lo que está entre las dos líneas `=====` y pegalo como un mensaje nuevo a Claude en claude.ai. Adjuntá también el archivo `tools/download-photos.sh` (o pegá el contenido del bloque ` ```bash` al final).

---

=====

Hola Claude. Soy el cliente del proyecto **Pasaporte Negro** (sitio de turismo de lujo). Otro Claude (Claude Code en el sandbox web) curó 37 fotos específicas de Unsplash y armó este script de descarga, pero su sandbox bloquea `images.unsplash.com`. Vos sí tenés acceso. Te pido lo siguiente, en este orden:

### Paso 1 — Correr el script
Guardá el script abajo como `download-photos.sh` y corrélo:

```bash
mkdir -p assets/img && bash download-photos.sh
```

El script tiene un proceso de 4 etapas por foto:
1. Fetch del HTML de `unsplash.com/photos/<slug>`
2. Parsea `og:image` para extraer la URL canónica del CDN
3. Aplica params de tamaño/calidad (`?w=<W>&h=<H>&fit=crop&fm=jpg&q=85`)
4. Valida que el archivo bajado sea JPEG real (`file ... | grep "JPEG image"`)

Los corruptos se mueven a `assets/img/_failed/` (no quiero archivos basura mezclados).

### Paso 2 — Devolveme tres cosas

**(a) El output completo** del script (la sección "RESUMEN" con OK/skip/failed).

**(b) Verificación visual** — abrí cada uno de los 37 archivos en `assets/img/` (no `_failed/`) y comparalos contra la descripción esperada de abajo. Devolveme una tabla:

| Archivo | Descripción esperada | ¿Coincide? | Nota si swap |
|---|---|---|---|
| hero-piamonte-tartufo.jpg | Viñedos de las Langhe en otoño, vista aérea, viñedos rojos | ✅ / ❌ | (sugerir keywords para reemplazo) |
| ... | ... | | |

**(c) Un zip** llamado `sitio-photos.zip` con las 37 fotos para que yo lo descargue y lo agregue al repo.

### Descripciones esperadas por slot

#### Heros de viaje (10)
- `hero-piamonte-tartufo.jpg` — Viñedos de las Langhe en otoño, viñedos rojos, niebla, cascina
- `hero-uzbekistan-ruta-seda.jpg` — Plaza Registán Samarcanda, las tres madrasas con cúpulas azules
- `hero-namibia-dunas.jpg` — Duna roja gigante al amanecer (Sossusvlei), escala humana al pie
- `hero-laponia-auroras.jpg` — Aurora boreal verde-violeta sobre lago helado
- `hero-bahia-otro-carnaval.jpg` — Procesión "Filhos de Gandhy" en blanco con turbantes azules
- `hero-japon-mono-no-aware.jpg` — Camino del Filósofo en plena floración, sakura sobre canal
- `hero-butan-nepal-himalaya.jpg` — Tiger's Nest contra acantilado y cielo himalayo
- `hero-marruecos-imperial.jpg` — Patio de Bahia Palace con zellige y luz cenital
- `hero-croacia-islas-dalmatas.jpg` — Catamarán anclado en cala azul turquesa
- `hero-alaska-salvaje.jpg` — Oso pardo en pradera con macizo de fondo

#### Wildlife / retratos (10) — ratio 3:4 portrait
- `wildlife-piamonte-tartufo.jpg` — Trifolau con lagotto romagnolo en bosque al amanecer
- `wildlife-uzbekistan-ruta-seda.jpg` — Detalle de cúpula tilada azul cobalto
- `wildlife-namibia-dunas.jpg` — Oryx solitario contra duna
- `wildlife-laponia-auroras.jpg` — Reno solo en bosque nevado
- `wildlife-bahia-otro-carnaval.jpg` — Tambor olodum cerca del rostro de percussionista
- `wildlife-japon-mono-no-aware.jpg` — Hojas de arce y musgo con piedra de jardín
- `wildlife-butan-nepal-himalaya.jpg` — Monje en thangka workshop con luz lateral
- `wildlife-marruecos-imperial.jpg` — Manos del maestro tallando zellige
- `wildlife-croacia-islas-dalmatas.jpg` — Ostra Mali Ston abierta con limón y vino
- `wildlife-alaska-salvaje.jpg` — Salmón rojo saltando en cataratas

#### Site heroes (3)
- `hero-savannah.jpg` — Sabana al amanecer con árbol acacia
- `hero-alpine.jpg` — Montaña alpina con nieve y lago
- `hero-coast.jpg` — Costa al atardecer con rocas

#### Day images (14)
- `day-namibia-dunas-2.jpg` — Deadvlei, esqueletos de camelthorn
- `day-namibia-dunas-3.jpg` — Shipwreck Coast o vista aérea de dunas
- `day-laponia-auroras-1.jpg` — Helsinki design district o sauna
- `day-laponia-auroras-2.jpg` — Familia Sami con renos
- `day-laponia-auroras-3.jpg` — Cabaña de cristal interior con aurora afuera
- `day-laponia-auroras-4.jpg` — Equipo de huskies en bosque
- `day-japon-mono-no-aware-1.jpg` — Asakusa Senso-ji con cerezos
- `day-japon-mono-no-aware-2.jpg` — Ceremonia del té (o camino del filósofo)
- `day-japon-mono-no-aware-3.jpg` — Onsen Hakone con vista a Fuji (o templo japonés)
- `day-japon-mono-no-aware-4.jpg` — Teshima Art Museum (o cerezos)
- `day-butan-nepal-himalaya-3.jpg` — Danza cham con máscara butanesa
- `day-butan-nepal-himalaya-4.jpg` — Thongdrel desenrollándose o paisaje himalayo
- `day-croacia-islas-dalmatas-1.jpg` — Palacio Diocleciano peristyle
- `day-croacia-islas-dalmatas-4.jpg` — Murallas Dubrovnik vista desde el mar

### Si algo falla

Si `og:image` no aparece en el HTML de un slug, o el redirect del CDN devuelve 503/404, marcalo en la tabla y proponé 1-2 slugs alternativos con búsqueda en `unsplash.com/s/photos/<keywords>`. NO uses `source.unsplash.com` — está deprecado desde junio 2024.

### Script

```bash
{ cat tools/download-photos.sh aquí }
```

=====

---

## Cómo usar este prompt

1. Abrí `tools/download-photos.sh` en este repo, copialo entero
2. En claude.ai (web), pegá el prompt de arriba reemplazando `{ cat tools/download-photos.sh aquí }` con el script real
3. Mandalo
4. Cuando el otro Claude te devuelva el zip, descargá y descomprimí en `assets/img/`
5. `git add assets/img/ && git commit -m "Real photos (Phase 1)" && git push`
6. Yo (Claude Code) re-renderizo screenshots y verifico

## Phase 2

Después de Phase 1, quedan ~85 slots con placeholder:
- 26 day images (4 por viaje × 10 viajes, menos los 14 que ya curé)
- 40 lodge images (4 por viaje × 10 viajes)
- 15 dest-*.jpg (regiones)
- 7 way-*.jpg (formas de explorar)
- 2 stay-*.jpg
- 5 misc (intro-quote, why-banner, etc.)
- 3 brochure-*.jpg
- 1 route-map.jpg

Para Phase 2, te paso un segundo payload con los slugs curados de esos slots después de validar Phase 1.
