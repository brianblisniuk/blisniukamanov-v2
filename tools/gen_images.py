"""Procedurally generate landscape-like placeholder images for the website."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter

OUT = "/home/user/sitio/assets/img"
os.makedirs(OUT, exist_ok=True)

# Each entry: (filename, [(top RGB), (mid RGB), (bottom RGB)], horizon_y_ratio, accent_band, style)
# style: 'mountain' | 'flat' | 'water' | 'sky' | 'forest' | 'desert' | 'snow' | 'city'
PALETTE = [
    # Hero / spotlight
    ("hero-savannah.jpg",      [(76,52,30), (180,128,72), (245,200,140)], 0.62, "warm",   "savannah"),
    ("hero-alpine.jpg",        [(40,55,80), (90,120,150), (200,210,220)], 0.55, "cool",   "mountain"),
    ("hero-coast.jpg",         [(60,90,130), (110,160,180), (230,210,180)], 0.50, "cool",  "water"),

    # Destinations / regions
    ("dest-japan.jpg",         [(80,50,80), (170,90,110), (240,200,200)], 0.55, "warm",   "mountain"),
    ("dest-patagonia.jpg",     [(50,75,100), (110,140,160), (220,225,230)], 0.50, "cool",  "mountain"),
    ("dest-morocco.jpg",       [(110,55,30), (200,130,70), (245,210,160)], 0.55, "warm",   "desert"),
    ("dest-kenya.jpg",         [(180,110,60), (210,160,90), (240,210,150)], 0.55, "warm",  "savannah"),
    ("dest-india.jpg",         [(140,60,50), (210,140,100), (240,200,170)], 0.55, "warm",  "city"),
    ("dest-italy.jpg",         [(60,80,120), (180,180,160), (235,215,180)], 0.50, "warm",  "city"),
    ("dest-spain.jpg",         [(120,80,40), (200,150,90), (240,210,170)], 0.55, "warm",   "city"),
    ("dest-asia.jpg",          [(50,90,80), (120,160,130), (215,220,200)], 0.55, "cool",   "forest"),
    ("dest-southamerica.jpg",  [(90,60,100), (180,110,90), (240,200,170)], 0.55, "warm",   "mountain"),
    ("dest-centralamerica.jpg",[(70,90,60), (150,170,100), (230,220,180)], 0.55, "warm",   "forest"),
    ("dest-northamerica.jpg",  [(120,70,50), (210,150,100), (240,210,170)], 0.55, "warm",   "desert"),
    ("dest-caribbean.jpg",     [(60,140,170), (150,210,210), (240,235,210)], 0.45, "cool",  "water"),
    ("dest-oceania.jpg",       [(20,90,130), (60,160,170), (230,225,200)], 0.45, "cool",   "water"),
    ("dest-europe.jpg",        [(70,90,120), (180,180,160), (240,230,210)], 0.50, "cool",  "mountain"),
    ("dest-arctic.jpg",        [(80,100,130), (160,180,200), (235,240,245)], 0.55, "cool", "snow"),
    ("dest-mena.jpg",          [(140,70,40), (220,150,80), (245,215,170)], 0.55, "warm",   "desert"),
    ("dest-indianocean.jpg",   [(40,110,160), (130,200,210), (240,230,200)], 0.50, "cool", "water"),

    # Trip kinds / ways
    ("way-private.jpg",        [(60,40,30), (140,90,60), (210,170,130)], 0.55, "warm",    "savannah"),
    ("way-group.jpg",          [(70,90,60), (150,170,110), (220,210,180)], 0.55, "warm",   "forest"),
    ("way-safari.jpg",         [(160,90,40), (220,150,80), (240,200,150)], 0.55, "warm",   "savannah"),
    ("way-cruise.jpg",         [(40,80,120), (110,170,200), (240,220,200)], 0.50, "cool",  "water"),
    ("way-jet.jpg",            [(50,70,110), (130,160,200), (220,225,235)], 0.45, "cool",  "sky"),
    ("way-family.jpg",         [(110,80,50), (210,160,110), (240,215,180)], 0.55, "warm",  "savannah"),
    ("way-honey.jpg",          [(180,90,80), (220,150,140), (240,210,200)], 0.50, "warm",  "water"),

    # Stay with us
    ("stay-sanctuari.jpg",     [(100,50,40), (190,120,80), (235,200,160)], 0.55, "warm",   "desert"),
    ("stay-villa.jpg",         [(50,80,120), (120,170,170), (230,220,200)], 0.50, "cool",  "water"),

    # Misc
    ("intro-quote.jpg",        [(40,50,70), (100,120,140), (210,200,180)], 0.55, "warm",   "mountain"),
    ("philanthropy.jpg",       [(150,90,40), (210,150,90), (240,200,150)], 0.55, "warm",   "savannah"),
    ("why-banner.jpg",         [(100,60,40), (190,130,80), (240,200,150)], 0.55, "warm",   "desert"),
    ("award-thumb.jpg",        [(80,50,30), (160,100,50), (220,170,110)], 0.50, "warm",   "savannah"),
    ("next-up.jpg",            [(60,80,60), (140,170,110), (220,220,180)], 0.55, "warm",   "forest"),
    ("magazine-1.jpg",         [(80,60,50), (170,120,90), (220,190,160)], 0.55, "warm",   "mountain"),
    ("magazine-2.jpg",         [(60,90,70), (150,170,120), (220,210,180)], 0.55, "warm",   "forest"),
    ("magazine-3.jpg",         [(150,90,50), (220,160,90), (240,210,170)], 0.55, "warm",   "desert"),

    # Brochure stack
    ("brochure-1.jpg",         [(40,60,90), (120,160,180), (220,215,200)], 0.45, "cool",  "water"),
    ("brochure-2.jpg",         [(110,60,40), (200,130,70), (240,200,150)], 0.55, "warm",   "desert"),
    ("brochure-3.jpg",         [(70,90,60), (150,170,110), (220,210,170)], 0.55, "warm",   "forest"),

    # Journey cards
    ("j-italy.jpg",            [(70,90,120), (180,170,150), (235,220,190)], 0.50, "warm",   "city"),
    ("j-spainport.jpg",        [(120,80,50), (200,150,100), (240,210,170)], 0.55, "warm",   "city"),
    ("j-japan.jpg",            [(90,50,80), (180,100,110), (240,200,200)], 0.55, "warm",   "mountain"),
    ("j-asia.jpg",             [(50,90,70), (130,170,120), (220,220,190)], 0.55, "cool",   "forest"),
    ("j-botswana.jpg",         [(150,90,40), (220,150,80), (240,200,150)], 0.55, "warm",   "savannah"),
    ("j-migration.jpg",        [(170,100,50), (230,160,90), (240,210,160)], 0.55, "warm",  "savannah"),
    ("j-peru.jpg",             [(70,90,110), (160,140,110), (220,200,170)], 0.55, "warm",  "mountain"),
    ("j-alaska.jpg",           [(70,100,130), (160,180,180), (230,235,235)], 0.55, "cool", "snow"),
    ("j-egypt.jpg",            [(140,90,40), (220,170,90), (245,215,160)], 0.55, "warm",   "desert"),

    # Fundación
    ("fund-people.jpg",        [(150,80,60), (220,150,110), (240,210,180)], 0.55, "warm",  "city"),

    # Piamonte (paleta otoñal: viñedos rojos, niebla, dorado bajo)
    ("hero-piamonte-tartufo.jpg",     [(70,55,75), (170,110,80), (235,200,140)], 0.55, "warm", "mountain"),
    ("wildlife-piamonte-tartufo.jpg", [(60,50,40), (140,110,70), (220,190,140)], 0.60, "warm", "forest"),
    ("day-piamonte-tartufo-1.jpg",    [(80,60,50), (190,140,90), (240,210,170)], 0.55, "warm", "city"),
    ("day-piamonte-tartufo-2.jpg",    [(50,45,55), (110,90,90), (190,170,150)], 0.50, "warm", "city"),
    ("day-piamonte-tartufo-3.jpg",    [(70,55,55), (160,120,100), (230,200,170)], 0.55, "warm", "city"),
    ("day-piamonte-tartufo-4.jpg",    [(60,50,40), (140,110,80), (220,190,150)], 0.55, "warm", "forest"),
    ("lodge-piamonte-tartufo-1.jpg",  [(80,65,55), (190,150,110), (235,210,170)], 0.55, "warm", "city"),
    ("lodge-piamonte-tartufo-2.jpg",  [(45,40,45), (100,85,80), (180,160,140)], 0.50, "warm", "city"),
    ("lodge-piamonte-tartufo-3.jpg",  [(70,55,50), (150,115,85), (215,185,150)], 0.55, "warm", "city"),
    ("lodge-piamonte-tartufo-4.jpg",  [(60,75,90), (170,160,140), (235,215,185)], 0.50, "warm", "mountain"),

    # Uzbekistán (cobalto + sand + turquoise dome)
    ("hero-uzbekistan-ruta-seda.jpg",     [(40,60,110), (140,160,200), (235,210,160)], 0.55, "cool", "city"),
    ("wildlife-uzbekistan-ruta-seda.jpg", [(30,70,130), (90,160,200), (220,220,200)], 0.55, "cool", "city"),
    ("day-uzbekistan-ruta-seda-1.jpg",    [(60,75,110), (180,170,140), (235,215,170)], 0.55, "warm", "city"),
    ("day-uzbekistan-ruta-seda-2.jpg",    [(80,60,40), (180,140,90), (240,210,160)], 0.55, "warm", "desert"),
    ("day-uzbekistan-ruta-seda-3.jpg",    [(130,80,50), (210,160,100), (245,215,170)], 0.55, "warm", "desert"),
    ("day-uzbekistan-ruta-seda-4.jpg",    [(40,80,140), (110,170,200), (230,210,170)], 0.55, "cool", "city"),
    ("lodge-uzbekistan-ruta-seda-1.jpg",  [(80,70,60), (190,160,120), (235,210,170)], 0.55, "warm", "city"),
    ("lodge-uzbekistan-ruta-seda-2.jpg",  [(60,55,50), (160,130,100), (220,200,170)], 0.55, "warm", "city"),
    ("lodge-uzbekistan-ruta-seda-3.jpg",  [(50,75,120), (140,170,180), (230,220,200)], 0.55, "cool", "city"),
    ("lodge-uzbekistan-ruta-seda-4.jpg",  [(70,80,100), (180,180,170), (235,225,205)], 0.50, "warm", "city"),

    # Namibia (red dunes + sky + bone)
    ("hero-namibia-dunas.jpg",     [(120,55,30), (210,120,60), (245,200,130)], 0.55, "warm", "desert"),
    ("wildlife-namibia-dunas.jpg", [(100,50,30), (200,130,70), (240,210,150)], 0.55, "warm", "desert"),
    ("day-namibia-dunas-1.jpg",    [(80,70,60), (180,160,130), (230,215,180)], 0.55, "warm", "city"),
    ("day-namibia-dunas-2.jpg",    [(140,60,30), (220,140,80), (245,210,160)], 0.55, "warm", "desert"),
    ("day-namibia-dunas-3.jpg",    [(100,60,50), (200,130,100), (235,210,180)], 0.50, "warm", "desert"),
    ("day-namibia-dunas-4.jpg",    [(110,55,40), (210,140,90), (240,210,170)], 0.55, "warm", "savannah"),
    ("lodge-namibia-dunas-1.jpg",  [(140,70,40), (220,150,90), (245,215,170)], 0.55, "warm", "desert"),
    ("lodge-namibia-dunas-2.jpg",  [(80,60,50), (180,130,90), (235,205,160)], 0.55, "warm", "desert"),
    ("lodge-namibia-dunas-3.jpg",  [(120,80,50), (210,160,100), (240,210,170)], 0.55, "warm", "savannah"),
    ("lodge-namibia-dunas-4.jpg",  [(100,70,50), (200,150,90), (235,210,170)], 0.55, "warm", "savannah"),

    # Laponia (aurora green/violet + snow)
    ("hero-laponia-auroras.jpg",     [(20,30,70), (60,140,130), (180,210,210)], 0.55, "cool", "snow"),
    ("wildlife-laponia-auroras.jpg", [(60,80,100), (140,170,180), (230,235,240)], 0.55, "cool", "snow"),
    ("day-laponia-auroras-1.jpg",    [(60,55,80), (140,130,150), (210,210,220)], 0.55, "cool", "snow"),
    ("day-laponia-auroras-2.jpg",    [(80,90,110), (170,180,190), (235,240,245)], 0.55, "cool", "snow"),
    ("day-laponia-auroras-3.jpg",    [(40,55,90), (110,160,170), (220,230,235)], 0.55, "cool", "snow"),
    ("day-laponia-auroras-4.jpg",    [(50,70,100), (130,170,180), (220,225,230)], 0.55, "cool", "snow"),
    ("lodge-laponia-auroras-1.jpg",  [(70,80,100), (160,170,180), (220,225,230)], 0.55, "cool", "snow"),
    ("lodge-laponia-auroras-2.jpg",  [(60,70,90), (140,160,170), (215,220,225)], 0.55, "cool", "snow"),
    ("lodge-laponia-auroras-3.jpg",  [(50,60,80), (130,150,170), (210,220,225)], 0.55, "cool", "snow"),
    ("lodge-laponia-auroras-4.jpg",  [(70,75,90), (160,165,175), (225,225,230)], 0.55, "cool", "snow"),

    # Bahía (tropical orange + blue + cobalt)
    ("hero-bahia-otro-carnaval.jpg",     [(70,90,120), (200,180,160), (240,225,200)], 0.55, "warm", "city"),
    ("wildlife-bahia-otro-carnaval.jpg", [(80,60,50), (170,120,90), (220,190,160)], 0.55, "warm", "city"),
    ("day-bahia-otro-carnaval-1.jpg",    [(60,80,120), (170,170,180), (230,220,200)], 0.50, "warm", "city"),
    ("day-bahia-otro-carnaval-2.jpg",    [(120,70,40), (210,160,90), (240,210,160)], 0.55, "warm", "city"),
    ("day-bahia-otro-carnaval-3.jpg",    [(80,90,60), (180,180,120), (230,220,190)], 0.55, "warm", "forest"),
    ("day-bahia-otro-carnaval-4.jpg",    [(40,120,150), (130,200,200), (240,230,200)], 0.45, "cool", "water"),
    ("lodge-bahia-otro-carnaval-1.jpg",  [(70,90,120), (180,180,160), (235,220,190)], 0.50, "warm", "city"),
    ("lodge-bahia-otro-carnaval-2.jpg",  [(80,90,70), (180,180,140), (230,220,190)], 0.55, "warm", "forest"),
    ("lodge-bahia-otro-carnaval-3.jpg",  [(40,130,160), (140,210,210), (240,235,210)], 0.45, "cool", "water"),
    ("lodge-bahia-otro-carnaval-4.jpg",  [(70,80,100), (180,170,150), (230,220,190)], 0.50, "warm", "city"),

    # Japón mono no aware (sakura pink + dark wood + moss)
    ("hero-japon-mono-no-aware.jpg",     [(80,50,80), (200,140,160), (240,215,210)], 0.55, "warm", "city"),
    ("wildlife-japon-mono-no-aware.jpg", [(50,80,60), (130,170,120), (220,220,190)], 0.55, "warm", "forest"),
    ("day-japon-mono-no-aware-1.jpg",    [(90,60,90), (210,150,160), (240,220,210)], 0.55, "warm", "city"),
    ("day-japon-mono-no-aware-2.jpg",    [(70,55,60), (170,130,120), (220,200,180)], 0.55, "warm", "city"),
    ("day-japon-mono-no-aware-3.jpg",    [(60,70,100), (160,170,190), (230,225,220)], 0.55, "cool", "mountain"),
    ("day-japon-mono-no-aware-4.jpg",    [(70,90,100), (170,180,180), (225,220,210)], 0.50, "cool", "city"),
    ("lodge-japon-mono-no-aware-1.jpg",  [(60,50,50), (160,120,110), (220,200,180)], 0.55, "warm", "city"),
    ("lodge-japon-mono-no-aware-2.jpg",  [(70,80,70), (170,170,150), (230,220,200)], 0.55, "warm", "forest"),
    ("lodge-japon-mono-no-aware-3.jpg",  [(50,60,60), (150,150,140), (215,210,200)], 0.55, "cool", "forest"),
    ("lodge-japon-mono-no-aware-4.jpg",  [(40,60,90), (130,170,180), (220,220,210)], 0.50, "cool", "water"),

    # Bután + Nepal (saffron + slate + cobalt sky)
    ("hero-butan-nepal-himalaya.jpg",     [(60,70,110), (160,170,200), (235,225,200)], 0.55, "cool", "mountain"),
    ("wildlife-butan-nepal-himalaya.jpg", [(120,70,50), (210,150,100), (240,210,170)], 0.55, "warm", "city"),
    ("day-butan-nepal-himalaya-1.jpg",    [(80,70,60), (190,160,130), (235,215,180)], 0.55, "warm", "city"),
    ("day-butan-nepal-himalaya-2.jpg",    [(60,80,110), (160,180,200), (230,225,210)], 0.55, "cool", "mountain"),
    ("day-butan-nepal-himalaya-3.jpg",    [(120,80,60), (210,160,110), (240,215,180)], 0.55, "warm", "city"),
    ("day-butan-nepal-himalaya-4.jpg",    [(100,60,40), (210,140,80), (240,205,160)], 0.55, "warm", "city"),
    ("lodge-butan-nepal-himalaya-1.jpg",  [(80,60,50), (180,140,110), (230,210,180)], 0.55, "warm", "city"),
    ("lodge-butan-nepal-himalaya-2.jpg",  [(70,80,90), (170,180,180), (225,220,210)], 0.55, "cool", "mountain"),
    ("lodge-butan-nepal-himalaya-3.jpg",  [(60,70,80), (160,170,170), (220,215,205)], 0.55, "cool", "mountain"),
    ("lodge-butan-nepal-himalaya-4.jpg",  [(80,90,100), (180,190,200), (235,230,220)], 0.55, "cool", "mountain"),

    # Marruecos (terracotta + cobalt tile + brass)
    ("hero-marruecos-imperial.jpg",     [(100,55,30), (200,130,70), (245,210,160)], 0.55, "warm", "desert"),
    ("wildlife-marruecos-imperial.jpg", [(80,60,40), (180,140,90), (230,200,160)], 0.55, "warm", "city"),
    ("day-marruecos-imperial-1.jpg",    [(70,90,130), (180,200,210), (240,230,215)], 0.50, "cool", "city"),
    ("day-marruecos-imperial-2.jpg",    [(110,55,30), (210,130,70), (245,210,160)], 0.55, "warm", "city"),
    ("day-marruecos-imperial-3.jpg",    [(80,70,60), (190,170,140), (235,215,180)], 0.55, "warm", "mountain"),
    ("day-marruecos-imperial-4.jpg",    [(120,70,40), (220,150,90), (245,215,170)], 0.55, "warm", "city"),
    ("lodge-marruecos-imperial-1.jpg",  [(100,60,40), (200,140,90), (235,205,160)], 0.55, "warm", "city"),
    ("lodge-marruecos-imperial-2.jpg",  [(80,70,60), (180,160,130), (230,210,180)], 0.55, "warm", "mountain"),
    ("lodge-marruecos-imperial-3.jpg",  [(110,60,40), (210,140,90), (240,205,160)], 0.55, "warm", "city"),
    ("lodge-marruecos-imperial-4.jpg",  [(90,80,70), (190,170,150), (235,215,185)], 0.55, "warm", "city"),

    # Croacia (aqua sea + white stone + terracotta roof)
    ("hero-croacia-islas-dalmatas.jpg",     [(40,110,160), (140,200,210), (240,230,200)], 0.45, "cool", "water"),
    ("wildlife-croacia-islas-dalmatas.jpg", [(70,90,110), (180,170,150), (235,220,190)], 0.50, "warm", "water"),
    ("day-croacia-islas-dalmatas-1.jpg",    [(80,70,60), (180,160,130), (230,215,180)], 0.55, "warm", "city"),
    ("day-croacia-islas-dalmatas-2.jpg",    [(50,120,160), (140,200,200), (240,230,200)], 0.45, "cool", "water"),
    ("day-croacia-islas-dalmatas-3.jpg",    [(30,70,140), (90,160,210), (230,225,210)], 0.50, "cool", "water"),
    ("day-croacia-islas-dalmatas-4.jpg",    [(110,70,50), (210,150,100), (240,210,170)], 0.55, "warm", "city"),
    ("lodge-croacia-islas-dalmatas-1.jpg",  [(50,100,140), (140,190,200), (235,225,200)], 0.45, "cool", "water"),
    ("lodge-croacia-islas-dalmatas-2.jpg",  [(60,90,120), (170,180,190), (230,225,215)], 0.50, "cool", "water"),
    ("lodge-croacia-islas-dalmatas-3.jpg",  [(80,70,60), (180,160,140), (230,215,185)], 0.55, "warm", "city"),
    ("lodge-croacia-islas-dalmatas-4.jpg",  [(50,110,150), (150,200,210), (240,230,200)], 0.45, "cool", "water"),

    # Alaska Salvaje (deep teal + ice + dark green)
    ("hero-alaska-salvaje.jpg",     [(60,90,100), (140,180,170), (230,235,235)], 0.55, "cool", "snow"),
    ("wildlife-alaska-salvaje.jpg", [(80,60,40), (170,140,80), (220,200,160)], 0.55, "warm", "forest"),
    ("day-alaska-salvaje-1.jpg",    [(50,80,110), (130,170,180), (220,225,230)], 0.55, "cool", "water"),
    ("day-alaska-salvaje-2.jpg",    [(70,80,60), (160,170,120), (220,215,180)], 0.55, "warm", "forest"),
    ("day-alaska-salvaje-3.jpg",    [(70,100,130), (160,180,180), (230,235,235)], 0.55, "cool", "snow"),
    ("day-alaska-salvaje-4.jpg",    [(60,100,130), (140,180,200), (230,235,240)], 0.55, "cool", "snow"),
    ("lodge-alaska-salvaje-1.jpg",  [(60,80,90), (150,160,150), (220,225,220)], 0.55, "cool", "forest"),
    ("lodge-alaska-salvaje-2.jpg",  [(70,90,100), (160,170,170), (225,225,225)], 0.55, "cool", "mountain"),
    ("lodge-alaska-salvaje-3.jpg",  [(50,90,110), (140,180,180), (225,230,230)], 0.55, "cool", "snow"),
    ("lodge-alaska-salvaje-4.jpg",  [(70,80,90), (170,170,170), (225,220,220)], 0.55, "cool", "city"),
]

def add_noise(img, amount=10):
    """Add subtle noise so it feels like a photo, not a flat gradient."""
    px = img.load()
    w, h = img.size
    for _ in range(int(w * h * 0.02)):
        x = random.randint(0, w-1); y = random.randint(0, h-1)
        r, g, b = px[x, y]
        d = random.randint(-amount, amount)
        px[x, y] = (max(0, min(255, r+d)), max(0, min(255, g+d)), max(0, min(255, b+d)))
    return img.filter(ImageFilter.GaussianBlur(0.5))

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def gen(filename, colors, horizon_ratio, accent, style, w=1600, h=1100):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    top, mid, bot = colors
    horizon = int(h * horizon_ratio)

    # Sky gradient
    for y in range(horizon):
        t = y / horizon
        c = lerp(top, mid, t)
        draw.line([(0, y), (w, y)], fill=c)

    # Ground gradient
    for y in range(horizon, h):
        t = (y - horizon) / max(1, (h - horizon))
        c = lerp(mid, bot, t)
        draw.line([(0, y), (w, y)], fill=c)

    # Style-specific silhouettes
    if style == "mountain":
        # Layered mountain silhouettes
        for layer in range(3):
            base = horizon + layer * 30 - 60
            color = lerp(mid, top, 0.7 - layer*0.2)
            n = 6 + layer
            pts = [(0, h)]
            for i in range(n+1):
                x = int(i / n * w)
                peak = base - random.randint(40, 140) - layer*20
                pts.append((x, peak))
            pts.append((w, h))
            draw.polygon(pts, fill=color)
    elif style == "savannah":
        # Acacia-like horizon shapes
        for _ in range(10):
            cx = random.randint(0, w)
            cy = horizon - random.randint(-10, 50)
            r = random.randint(30, 80)
            color = lerp(mid, (40,30,20), 0.6)
            draw.ellipse([cx-r*1.5, cy-r*0.6, cx+r*1.5, cy+r*0.6], fill=color)
            draw.line([(cx, cy), (cx, cy+r*1.6)], fill=color, width=4)
    elif style == "water":
        # Wave bands
        for i in range(8):
            y = horizon + i * 22
            shade = lerp(mid, bot, i/8)
            draw.line([(0, y), (w, y+random.randint(-6,6))], fill=shade, width=12)
    elif style == "desert":
        # Dune curves
        for layer in range(3):
            color = lerp(mid, bot, 0.4 + layer*0.2)
            base = horizon + layer * 80
            pts = [(0, h)]
            for x in range(0, w+1, 40):
                y = base + int(40 * math.sin(x / 200 + layer))
                pts.append((x, y))
            pts.append((w, h))
            draw.polygon(pts, fill=color)
    elif style == "forest":
        # Tree silhouettes
        for x in range(-20, w+20, 18):
            ty = horizon + random.randint(-20, 30)
            th = random.randint(80, 180)
            color = lerp(mid, (30,40,20), 0.7)
            draw.polygon([(x-12, ty+th), (x, ty), (x+12, ty+th)], fill=color)
    elif style == "snow":
        # Snowy mountain layers
        for layer in range(2):
            base = horizon + layer * 30 - 40
            color = lerp(mid, (250,250,255), 0.4 - layer*0.2)
            n = 6
            pts = [(0, h)]
            for i in range(n+1):
                x = int(i / n * w)
                peak = base - random.randint(60, 160)
                pts.append((x, peak))
            pts.append((w, h))
            draw.polygon(pts, fill=color)
    elif style == "city":
        # Building silhouettes
        x = 0
        while x < w:
            bw = random.randint(50, 120)
            bh = random.randint(80, 220)
            color = lerp(mid, (30,30,40), 0.6)
            draw.rectangle([x, horizon-bh, x+bw, horizon+20], fill=color)
            x += bw + 4
    elif style == "sky":
        # Cloud streaks
        for _ in range(6):
            y = random.randint(int(horizon*0.3), int(horizon*0.9))
            cw = random.randint(200, 500)
            cx = random.randint(-100, w)
            color = lerp(top, (255,255,255), 0.5)
            draw.ellipse([cx, y, cx+cw, y+30], fill=color)

    # Sun/moon glow
    cx = random.randint(int(w*0.55), int(w*0.85))
    cy = random.randint(int(horizon*0.25), int(horizon*0.55))
    glow = Image.new("RGB", (w, h), (0,0,0))
    gd = ImageDraw.Draw(glow)
    for r in range(180, 0, -20):
        a = int(220 * (1 - r/180))
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(a, int(a*0.85), int(a*0.6)))
    glow = glow.filter(ImageFilter.GaussianBlur(35))
    img = Image.blend(img, glow, 0.18 if accent == "warm" else 0.12)

    img = img.filter(ImageFilter.GaussianBlur(0.8))
    img = add_noise(img, amount=8)
    out = os.path.join(OUT, filename)
    img.save(out, "JPEG", quality=82)
    return out

random.seed(42)
for entry in PALETTE:
    p = gen(*entry)
    print("✓", p.split('/')[-1])

print(f"\nGenerated {len(PALETTE)} images in {OUT}")
