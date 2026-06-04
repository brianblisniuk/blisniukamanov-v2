#!/usr/bin/env bash
# ============================================================================
# Blisniuk & Amanov — descarga 37 fotos curadas de Unsplash
# ============================================================================
# Cómo funciona:
# 1. Para cada slug, fetch del HTML de unsplash.com/photos/<slug>
# 2. Extrae la URL canónica del CDN del meta tag og:image
# 3. Reemplaza los query params por los nuestros (w, h, fit, q, fm)
# 4. Descarga la imagen optimizada (CDN-side resize → 300-500 KB target)
# 5. Valida que sea JPEG real; los corruptos van a assets/img/_failed/
#
# Salida típica esperada: 37 archivos JPG en assets/img/, < 500 KB c/u
# ============================================================================
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/img assets/img/_failed

OK=0
FAIL=0
SKIP=0
FAILED_LIST=()

# fetch_unsplash <output_filename> <slug> <width> <height>
# Para hero: 2400x1300 (ratio 16:9 cropped)
# Para wildlife: 900x1200 (ratio 3:4 portrait)
# Para day: 1200x900 (ratio 4:3 landscape)
fetch_unsplash() {
  local out="$1" slug="$2" w="${3:-2400}" h="${4:-1300}"
  local target="assets/img/$out"
  local page_url="https://unsplash.com/photos/${slug}"

  # Skip if already a valid sized JPEG
  if [[ -f "$target" ]] && [[ $(wc -c < "$target") -gt 30000 ]] && file "$target" 2>/dev/null | grep -q "JPEG image"; then
    echo "  ⊖ ${out}  (skip — already a valid JPEG)"
    SKIP=$((SKIP+1))
    return 0
  fi

  echo -n "  → ${out} (slug ${slug}, ${w}x${h}) ... "

  # Stage 1: fetch the photo page HTML
  local html
  html=$(curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
              --connect-timeout 10 --max-time 30 \
              "$page_url" 2>/dev/null) || { echo "✗ page fetch failed"; FAIL=$((FAIL+1)); FAILED_LIST+=("$out:page-fetch"); return 1; }

  # Stage 2: extract og:image canonical URL from the HTML
  # Unsplash's og:image is typically https://images.unsplash.com/photo-XXX?w=1200&...
  local og_url
  og_url=$(echo "$html" | grep -oE 'property="og:image"[^>]+content="[^"]+"' | head -1 \
                       | sed -E 's/.*content="([^"]+)".*/\1/')

  if [[ -z "$og_url" ]]; then
    # Fallback: try meta property in other order
    og_url=$(echo "$html" | grep -oE 'content="[^"]*images\.unsplash\.com[^"]*"' | head -1 \
                         | sed -E 's/.*content="([^"]+)".*/\1/')
  fi

  if [[ -z "$og_url" ]]; then
    echo "✗ no og:image found"
    FAIL=$((FAIL+1)); FAILED_LIST+=("$out:no-og-image")
    return 1
  fi

  # Stage 3: strip existing query params and apply ours
  local base="${og_url%%\?*}"
  local img_url="${base}?w=${w}&h=${h}&fit=crop&fm=jpg&q=85"

  # Stage 4: download the optimized image
  if curl -sSL -A "Mozilla/5.0" --connect-timeout 10 --max-time 60 \
          -o "$target" "$img_url"; then
    if file "$target" 2>/dev/null | grep -q "JPEG image"; then
      local size_kb; size_kb=$(($(wc -c < "$target")/1024))
      echo "✓ (${size_kb} KB)"
      OK=$((OK+1))
      return 0
    fi
    local body; body=$(head -c 80 "$target" | tr -d '\0\r\n' | head -c 50)
    echo "✗ not JPEG (got: ${body}...)"
    mv "$target" "assets/img/_failed/$out" 2>/dev/null
  else
    echo "✗ image download failed"
  fi
  FAIL=$((FAIL+1)); FAILED_LIST+=("$out:download-or-not-jpeg")
  return 1
}

echo "============================================================"
echo " 1) HERO IMAGES — 10 viajes (2400x1300, ratio 16:9)"
echo "============================================================"
fetch_unsplash hero-piamonte-tartufo.jpg       "Yc2OnbuO2Ck" 2400 1300
fetch_unsplash hero-uzbekistan-ruta-seda.jpg   "hvLu3ABC1n0" 2400 1300
fetch_unsplash hero-namibia-dunas.jpg          "vEAFs5C4Lkk" 2400 1300
fetch_unsplash hero-laponia-auroras.jpg        "ZPbfvIN4NXs" 2400 1300
fetch_unsplash hero-bahia-otro-carnaval.jpg    "BGD47PMGzyM" 2400 1300
fetch_unsplash hero-japon-mono-no-aware.jpg    "8sOZJ8JF0S8" 2400 1300
fetch_unsplash hero-butan-nepal-himalaya.jpg   "e6x39Tqj0g4" 2400 1300
fetch_unsplash hero-marruecos-imperial.jpg     "ZrX8Fx2myj8" 2400 1300
fetch_unsplash hero-croacia-islas-dalmatas.jpg "5maoPl591Sk" 2400 1300
fetch_unsplash hero-alaska-salvaje.jpg         "Ex1vVC0Zxwg" 2400 1300

