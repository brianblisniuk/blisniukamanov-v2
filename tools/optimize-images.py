#!/usr/bin/env python3
"""
tools/optimize-images.py — Pipeline de imágenes de Pasaporte Negro.

Toda foto que se suba a assets/img/ pasa por acá: se convierte a WebP
optimizado y se generan versiones responsivas (480 / 960 / 1440 px de
ancho), para que cada dispositivo descargue el tamaño justo y el sitio
cargue rápido. Es el MISMO tratamiento que se aplicó a las 143 imágenes
iniciales — este script lo deja como precedente para todas las que vengan.

USO
  python3 tools/optimize-images.py                 # genera .webp + tiers (idempotente)
  python3 tools/optimize-images.py --apply-srcset  # ademas agrega srcset/sizes a los <img> de *.html

CONVENCIÓN
  - Nombrá los heroes de pagina 'hero-*.jpg' -> usan sizes="100vw".
  - El resto usa un sizes responsivo (full-width en mobile, ~mitad en desktop).
  - Re-ejecutalo cuando agregues fotos: solo procesa lo que falta y solo
    agrega srcset a los <img> que todavia no lo tienen (no pisa nada).
"""
import os, sys, glob, json, re
from PIL import Image, ImageOps

IMG_DIR = "assets/img"
TIERS = [480, 960, 1440]
QUALITY = 80
MANIFEST = os.path.join(IMG_DIR, "_srcset.json")
SKIP = re.compile(r'^(favicon|apple-touch)')


def process_images():
    """Convierte fuentes raster a WebP + genera tiers. Devuelve el manifiesto."""
    manifest = {}
    sources = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        sources += glob.glob(os.path.join(IMG_DIR, ext))
    for src in sorted(sources):
        base = os.path.splitext(os.path.basename(src))[0]
        if SKIP.match(base):
            continue
        webp_full = os.path.join(IMG_DIR, base + ".webp")
        try:
            im = Image.open(src)
            im = ImageOps.exif_transpose(im)
            if im.mode in ("RGBA", "P", "LA"):
                im = im.convert("RGB")
        except Exception as e:
            print("  skip (no abre):", src, e)
            continue
        w, h = im.size
        if not os.path.exists(webp_full):
            im.save(webp_full, "WEBP", quality=QUALITY, method=4)
        made = []
        for t in TIERS:
            if t < w:
                tf = os.path.join(IMG_DIR, "%s-%d.webp" % (base, t))
                if not os.path.exists(tf):
                    r = im.resize((t, round(h * t / w)), Image.LANCZOS)
                    r.save(tf, "WEBP", quality=QUALITY, method=4)
                made.append(t)
        manifest[base] = {"w": w, "tiers": made}
    json.dump(manifest, open(MANIFEST, "w"), ensure_ascii=False, indent=0)
    print("procesadas %d imagenes -> %s" % (len(manifest), MANIFEST))
    return manifest


def srcset_for(base, info):
    parts = ["%s/%s-%d.webp %dw" % (IMG_DIR, base, t, t) for t in info["tiers"]]
    parts.append("%s/%s.webp %dw" % (IMG_DIR, base, info["w"]))
    return ", ".join(parts)


def sizes_for(base):
    return "100vw" if base.startswith("hero-") else "(max-width: 768px) 100vw, 50vw"


def apply_srcset(manifest):
    """Agrega srcset/sizes (+fetchpriority en heroes, +decoding) a los <img> que falten."""
    pages = glob.glob("*.html") + glob.glob("blog/*.html")
    TAG = re.compile(r'<img\b[^>]*\bsrc=["\']' + re.escape(IMG_DIR) + r'/([^"\']+)\.webp["\'][^>]*?/?>')
    total = 0

    def repl(mm):
        tag, base = mm.group(0), mm.group(1)
        if "srcset" in tag:
            return tag
        info = manifest.get(base)
        if not info or not info["tiers"]:
            return tag
        inj = ' srcset="%s" sizes="%s"' % (srcset_for(base, info), sizes_for(base))
        if base.startswith("hero-") and "loading=" not in tag:
            inj += ' fetchpriority="high"'
        if "decoding=" not in tag:
            inj += ' decoding="async"'
        return "<img" + inj + tag[4:]

    for f in pages:
        s = open(f).read()
        s2, n = TAG.subn(repl, s)
        if n and s2 != s:
            open(f, "w").write(s2)
            total += sum(1 for _ in TAG.finditer(s2))
    # contar cuantos quedaron con srcset
    done = 0
    for f in pages:
        done += open(f).read().count("srcset=")
    print("paginas con srcset aplicado; <img> con srcset ahora:", done)


if __name__ == "__main__":
    m = process_images()
    if "--apply-srcset" in sys.argv:
        apply_srcset(m)