echo
echo "============================================================"
echo " 2) WILDLIFE / PORTRAITS — 10 viajes (900x1200, ratio 3:4 portrait)"
echo "============================================================"
fetch_unsplash wildlife-piamonte-tartufo.jpg       "rbDKzRSzx9o" 900 1200
fetch_unsplash wildlife-uzbekistan-ruta-seda.jpg   "QaxdKj5E2kM" 900 1200
fetch_unsplash wildlife-namibia-dunas.jpg          "1CpVwBuMnvc" 900 1200
fetch_unsplash wildlife-laponia-auroras.jpg        "YtU0qFOJ654" 900 1200
fetch_unsplash wildlife-bahia-otro-carnaval.jpg    "qHgLw6-qmsQ" 900 1200
fetch_unsplash wildlife-japon-mono-no-aware.jpg    "kBG0r2tEaEY" 900 1200
fetch_unsplash wildlife-butan-nepal-himalaya.jpg   "s5jSBfDXuZI" 900 1200
fetch_unsplash wildlife-marruecos-imperial.jpg     "YeEiQYSd3ms" 900 1200
fetch_unsplash wildlife-croacia-islas-dalmatas.jpg "sXhTeALCxbQ" 900 1200
fetch_unsplash wildlife-alaska-salvaje.jpg         "uMnIZ8CTVOg" 900 1200

echo
echo "============================================================"
echo " 3) SITE HEROES — 3 (2400x1300, ratio 16:9)"
echo "============================================================"
fetch_unsplash hero-savannah.jpg "Q4QXdCCbVzI" 2400 1300
fetch_unsplash hero-alpine.jpg   "7Z94A-v9kvw" 2400 1300
fetch_unsplash hero-coast.jpg    "eUeK1pD7fH0" 2400 1300

echo
echo "============================================================"
echo " 4) DAY IMAGES — 14 con slug específico (1200x900, ratio 4:3)"
echo "    Phase 2 buscará los ~26 restantes."
echo "============================================================"
# Namibia
fetch_unsplash day-namibia-dunas-2.jpg          "UbIvR3B4NJ8" 1200 900  # Deadvlei
fetch_unsplash day-namibia-dunas-3.jpg          "sFrBry-NkKw" 1200 900  # aerial dunes
# Laponia
fetch_unsplash day-laponia-auroras-1.jpg        "GFlDG_HPlBo" 1200 900  # Helsinki glass
fetch_unsplash day-laponia-auroras-2.jpg        "KBKHXjhVQVM" 1200 900  # reindeer sled
fetch_unsplash day-laponia-auroras-3.jpg        "DvWgkPcsd7E" 1200 900  # aurora trees
fetch_unsplash day-laponia-auroras-4.jpg        "pM2Hpsi-Hxs" 1200 900  # animal snow
# Japón
fetch_unsplash day-japon-mono-no-aware-1.jpg    "_M3BbcfZajA" 1200 900  # cherry walkway
fetch_unsplash day-japon-mono-no-aware-2.jpg    "tl0uMsO7xIs" 1200 900  # cherry garden path
fetch_unsplash day-japon-mono-no-aware-3.jpg    "4Q-Rbu8Ipcg" 1200 900  # temple cherry sunset
fetch_unsplash day-japon-mono-no-aware-4.jpg    "A29L9_iebmQ" 1200 900  # weeping cherry
# Bután
fetch_unsplash day-butan-nepal-himalaya-3.jpg   "Q0IkDV2i4S4" 1200 900  # cliff w/ building
fetch_unsplash day-butan-nepal-himalaya-4.jpg   "14nx0UYX3vE" 1200 900  # mountain village
# Croacia
fetch_unsplash day-croacia-islas-dalmatas-1.jpg "RFI7w4MyzW4" 1200 900  # Dubrovnik aerial
fetch_unsplash day-croacia-islas-dalmatas-4.jpg "C2-XJaEpeKY" 1200 900  # Dubrovnik walls

echo
echo "============================================================"
echo " RESUMEN"
echo "============================================================"
printf "  ✓ OK:      %d\n" "$OK"
printf "  ⊖ skip:    %d\n" "$SKIP"
printf "  ✗ failed:  %d\n" "$FAIL"

if [[ $FAIL -gt 0 ]]; then
  echo
  echo "FAILED detail:"
  for f in "${FAILED_LIST[@]}"; do echo "  - $f"; done
fi

echo
echo "Total real JPEGs en assets/img/: $(find assets/img -maxdepth 1 -name '*.jpg' -size +30k | wc -l)"
echo "Tamaño promedio: $(du -sk assets/img/*.jpg 2>/dev/null | awk '{sum+=$1; n++} END {if(n) printf "%d KB", sum/n}')"
