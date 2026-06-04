"""
Page generator for Blisniuk & Amanov.
Generates journey detail pages + region pages from data structures.

Usage: python3 tools/build.py
"""
import os, json, html as html_lib

REPO = "/home/user/blisniukamanov"

# Map of stop name → [lat, lng]. Used to render the interactive Leaflet map.
# Add new stops here when adding a new journey.
STOP_COORDS = {
    # África
    "Nairobi": [-1.2921, 36.8219],
    "Aberdares": [-0.3678, 36.7372],
    "Tarangire": [-3.8278, 36.0186],
    "Manyara y Ngorongoro": [-3.2403, 35.4881],
    "Manyara": [-3.6500, 35.7833],
    "Ngorongoro": [-3.2403, 35.4881],
    "Serengeti central": [-2.3333, 34.8333],
    "Kogatende": [-1.6700, 34.9000],
    "Reserva privada Naboisho": [-1.4400, 35.3500],
    "Naboisho": [-1.4400, 35.3500],
    "Masai Mara": [-1.4400, 35.1500],
    "Arusha": [-3.3869, 36.6830],
    "Pejeta": [0.0167, 36.9000],
    "Johannesburgo": [-26.2041, 28.0473],
    "Livingstone": [-17.8419, 25.8543],
    "Cataratas Victoria": [-17.9243, 25.8572],
    "Chobe": [-18.7833, 25.0500],
    "Sabi Sands": [-24.7833, 31.3833],
    "Khwai": [-19.1500, 23.7833],
    "Delta del Okavango": [-19.2833, 22.8000],
    "Maun": [-19.9800, 23.4200],
    # Sudamérica
    "Buenos Aires": [-34.6037, -58.3816],
    "El Calafate": [-50.3403, -72.2647],
    "Perito Moreno": [-50.4861, -73.0306],
    "Torres del Paine": [-51.0000, -73.0000],
    "Puerto Natales": [-51.7236, -72.5167],
    "Ushuaia": [-54.8019, -68.3030],
    "Canal Beagle": [-54.8500, -68.3000],
    "Manaos": [-3.1190, -60.0217],
    "Río Negro": [-3.0000, -60.0000],
    "Anavilhanas": [-2.4500, -60.7500],
    "Cuiabá": [-15.6014, -56.0979],
    "Transpantaneira": [-16.5333, -56.7500],
    "Porto Jofre": [-17.3500, -56.8000],
    "Foz do Iguaçú": [-25.5163, -54.5854],
    "Lima": [-12.0464, -77.0428],
    "Cuzco": [-13.5320, -71.9675],
    "Valle Sagrado": [-13.3167, -72.0833],
    "Ollantaytambo": [-13.2583, -72.2625],
    "Aguas Calientes": [-13.1631, -72.5286],
    "Machu Picchu": [-13.1631, -72.5450],
    # Europa
    "Milán": [45.4642, 9.1900],
    "Turín": [45.0703, 7.6869],
    "Sestri Levante": [44.2733, 9.4000],
    "Portovenere": [44.0489, 9.8389],
    "Parma": [44.8015, 10.3279],
    "Lago di Como": [45.9700, 9.2500],
    "Bolonia": [44.4949, 11.3426],
    "Venecia": [45.4408, 12.3155],
    "Santo Stefano Belbo": [44.7115, 8.2434],
    "Canelli": [44.7222, 8.2933],
    "Barbaresco": [44.7232, 8.0788],
    "Treiso": [44.6843, 8.0530],
    "Alba": [44.7000, 8.0333],
    "Pollenzo": [44.7034, 7.8983],
    "Bra": [44.6989, 7.8589],
    "Barolo": [44.6125, 7.9436],
    "Lisboa": [38.7223, -9.1393],
    "Évora": [38.5667, -7.9000],
    "Sevilla": [37.3886, -5.9823],
    "Granada": [37.1773, -3.5986],
    "Córdoba": [37.8847, -4.7794],
    "Madrid": [40.4168, -3.7038],
    "Toledo": [39.8628, -4.0273],
    "Bilbao": [43.2630, -2.9350],
    "Barcelona": [41.3851, 2.1734],
    # Asia
    "Tokio": [35.6762, 139.6503],
    "Hakone": [35.2329, 139.1058],
    "Kioto": [35.0116, 135.7681],
    "Nara": [34.6851, 135.8048],
    "Osaka": [34.6937, 135.5023],
    "Hanoi": [21.0285, 105.8542],
    "Ha Long Bay": [20.9101, 107.1839],
    "Hai Phong": [20.8449, 106.6881],
    "Ho Chi Minh": [10.8231, 106.6297],
    "Siem Reap": [13.3633, 103.8564],
    "Luang Prabang": [19.8845, 102.1348],
    "Bangkok": [13.7563, 100.5018],
    "Delhi": [28.7041, 77.1025],
    "Agra": [27.1767, 78.0081],
    "Ranthambore": [26.0173, 76.5026],
    "Jaipur": [26.9124, 75.7873],
    "Udaipur": [24.5854, 73.7125],
    # Norte de África / Oriente Medio
    "El Cairo": [30.0444, 31.2357],
    "Saqqara": [29.8714, 31.2167],
    "Luxor": [25.6872, 32.6396],
    "Edfu": [24.9779, 32.8731],
    "Kom Ombo": [24.4658, 32.9281],
    "Asuán": [24.0889, 32.8998],
    "Abu Simbel": [22.3372, 31.6258],
    # Norteamérica
    "Anchorage": [61.2181, -149.9003],
    "Seward": [60.1042, -149.4422],
    "Kenai Fjords": [59.9197, -149.6500],
    "Talkeetna": [62.3208, -150.1078],
    "Denali": [63.0695, -151.0070],
    "Wasilla": [61.5814, -149.4394],
    "Lake Clark": [59.8200, -153.4500],
    "Aialik Glacier": [59.8800, -149.7000],
    "Heritage Center Anchorage": [61.2078, -149.7464],
    # Uzbekistán
    "Tashkent": [41.2995, 69.2401],
    "Khiva": [41.3782, 60.3589],
    "Ayaz Kala": [42.0250, 60.9719],
    "Bujará": [39.7681, 64.4556],
    "Gijduvan": [40.1014, 64.6750],
    "Konigil": [39.7050, 67.0500],
    "Samarcanda": [39.6542, 66.9597],
    "Shahrisabz": [39.0517, 66.8333],
    # Namibia
    "Windhoek": [-22.5594, 17.0832],
    "Sossusvlei": [-24.7297, 15.2939],
    "NamibRand": [-25.0000, 16.0000],
    "Skeleton Coast": [-19.9000, 13.0500],
    "Cape Cross": [-21.7667, 13.9667],
    "Twyfelfontein": [-20.5917, 14.3722],
    "Onduli Ridge": [-20.4500, 14.5000],
    "Etosha": [-18.7500, 16.9500],
    # Laponia (Finlandia + Noruega)
    "Helsinki": [60.1699, 24.9384],
    "Inari": [68.9050, 27.0289],
    "Ivalo": [68.6592, 27.5392],
    "Sodankylä": [67.4187, 26.5919],
    "Tromsø": [69.6492, 18.9553],
    "Djupvik": [69.7000, 20.5500],
    "Lyngen Alps": [69.6000, 20.0000],
    "Lyngenfjord": [69.8000, 20.3000],
    # Bahía
    "Salvador": [-12.9714, -38.5014],
    "Cachoeira": [-12.6064, -38.9583],
    "Porto Seguro": [-16.4350, -39.0808],
    "Trancoso": [-16.5894, -39.0950],
    "Praia dos Nativos": [-16.5950, -39.1000],
    "Caraíva": [-16.8089, -39.1444],
    "Aldeia Jaqueira": [-16.4500, -39.1500],
    "Praia do Espelho": [-16.7783, -39.0822],
    # Japón (mono-no-aware ampliación)
    "Asakusa": [35.7148, 139.7967],
    "Kanazawa": [36.5613, 136.6562],
    "Arashiyama": [35.0094, 135.6661],
    "Naoshima": [34.4570, 133.9885],
    "Teshima": [34.4953, 134.0739],
    # Bután + Nepal
    "Kathmandu": [27.7172, 85.3240],
    "Boudhanath": [27.7215, 85.3617],
    "Bhaktapur": [27.6710, 85.4298],
    "Thimphu": [27.4728, 89.6390],
    "Punakha": [27.5907, 89.8773],
    "Gangtey": [27.4523, 90.1660],
    "Paro": [27.4287, 89.4164],
    "Tiger's Nest": [27.4914, 89.3635],
    # Marruecos
    "Casablanca": [33.3675, -7.5897],
    "Rabat": [34.0209, -6.8416],
    "Volubilis": [34.0739, -5.5567],
    "Mequínez": [33.8935, -5.5547],
    "Fez": [34.0631, -4.9743],
    "Imlil": [31.1390, -7.9170],
    "Aremd": [31.1300, -7.9200],
    "Marrakech": [31.6295, -7.9811],
    # Croacia
    "Split": [43.5081, 16.4402],
    "Brač": [43.2614, 16.6481],
    "Hvar": [43.1729, 16.4413],
    "Vis": [43.0492, 16.1808],
    "Korčula": [42.9621, 17.1366],
    "Mljet": [42.7847, 17.3411],
    "Ston": [42.8345, 17.6928],
    "Dubrovnik": [42.6507, 18.0944],
}

# =============================================================================
# COMMON BLOCKS
# =============================================================================
HEAD = lambda title, desc: f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Cormorant+Garamond:ital,wght@0,300;1,300&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>"""

UTILITY_BAR = """  <div class="utility-bar">
    <div class="utility-inner">
      <div class="utility-left">
        <a href="tel:+541161395550" class="speak">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.86 19.86 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.86 19.86 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.91.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7a2 2 0 0 1 1.72 2.03z"/></svg>
          Hablar con un experto · +54 11 6139 5550
        </a>
        <span class="utility-status">· Atendemos hoy de 9:00 a 20:00</span>
      </div>
      <div class="utility-right">
        <a href="#newsletter">Suscribirme</a>
        <span class="dot"></span>
        <a href="catalogos.html">Catálogos</a>
      </div>
    </div>
  </div>"""

HEADER = """  <header class="site-header" id="siteHeader">
    <div class="header-inner">
      <div class="nav-left">
        <button class="menu-trigger" id="menuTrigger" aria-label="Abrir menú">
          <span class="bars"><span></span><span></span><span></span></span> Menú
        </button>
        <a href="destinations.html">Destinos</a>
        <a href="journeys.html">Viajes</a>
        <a href="index.html#sanctuary">Casas B&amp;A</a>
      </div>
      <a href="index.html" class="brand"><span class="brand-wordmark">BLISNIUK <span class="brand-amp">&amp;</span> AMANOV</span></a>
      <div class="nav-right">
        <a href="journeys.html" class="search-trigger">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          Encontrar tu viaje
        </a>
      </div>
    </div>
  </header>

  <aside class="mobile-drawer" id="mobileDrawer" aria-hidden="true">
    <div class="drawer-inner">
      <a href="destinations.html">Destinos</a>
      <a href="journeys.html">Viajes</a>
      <a href="index.html#sanctuary">Casas B&amp;A</a>
      <a href="contact.html" class="btn btn-dark">Contacto</a>
    </div>
  </aside>"""

FOOTER = """  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <div class="footer-brand-row">
          <span class="footer-mark">B&amp;a</span>
          <h3>Blisniuk &amp; Amanov</h3>
        </div>
        <p>Casa de viajes en pequeño grupo y a medida. Casa central en <a href="https://maps.google.com/?q=Manuel+Ugarte+2035+Buenos+Aires" target="_blank" rel="noopener" style="color:rgba(255,255,255,0.85); border-bottom:1px solid rgba(255,255,255,0.3);">Manuel Ugarte 2035, Buenos Aires</a>.</p>
        <div class="socials">
          <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M7 2C4.24 2 2 4.24 2 7v10c0 2.76 2.24 5 5 5h10c2.76 0 5-2.24 5-5V7c0-2.76-2.24-5-5-5H7zm10 2c1.66 0 3 1.34 3 3v10c0 1.66-1.34 3-3 3H7c-1.66 0-3-1.34-3-3V7c0-1.66 1.34-3 3-3h10zm-5 3a5 5 0 100 10 5 5 0 000-10zm0 2a3 3 0 110 6 3 3 0 010-6zm5.5-.5a1 1 0 100 2 1 1 0 000-2z"/></svg></a>
          <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M22 12a10 10 0 10-11.5 9.9v-7H8v-3h2.5V9.5C10.5 7 12 5.7 14.2 5.7c1 0 2.1.2 2.1.2v2.3H15c-1.2 0-1.5.7-1.5 1.5V12H17l-.4 3h-3.1v7A10 10 0 0022 12z"/></svg></a>
        </div>
      </div>
      <div class="footer-col"><h5>Compañía</h5><ul><li><a href="heritage.html">Nuestra historia</a></li><li><a href="filantropia.html">Filantropía B&amp;A</a></li><li><a href="contact.html">Contacto</a></li></ul></div>
      <div class="footer-col"><h5>Servicios</h5><ul><li><a href="catalogos.html">Catálogos</a></li><li><a href="journeys.html">Todos los viajes</a></li><li><a href="small-group.html">Pequeñas expediciones</a></li><li><a href="destinations.html">Destinos</a></li></ul></div>
      <div class="footer-col"><h5>Legal</h5><ul><li><a href="terminos.html">Términos y condiciones</a></li><li><a href="privacidad.html">Privacidad</a></li><li><a href="cookies.html">Cookies</a></li></ul></div>
    </div>
    <div class="footer-bottom">© 2026 Blisniuk &amp; Amanov S.A. · RNAV Legajo 20943</div>
  </footer>

  <script src="script.js"></script>
</body>
</html>"""

# =============================================================================
# JOURNEY TEMPLATE
# =============================================================================
def build_journey(j):
    # Coords first (used by days for data-stop-index)
    coords_data = []
    for s in j['stops']:
        if s in STOP_COORDS:
            lat, lng = STOP_COORDS[s]
            coords_data.append({"name": s, "lat": lat, "lng": lng})
    coords_json = json.dumps(coords_data, ensure_ascii=False).replace("'", "&#39;")
    stops_html = "\n".join([f'          <li><span>{i+1}</span> {s}</li>' for i, s in enumerate(j['stops'])])

    days_html_items = []
    n_stops = max(1, len(coords_data))
    for i, d in enumerate(j['days']):
        stop_idx = min(i, n_stops - 1) if coords_data else 0
        days_html_items.append(
            f"""      <article class="day" data-day="{d['n']:02d}" data-stop-index="{stop_idx}">
        <div class="day-text">
          <span class="day-num">{d['label']}</span>
          <h3>{d['title']}</h3>
          <p>{d['body']}</p>
          <p class="day-meta"><strong>Comidas:</strong> {d['meals']} · <strong>Alojamiento:</strong> {d['lodging']}</p>
        </div>
        <div class="day-img"><img src="assets/img/{d['img']}" alt="{d['title']}" /></div>
      </article>"""
        )
    days_html = "\n".join(days_html_items)
    lodges_html = "\n".join([
        f"""        <a href="#" class="lodge-card">
          <img src="assets/img/{l['img']}" alt="{l['name']}" />
          <h4>{l['name']}</h4>
          <p>{l['where']}</p>
        </a>""" for l in j['lodges']
    ])
    exts_html = "\n".join([
        f"""        <a href="#" class="ext-card">
          <img src="assets/img/{e['img']}" alt="{e['title']}" />
          <div class="ext-body">
            <small>{e['meta']}</small>
            <h4>{e['title']}</h4>
            <p>{e['body']}</p>
          </div>
        </a>""" for e in j['extensions']
    ])
    dates_html = "\n".join([
        f"""            <tr><td>{d['date']}</td><td><span class="dot-status {d['status_class']}"></span> {d['status']}</td><td>{d['price']}</td><td><a href="#" class="link-arrow">Reservar →</a></td></tr>"""
        for d in j['dates']
    ])
    similar_html = "\n".join([
        f"""        <a href="{s['href']}" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/{s['img']}" alt="{s['title']}" />
          <span class="label-pill">{s['pill']}</span>
          <div class="img-card-body">
            <small>Pequeño grupo</small>
            <h3>{s['title']}</h3>
          </div>
        </a>""" for s in j['similar']
    ])
    incl_html = "\n".join([f"          <li>{x}</li>" for x in j['includes']])
    excl_html = ""
    if j.get('excludes'):
        items = "\n".join([f"          <li>{x}</li>" for x in j['excludes']])
        excl_html = f"""
        <h3 class="excludes-head">Lo que no incluye</h3>
        <ul class="check-list excludes-list">
{items}
        </ul>"""

    return f"""{HEAD(j['title'] + ' · Blisniuk & Amanov', j['meta_desc'])}

{UTILITY_BAR}
{HEADER}

  <section class="journey-detail-hero">
    <img src="assets/img/{j['hero']}" alt="{j['hero_alt']}" />
    <div class="container journey-hero-inner">
      <nav class="breadcrumb light">
        <a href="journeys.html">Viajes</a>
        <span>/</span>
        <a href="small-group.html">Pequeñas expediciones</a>
        <span>/</span>
        <span class="current">{j['title']}</span>
      </nav>
      <span class="eyebrow light">{j['eyebrow']}</span>
      <h1>{j['headline']}</h1>
      {f'<p class="hero-sub"><em>{j["subtitle"]}</em></p>' if j.get('subtitle') else ''}
      <a href="#fechas" class="btn btn-laurel">Ver fechas y precios</a>
    </div>

    <div class="hero-stats">
      <div class="stat-card"><small>Duración</small><strong>{j['duration']}</strong><span>{j['nights']}</span></div>
      <div class="stat-card"><small>Tipo de viaje</small><strong>Pequeño grupo</strong><span>Hasta {j['max_guests']} viajeros</span></div>
      <div class="stat-card"><small>Salidas</small><strong>{j['window']}</strong><span>2026 · 2027</span></div>
      <div class="stat-card"><small>Desde</small><strong>{j['price_from']}</strong><span>Por persona</span></div>
    </div>
  </section>

  <section class="journey-intro">
    <div class="container">
      <div class="intro-grid">
        <div class="intro-text">
          <h2>{j['intro_h2']}</h2>
          <p>{j['intro_p1']}</p>
          <p>{j['intro_p2']}</p>
        </div>
        <div class="intro-portrait"><img src="assets/img/{j['portrait']}" alt="{j['title']}" /></div>
      </div>

      <div class="highlights">
        <div class="highlight"><span class="hi-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a4 4 0 110 8 4 4 0 010-8zM4 22c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg></span><h4>{j['highlights'][0]['t']}</h4><p>{j['highlights'][0]['b']}</p></div>
        <div class="highlight"><span class="hi-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L4 6v6c0 5 3.5 9.5 8 10 4.5-.5 8-5 8-10V6l-8-4z"/></svg></span><h4>{j['highlights'][1]['t']}</h4><p>{j['highlights'][1]['b']}</p></div>
        <div class="highlight"><span class="hi-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 12h18M12 3a15 15 0 010 18M12 3a15 15 0 000 18"/></svg></span><h4>{j['highlights'][2]['t']}</h4><p>{j['highlights'][2]['b']}</p></div>
      </div>
    </div>
  </section>

  <section class="itinerary-sticky">
    <div class="container itinerary-sticky-grid">
      <aside class="itinerary-aside">
        <h2>Itinerario</h2>
        <p class="itin-lede">{j['itin_intro']}</p>
        <div class="map-frame" data-stops='{coords_json}'>
          <img src="assets/img/route-map.jpg" alt="Mapa de la ruta" />
        </div>
        <ul class="map-stops">
{stops_html}
        </ul>
      </aside>
      <div class="itinerary-days">
{days_html}
      </div>
    </div>
  </section>

  <section class="extensions">
    <div class="container">
      <div class="section-head left">
        <h2>Extensiones</h2>
        <p style="color:var(--ink-mute); margin-top: 6px;">Sumá días al final del viaje, con salidas privadas.</p>
      </div>
      <div class="cards-3 ext-grid">
{exts_html}
      </div>
    </div>
  </section>

  <section class="lodges">
    <div class="container">
      <span class="eyebrow">Alojamientos</span>
      <h2>Casas seleccionadas para esta experiencia</h2>
      <div class="lodge-grid">
{lodges_html}
      </div>
    </div>
  </section>

  <section class="dates-prices">
    <div class="container dates-grid">
      <div class="inclusions">
        <h2>Lo que incluye</h2>
        <ul class="check-list">
{incl_html}
        </ul>{excl_html}
      </div>
      <div class="dates-table" id="fechas">
        <h2>Fechas y precios</h2>
        <table>
          <thead><tr><th>Salida</th><th>Disponibilidad</th><th>Precio desde</th><th></th></tr></thead>
          <tbody>
{dates_html}
          </tbody>
        </table>
        <p class="dates-note">Precios por persona en habitación doble. Suplemento de habitación individual a consultar.</p>
      </div>
    </div>
  </section>

  <section class="similar">
    <div class="container">
      <span class="eyebrow">También podría interesarte</span>
      <h2>Otros viajes en pequeño grupo</h2>
      <div class="cards-4">
{similar_html}
      </div>
    </div>
  </section>

{FOOTER}"""

# =============================================================================
# REGION TEMPLATE
# =============================================================================
def build_region(r):
    countries_html = "\n".join([
        f"""        <a href="{c.get('href', '#')}" class="country-card">
          <img src="assets/img/{c['img']}" alt="{c['name']}" />
          <div class="country-body">
            <h3>{c['name']}</h3>
            <p>{c['blurb']}</p>
            {f'<span class="country-cta">Ver el viaje →</span>' if c.get('href') else ''}
          </div>
        </a>""" for c in r['countries']
    ])
    return f"""{HEAD('Explorar ' + r['name'] + ' · Blisniuk & Amanov', r['meta_desc'])}

{UTILITY_BAR}
{HEADER}

  <nav class="subnav">
    <div class="subnav-inner">
      <a href="#paises" class="active">{r['nav_label']}</a>
      <a href="#formas">Formas de explorar</a>
    </div>
  </nav>

  <section class="region-hero">
    <div class="region-hero-image">
      <img src="assets/img/{r['hero']}" alt="{r['name']}" />
      <div class="region-hero-overlay">
        <h1>Explorá {r['name']}</h1>
        <a href="#paises" class="btn btn-outline-light">{r['cta']} ↓</a>
      </div>
    </div>
    <div class="region-hero-content">
      <nav class="breadcrumb">
        <a href="index.html">Inicio</a>
        <span>/</span>
        <a href="destinations.html">Todos los destinos</a>
        <span>/</span>
        <span class="current">{r['name']}</span>
      </nav>
      <p class="region-lede"><em>{r['lede']}</em></p>
      <p>{r['body']}</p>
    </div>
  </section>

  <section class="region-countries" id="paises">
    <div class="container">
      <h2>Descubrí dónde podemos llevarte</h2>
      <div class="countries-grid">
{countries_html}
      </div>
    </div>
  </section>

  <section class="section ways-explore" id="formas">
    <div class="container">
      <div class="section-head left">
        <h2>Formas de explorar</h2>
      </div>
      <div class="cards-3" style="grid-template-columns: repeat(4, 1fr);">
        <a href="small-group.html" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-group.jpg" alt="Pequeñas expediciones" />
          <div class="img-card-body"><h3>Pequeñas expediciones</h3><p>Aventuras compartidas con un máximo de dieciséis viajeros.</p></div>
        </a>
        <a href="journeys.html" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-private.jpg" alt="Viaje privado" />
          <div class="img-card-body"><h3>Viaje privado</h3><p>A medida, en exclusiva, desde el primer trayecto hasta la última cena.</p></div>
        </a>
        <a href="#" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-cruise.jpg" alt="Crucero" />
          <div class="img-card-body"><h3>Cruceros</h3><p>Llegar al lugar al ritmo del agua.</p></div>
        </a>
        <a href="#" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-jet.jpg" alt="Jet privado" />
          <div class="img-card-body"><h3>Jet privado</h3><p>Vuelo de altura para itinerarios singulares.</p></div>
        </a>
      </div>
    </div>
  </section>

{FOOTER}"""

# =============================================================================
# DATA
# =============================================================================
DEFAULT_INCLUDES = [
    "Todos los traslados internos en avioneta y vehículo privado",
    "Pensión completa o media pensión según el itinerario",
    "Líder de viaje hispanohablante",
    "Guías locales especializados",
    "Tasas de ingreso a parques y reservas",
    "Seguro de asistencia al viajero",
    "Aporte a la fundación local de conservación",
]

JOURNEYS = [
    {
        "slug": "piamonte-tartufo",
        "title": "Piamonte",
        "headline": "Piamonte",
        "subtitle": "Tartufo, Nebbiolo y Pavese · Edición octubre 2026",
        "eyebrow": "Pequeño grupo · Italia · Otoño",
        "meta_desc": "Ocho días en las Langhe en el peak de la temporada del tartufo bianco. Bodegas históricas, caza al amanecer y la casa natal de Pavese. La única ventana del año en que todo coincide al mismo tiempo.",
        "hero": "hero-piamonte-tartufo.jpg", "hero_alt": "Viñedos de las Langhe en octubre con niebla baja",
        "portrait": "wildlife-piamonte-tartufo.jpg",
        "duration": "8 días", "nights": "7 noches", "max_guests": 8,
        "window": "Octubre", "price_from": "$8,450 USD",
        "intro_h2": "Ocho días en el Piamonte gastronómico y literario, en la única ventana del año en que todo sucede al mismo tiempo.",
        "intro_p1": "A mediados de octubre, las Langhe entran en su momento más pleno: los grandes domaines terminan la cosecha del Nebbiolo, los trifolau salen al amanecer a buscar el primer tartufo bianco de la temporada, las hojas de las viñas se ponen rojas, y los productores chicos están en el ritmo más fértil del año. Ir tres semanas antes de la subasta de Alba significa producto fresco, productores no saturados de prensa, y el campo todavía respirando a su ritmo humano.",
        "intro_p2": "Nos instalamos en una cascina de uso exclusivo en Santo Stefano Belbo — la casa natal de Cesare Pavese, el escenario de <em>La luna y las hogueras</em>. Desde ahí salimos a Barbaresco, Barolo, Pollenzo, las catedrales subterráneas de Canelli. Pero también volvemos cada noche a casa, donde una cocinera del pueblo nos espera, donde el sommelier abre vinos en el jardín, y donde la sobremesa se vuelve el corazón del viaje.",
        "highlights": [
            {"t": "La trufa, al amanecer", "b": "Caza con un trifolau de linaje en los bosques del Belbo, a las cinco y media de la madrugada, seguida del desayuno con frittata de tartufo en su casa familiar."},
            {"t": "El Nebbiolo en tres voces", "b": "Produttori del Barbaresco con sus nueve cru comparados, una visita extendida a Vajra en Barolo, y una cata vertical histórica (1985, 1996, 2004, 2016) en la cascina, moderada por nuestro sommelier."},
            {"t": "La cena donde somos anfitriones", "b": "La última noche cambia el rol: invitamos a las familias productoras que abrieron sus cantinas durante la semana. Asado al fuego en el jardín de la cascina, vinos que ellos traen, mate al final."}
        ],
        "stops": ["Santo Stefano Belbo", "Canelli", "Barbaresco", "Treiso", "Alba", "Pollenzo", "Bra", "Barolo"],
        "itin_intro": "Ocho días, una sola base, un solo grupo. Empezamos en la cascina con una cena cocinada en casa por una cocinera del pueblo y terminamos siete noches después en el mismo jardín, con los productores que conocimos durante la semana sentados a la mesa como nuestros invitados. En el medio: una caza de trufas a las cinco y media de la madrugada, los nueve cru del Barbaresco comparados en una sola cata, las catedrales subterráneas de Canelli, la casa natal de Pavese, una vertical de Nebbiolo en la cascina iluminada por velas, y una cena estrellada en la única terraza del Piamonte donde el ocaso cae sobre las Langhe.",
        "days": [
            {"n": 1, "label": "Día 1 · Llegada", "title": "Bienvenida en la cascina", "body": "Llegadas escalonadas desde Torino o Milán. Check-in en la casa de Santo Stefano Belbo. Aperitivo en el jardín con vermut local y Moscato d'Asti, cena de bienvenida cocinada por la cocinera del pueblo: tajarin al ragù, brasato al Barolo, bonet. El sommelier presenta el viaje.", "meals": "Cena", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-1.jpg"},
            {"n": 2, "label": "Día 2 · Pavese y Canelli", "title": "La casa del escritor y las catedrales subterráneas", "body": "Caminata por Santo Stefano Belbo y visita a la Fondazione Cesare Pavese y la casa natal. Almuerzo en la Enoteca Regionale di Canelli. Por la tarde, descenso a las Catedrales Subterráneas de Canelli, las antiguas bodegas históricas de espumantes inscriptas por UNESCO. Cata final. Cena ligera en casa.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-2.jpg"},
            {"n": 3, "label": "Día 3 · Barbaresco", "title": "Los nueve cru", "body": "Visita y cata comparativa en Produttori del Barbaresco — los nueve cru Riserva en una sola sesión. Almuerzo en Trattoria Antica Torre, en el corazón del pueblo. Por la tarde, cata íntima en Roagna: Barbaresco artesanal, sin filtración. Vuelta vía el Bricco di Treiso para el ocaso. Cena en casa con sobremesa larga.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-3.jpg"},
            {"n": 4, "label": "Día 4 · La trufa", "title": "Amanecer en el bosque y cena estrellada", "body": "5:30 caza con trifolau y su lagotto romagnolo, seguida del desayuno en su casa familiar. Vuelta a la cascina para una larga siesta. Por la tarde, MUDET — Museo del Tartufo en Alba y paseo por el centro histórico. La cena, en la terraza de La Ciau del Tornavento (1 estrella Michelin), justo cuando el ocaso cae sobre las Langhe.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-4.jpg"},
            {"n": 5, "label": "Día 5 · Pollenzo y Bra", "title": "La idea del Slow Food", "body": "Mañana en la Università di Scienze Gastronomiche de Pollenzo con una sesión sobre el manifiesto del Slow Food, la biodiversidad alimentaria y los Presidi. Almuerzo en el Albergo dell'Agenzia. Tarde en la Banca del Vino (350.000 botellas conservadas) y caminata por Bra, la ciudad donde nació el movimiento en 1986. Aperitivo en Boccondivino, el restaurante fundacional. Cena ligera en casa.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-2.jpg"},
            {"n": 6, "label": "Día 6 · Barolo", "title": "El Nebbiolo y la vertical histórica", "body": "Visita extendida y cata vertical en G.D. Vajra, con almuerzo en cantina junto a la familia Vaira. Por la tarde, WiMu — Museo del Vino en el Castello di Barolo, y mirador de La Morra. Cena en casa preparada por la cocinera, y a las 22:30 la cata histórica vertical: cuatro Nebbiolos de 1985, 1996, 2004 y 2016, moderada por nuestro sommelier.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-3.jpg"},
            {"n": 7, "label": "Día 7 · La noche B&A", "title": "Cuando nosotros somos los anfitriones", "body": "Mañana libre — caminata opcional por el Sentiero Pavesiano o tarde tranquila en el jardín. Visita opcional al productor de avellana Tonda Gentile o al quesero de Castelmagno. A la noche, la cena B&A: las familias productoras que abrieron sus cantinas durante la semana llegan como nuestros invitados. Asado al fuego en el patio de la cascina, vinos que ellos traen, mate y dulce de leche al final. Lectura del último párrafo de <em>La luna y las hogueras</em>.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-1.jpg"},
            {"n": 8, "label": "Día 8 · Despedida", "title": "Vuelta", "body": "Desayuno tranquilo. Traslados escalonados a Torino Caselle o Milán Malpensa según horarios de vuelo. Parada opcional en Asti o Cherasco camino al aeropuerto.", "meals": "Desayuno", "lodging": "—", "img": "day-piamonte-tartufo-4.jpg"},
        ],
        "lodges": [
            {"name": "Cascina privada Santo Stefano Belbo", "where": "Santo Stefano Belbo, Langa Astigiana, Cuneo", "img": "lodge-piamonte-tartufo-1.jpg"},
            {"name": "Cantine Contratto · Catedrales Subterráneas", "where": "Canelli — Patrimonio UNESCO", "img": "lodge-piamonte-tartufo-2.jpg"},
            {"name": "G.D. Vajra", "where": "Vergne, Barolo", "img": "lodge-piamonte-tartufo-3.jpg"},
            {"name": "La Ciau del Tornavento", "where": "Treiso · 1 estrella Michelin", "img": "lodge-piamonte-tartufo-4.jpg"},
        ],
        "extensions": [
            {"meta": "+2 días · desde $1,450 USD", "title": "Torino antes · capital del Risorgimento", "body": "Caffè reales (Al Bicerin, Mulassano), Museo Egizio (el segundo más grande del mundo), Pinacoteca Agnelli y una cata de vermut en Carpano.", "img": "dest-italy.jpg"},
            {"meta": "+3 días · desde $2,850 USD", "title": "Lago di Como después · descompresión", "body": "Bellagio, Villa Carlotta, Villa del Balbianello y dos noches en Villa d'Este. El descanso después de las Langhe, con el ritmo del lago.", "img": "dest-europe.jpg"},
            {"meta": "+2 días · desde $1,650 USD", "title": "Milán antes · diseño y Triennale", "body": "Triennale di Milano, Fondazione Prada, Bagatti Valsecchi y una cena en Cracco. La precondición urbana al campo.", "img": "j-italy.jpg"},
        ],
        "dates": [
            {"date": "Vie 16 oct – Vie 23 oct 2026", "status": "Abierta", "status_class": "open", "price": "$8,450"},
            {"date": "Vie 15 oct – Vie 22 oct 2027", "status": "Abierta", "status_class": "open", "price": "$9,750"},
        ],
        "similar": [
            {"href": "croacia-islas-dalmatas.html", "img": "hero-croacia-islas-dalmatas.jpg", "pill": "9 días", "title": "Croacia"},
            {"href": "japon-mono-no-aware.html", "img": "hero-japon-mono-no-aware.jpg", "pill": "12 días", "title": "Japón · sakura"},
            {"href": "marruecos-imperial.html", "img": "hero-marruecos-imperial.jpg", "pill": "10 días", "title": "Marruecos"},
            {"href": "uzbekistan-ruta-seda.html", "img": "hero-uzbekistan-ruta-seda.jpg", "pill": "11 días", "title": "Uzbekistán"},
        ],
        "includes": [
            "7 noches en cascina privada en Santo Stefano Belbo (uso exclusivo del grupo)",
            "Pensión completa: 7 desayunos, 7 almuerzos, 7 cenas",
            "Cocinera local que prepara los desayunos y las cenas en casa",
            "1 cena en restaurante 1 estrella Michelin (La Ciau del Tornavento)",
            "Cata histórica vertical de Nebbiolo (4 añadas: 1985, 1996, 2004, 2016) en la cascina",
            "Caza de tartufo bianco al amanecer con trifolau de linaje + desayuno en su casa",
            "Visitas y catas con productores: Produttori del Barbaresco, Roagna, G.D. Vajra",
            "Visita a las Catedrales Subterráneas de Canelli (Patrimonio UNESCO)",
            "Visita a la Fondazione Cesare Pavese y la casa natal",
            "Sesión académica en Università di Scienze Gastronomiche, Pollenzo",
            "Visita guiada a la Banca del Vino, Pollenzo",
            "MUDET — Museo del Tartufo, Alba",
            "WiMu — Museo del Vino, Castello di Barolo",
            "La cena B&amp;A en la cascina (productores invitados, asado al fuego)",
            "Sommelier italoparlante acompañando al grupo toda la semana",
            "Fotógrafo profesional documentando los 8 días + libro custom impreso para cada pasajero",
            "Kit B&amp;A pre-viaje: 5 libros (incluyendo <em>La luna y las hogueras</em> de Pavese), journal de cuero, mapa de las Langhe, carta de bienvenida",
            "Detalles diarios: flores frescas, cartas manuscritas con el plan del día",
            "Dos furgones privados con chofer durante los 8 días",
            "Traslados aeropuerto-cascina-aeropuerto (Torino Caselle o Milán Malpensa)",
            "Anfitrión B&amp;A en piso durante toda la semana",
            "Aporte a la Fundación B&amp;A (3% del valor del viaje)",
        ],
        "excludes": [
            "Vuelos internacionales desde/hacia Latinoamérica",
            "Seguro de viaje (B&amp;A lo coordina a costo)",
            "Bebidas premium y vinos de cellar fuera del programa",
            "Gastos personales y compras (incluida la trufa que cada pasajero quiera llevar)",
            "Propinas opcionales para el equipo en piso",
            "Extensiones pre y post viaje (cotizadas por separado)",
        ],
    },
    {
        "slug": "uzbekistan-ruta-seda",
        "title": "Uzbekistán",
        "headline": "Uzbekistán",
        "subtitle": "Tesoros de la Ruta de la Seda · Edición septiembre 2026",
        "eyebrow": "Pequeña expedición · Asia Central",
        "meta_desc": "Once días por las tres ciudades-oasis de la antigua Ruta de la Seda, con acceso a sitios fuera de hora, historiadores en piso y noches en madrasas convertidas en hoteles boutique. Salidas septiembre 2026.",
        "hero": "hero-uzbekistan-ruta-seda.jpg", "hero_alt": "Plaza Registán de Samarcanda al ocaso",
        "portrait": "wildlife-uzbekistan-ruta-seda.jpg",
        "duration": "11 días", "nights": "10 noches", "max_guests": 8,
        "window": "Septiembre", "price_from": "$9,800 USD",
        "intro_h2": "Tres ciudades-oasis donde Asia, Persia y Europa se hablaron durante dos mil años.",
        "intro_p1": "Uzbekistán es el corazón redescubierto de la Ruta de la Seda. Durante mil años, las caravanas que cruzaban entre China y el Mediterráneo se detenían a comerciar, dormir y rezar en Khiva, Bujará y Samarcanda. Hoy las tres ciudades-oasis siguen en pie, en gran parte intactas, con sus madrasas tiladas en azul cobalto, sus zocos cubiertos del siglo XV, y sus mausoleos timúridas.",
        "intro_p2": "Las recorremos en orden geográfico —de oeste a este, como las caravanas— en grupo pequeño, con historiador en piso, acceso fuera de hora a la Plaza Registán de Samarcanda y al Corán de Caliph Uthman (original del siglo VII), y noches en madrasas convertidas en hoteles boutique. Once días para entender por qué Bujará fue capital del Imperio Samánida, y por qué Samarcanda fue durante un siglo entero la ciudad más rica del planeta.",
        "highlights": [
            {"t": "Registán privado fuera de hora", "b": "La plaza más fotografiada de Asia Central, abierta exclusivamente para nuestro grupo al amanecer, con historiador del sitio explicando los tres madrasas."},
            {"t": "El Corán de Caliph Uthman", "b": "Acceso al manuscrito del siglo VII en Khast Imam, Tashkent — uno de los cuatro Coranes originales que sobreviven en el mundo, en una visita privada con conservador."},
            {"t": "Cruce del Kyzylkum en convoy", "b": "Ocho horas atravesando el desierto rojo entre Khiva y Bujará, con parada en la fortaleza de Ayaz Kala (Corasmia, siglo IV a.C.) y almuerzo en yurta tradicional."}
        ],
        "stops": ["Tashkent", "Khiva", "Ayaz Kala", "Bujará", "Gijduvan", "Konigil", "Samarcanda", "Shahrisabz"],
        "itin_intro": "Once días, tres ciudades-oasis, un solo grupo. Empezamos en Tashkent para aclimatación urbana y acceso al Corán de Uthman, volamos a Khiva por la mañana siguiente, cruzamos el desierto Kyzylkum en convoy hasta Bujará, y cerramos en Samarcanda con el Registán privado al amanecer.",
        "days": [
            {"n": 1, "label": "Día 1 · Llegada", "title": "Llegada a Tashkent", "body": "Recepción privada, traslado al hotel. Cena de bienvenida con presentación del historiador en piso.", "meals": "Cena", "lodging": "Hyatt Regency Tashkent", "img": "day-uzbekistan-ruta-seda-1.jpg"},
            {"n": 2, "label": "Día 2 · El Corán", "title": "Tashkent y el Corán de Uthman", "body": "Visita privada al complejo Khast Imam con conservador. Mausoleo Yunus Khan, mezquita Hazrat Imam. Vuelo doméstico a Urgench, traslado a Khiva.", "meals": "Pensión completa", "lodging": "Orient Star Khiva (madrasa restaurada)", "img": "day-uzbekistan-ruta-seda-2.jpg"},
            {"n": 3, "label": "Días 3 · 4", "title": "Khiva — la ciudad de barro", "body": "Dos días dentro de Itchan Kala, la ciudad amurallada Patrimonio UNESCO. Madrasa Muhammad Amin Khan, mausoleo Pahlavan Mahmud, minarete Kalta Minor (el minarete corto).", "meals": "Pensión completa", "lodging": "Orient Star Khiva", "img": "day-uzbekistan-ruta-seda-2.jpg"},
            {"n": 5, "label": "Día 5 · El Kyzylkum", "title": "Cruce del desierto rojo", "body": "Convoy 4x4 de 8 horas a través del desierto rojo. Parada en Ayaz Kala (fortaleza Corasmia siglo IV a.C.) con almuerzo en yurta. Llegada a Bujará al ocaso.", "meals": "Pensión completa", "lodging": "Komil Boutique Hotel Bujará", "img": "day-uzbekistan-ruta-seda-3.jpg"},
            {"n": 6, "label": "Días 6 · 7", "title": "Bujará — capital samánida", "body": "Dos días en el Bujará antiguo: Mausoleo Samánida (siglo IX), Po-i-Kalyan, Madrasa Mir-i-Arab, Lyab-i-Hauz. Cena Sabbat en la sinagoga bukhari-judía. Demostración de Suzani con maestro tejedor.", "meals": "Pensión completa", "lodging": "Komil Boutique Hotel", "img": "day-uzbekistan-ruta-seda-4.jpg"},
            {"n": 8, "label": "Día 8 · El Afrosiyob", "title": "Bujará → Samarcanda", "body": "Tren de alta velocidad Afrosiyob (1h 30 min). Tarde en Samarcanda: Mezquita Bibi-Khanym, Necrópolis Shah-i-Zinda.", "meals": "Pensión completa", "lodging": "Silk Road Samarkand", "img": "day-uzbekistan-ruta-seda-1.jpg"},
            {"n": 9, "label": "Día 9 · El Registán", "title": "Samarcanda al amanecer", "body": "Acceso privado a la Plaza Registán antes de la apertura pública, con historiador timúrida en piso. Tarde: Mausoleo Gur-e-Amir (tumba de Timur), Observatorio Ulugh Beg.", "meals": "Pensión completa", "lodging": "Silk Road Samarkand", "img": "day-uzbekistan-ruta-seda-4.jpg"},
            {"n": 10, "label": "Día 10 · Shahrisabz", "title": "Papel y cuna de Timur", "body": "Mañana en el molino de papel de Konigil (Davlat Toshev, último maestro del papel de seda samarcandí). Tarde a Shahrisabz, cuna de Timur, con ruinas del Palacio Ak-Saray.", "meals": "Pensión completa", "lodging": "Hyatt Regency Tashkent", "img": "day-uzbekistan-ruta-seda-3.jpg"},
            {"n": 11, "label": "Día 11 · Despedida", "title": "Vuelta", "body": "Mañana libre, traslado a Tashkent International.", "meals": "Desayuno", "lodging": "—", "img": "day-uzbekistan-ruta-seda-1.jpg"},
        ],
        "lodges": [
            {"name": "Hyatt Regency Tashkent", "where": "Tashkent", "img": "lodge-uzbekistan-ruta-seda-4.jpg"},
            {"name": "Orient Star Khiva", "where": "Madrasa restaurada, dentro de Itchan Kala", "img": "lodge-uzbekistan-ruta-seda-1.jpg"},
            {"name": "Komil Boutique Hotel", "where": "Casa-jardín del siglo XIX, Bujará", "img": "lodge-uzbekistan-ruta-seda-2.jpg"},
            {"name": "Silk Road Samarkand", "where": "Samarcanda", "img": "lodge-uzbekistan-ruta-seda-3.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $1,950 USD", "title": "Aral Sea · El desierto del barco", "body": "Vuelo a Nukus + 4x4 a Moynaq, los cementerios de barcos del Mar Aral, una de las catástrofes ambientales del siglo XX.", "img": "dest-asia.jpg"},
            {"meta": "+2 días · desde $1,200 USD", "title": "Fergana Valley · cuna del seda", "body": "Margilan (telares de Atlas-ikat) y Rishtan (cerámica de cobalto).", "img": "j-asia.jpg"},
            {"meta": "+4 días · desde $2,800 USD", "title": "Turkmenistán · Ashgabat y Darvaza", "body": "Cruce frontera oeste a la Puerta del Infierno, el cráter de gas ardiendo desde 1971 en el desierto Karakum.", "img": "dest-mena.jpg"},
        ],
        "dates": [
            {"date": "12 sep 2026", "status": "Abierta", "status_class": "open", "price": "$9,800"},
            {"date": "19 sep 2026", "status": "Pocas plazas", "status_class": "few", "price": "$9,800"},
            {"date": "26 sep 2026", "status": "Abierta", "status_class": "open", "price": "$9,800"},
            {"date": "3 oct 2026", "status": "Abierta", "status_class": "open", "price": "$9,800"},
            {"date": "10 oct 2026", "status": "Lista de espera", "status_class": "wait", "price": "$9,800"},
        ],
        "similar": [
            {"href": "marruecos-imperial.html", "img": "hero-marruecos-imperial.jpg", "pill": "10 días", "title": "Marruecos"},
            {"href": "japon-mono-no-aware.html", "img": "hero-japon-mono-no-aware.jpg", "pill": "12 días", "title": "Japón · sakura"},
            {"href": "butan-nepal-himalaya.html", "img": "hero-butan-nepal-himalaya.jpg", "pill": "13 días", "title": "Bután y Nepal"},
            {"href": "piamonte-tartufo.html", "img": "hero-piamonte-tartufo.jpg", "pill": "8 días", "title": "Piamonte"},
        ],
        "includes": [
            "Vuelo doméstico Tashkent-Urgench",
            "Tren de alta velocidad Bujará-Samarcanda",
            "Convoy 4x4 cruce Kyzylkum con conductor experimentado",
            "Pensión completa (excluyendo bebidas premium)",
            "Historiador en piso bilingüe español-inglés durante 11 días",
            "Acceso fuera de hora a Registán de Samarcanda y Corán de Caliph Uthman",
            "Todas las entradas a sitios y museos",
            "Demostraciones con maestros artesanos (Suzani Bujará, papel Konigil, ikat Margilan)",
            "Kit B&amp;A pre-viaje (libros, journal, mapa de la Ruta de la Seda)",
            "Fotógrafo profesional + libro custom post-viaje",
            "Traslados aeropuerto, propinas a guías",
            "Seguro de viaje",
        ],
        "excludes": [
            "Vuelos internacionales desde Buenos Aires",
            "Visado Uzbekistán (gratis para muchos hispanoparlantes, verificar)",
            "Bebidas alcohólicas premium",
            "Compras personales",
        ],
    },
    {
        "slug": "namibia-dunas",
        "title": "Namibia",
        "headline": "Namibia",
        "subtitle": "Dunas Rojas, Costa de los Esqueletos y Etosha · Edición noviembre 2026",
        "eyebrow": "Pequeña expedición · África",
        "meta_desc": "Once días por Sossusvlei, Costa de los Esqueletos, Damaraland y Etosha. Lodges boutique fly-in, geólogo en piso, intérprete Himba ético y la Vía Láctea desde NamibRand Dark Sky Reserve.",
        "hero": "hero-namibia-dunas.jpg", "hero_alt": "Duna roja gigante al amanecer en Sossusvlei",
        "portrait": "wildlife-namibia-dunas.jpg",
        "duration": "11 días", "nights": "10 noches", "max_guests": 8,
        "window": "Noviembre", "price_from": "$10,800 USD",
        "intro_h2": "El desierto más viejo del mundo, recorrido en su luz más limpia.",
        "intro_p1": "El Namib tiene 55 millones de años — es el desierto más viejo del planeta. Las dunas rojas de Sossusvlei son tan altas como rascacielos. En el Deadvlei los esqueletos de camelthorn de 900 años se recortan contra arcilla blanca y cielo cobalto. Hacia el oeste, el desierto se mete en el Atlántico: la Costa de los Esqueletos, una de las costas más letales del mundo, con barcos hundidos en las dunas y colonias de lobos marinos del Cabo.",
        "intro_p2": "Recorremos cinco escenarios en once días con cinco charters internos: Windhoek, Sossusvlei (Sonop Lodge), NamibRand Dark Sky Reserve, Skeleton Coast (Shipwreck Lodge), Damaraland (Onduli Ridge) y Etosha (Onguma the Fort). Geólogo en piso en Sossusvlei, intérprete Himba ético en Kaokoland, astrónomo en NamibRand, y safari de fauna en Etosha al final de la estación seca cuando los animales concentran en los pocos pozos de agua.",
        "highlights": [
            {"t": "Sossusvlei + Deadvlei con geólogo", "b": "Amanecer en Dune 45 y caminata por las arcillas blancas con esqueletos de camelthorn, con un geólogo explicando los 55 millones de años de formación."},
            {"t": "Visita Himba ética en Kaokoland", "b": "Coordinada con Save the Rhino Trust, con intérprete y protocolo de respeto. Conversación real con familia Himba, no espectáculo turístico."},
            {"t": "Vía Láctea en NamibRand Dark Sky", "b": "Sesión privada con astrónomo en la reserva con clasificación Gold-Tier de la International Dark-Sky Association."}
        ],
        "stops": ["Windhoek", "Sossusvlei", "NamibRand", "Skeleton Coast", "Cape Cross", "Twyfelfontein", "Onduli Ridge", "Etosha"],
        "itin_intro": "Once días, cinco escenarios, cinco charters. De las dunas más altas del mundo a los esqueletos de barcos en el Atlántico, de los elefantes adaptados al desierto al pan de Etosha donde la fauna se concentra al final de la estación seca.",
        "days": [
            {"n": 1, "label": "Día 1 · Llegada", "title": "Llegada a Windhoek", "body": "Vuelo desde BA vía Johannesburgo. Cena en Joe's Beerhouse, oryx y kudu a la parrilla.", "meals": "Cena", "lodging": "Olive Exclusive Windhoek", "img": "day-namibia-dunas-1.jpg"},
            {"n": 2, "label": "Días 2 · 3", "title": "Sossusvlei — el corazón geológico", "body": "Charter a Sossusvlei. Sunrise en Dune 45 y Deadvlei con geólogo. Picnic en duna privada. Ascenso opcional Big Daddy.", "meals": "Pensión completa", "lodging": "Sonop Lodge (palacio italiano sobre kopje)", "img": "day-namibia-dunas-2.jpg"},
            {"n": 4, "label": "Día 4 · NamibRand", "title": "NamibRand → Costa", "body": "Cruce Reserva NamibRand. Sesión astronomía nocturna privada. Charter a Skeleton Coast.", "meals": "Pensión completa", "lodging": "Shipwreck Lodge", "img": "day-namibia-dunas-3.jpg"},
            {"n": 5, "label": "Día 5 · Esqueletos", "title": "Costa de los Esqueletos", "body": "Caminata al shipwreck del Eduard Bohlen (encalló 1909, hoy 400m tierra adentro). Cape Cross — colonia de 100.000 lobos marinos. Champagne al ocaso en playa privada.", "meals": "Pensión completa", "lodging": "Shipwreck Lodge", "img": "day-namibia-dunas-3.jpg"},
            {"n": 6, "label": "Día 6 · Damaraland", "title": "Skeleton Coast → Damaraland", "body": "Charter a Damaraland. Arte rupestre San en Twyfelfontein (UNESCO), 2.000 grabados de hasta 6.000 años.", "meals": "Pensión completa", "lodging": "Onduli Ridge", "img": "day-namibia-dunas-2.jpg"},
            {"n": 7, "label": "Día 7 · Elefantes", "title": "Damaraland — elefantes y geología", "body": "Tracker para elefantes adaptados al desierto. Formaciones Burnt Mountain y Organ Pipes. Cena al aire libre bajo estrellas.", "meals": "Pensión completa", "lodging": "Onduli Ridge", "img": "day-namibia-dunas-4.jpg"},
            {"n": 8, "label": "Día 8 · Himba", "title": "Damaraland — visita Himba", "body": "Visita ética a aldea Himba en Kaokoland con intérprete. Conversación con mujeres en sus chozas de adobe, donde el ocre rojo cubre la piel. Sin invasión fotográfica.", "meals": "Pensión completa", "lodging": "Onduli Ridge", "img": "day-namibia-dunas-4.jpg"},
            {"n": 9, "label": "Día 9 · Etosha", "title": "Damaraland → Etosha", "body": "Charter a Etosha. Game drive en concesión privada Onguma. Sunset al pozo de agua iluminado.", "meals": "Pensión completa", "lodging": "Onguma the Fort", "img": "day-namibia-dunas-2.jpg"},
            {"n": 10, "label": "Día 10 · El gran día", "title": "Etosha — el día grande de fauna", "body": "Day game drive en el pan. Leones, leopardos, rinocerontes negros, elefantes. Cena despedida con preview del fotógrafo.", "meals": "Pensión completa", "lodging": "Onguma the Fort", "img": "day-namibia-dunas-2.jpg"},
            {"n": 11, "label": "Día 11 · Vuelta", "title": "Etosha → Windhoek → partida", "body": "Charter a Windhoek. Vuelos internacionales nocturnos.", "meals": "Desayuno", "lodging": "—", "img": "day-namibia-dunas-1.jpg"},
        ],
        "lodges": [
            {"name": "Sonop Lodge", "where": "Sossusvlei (palacio italiano sobre kopje granítico)", "img": "lodge-namibia-dunas-1.jpg"},
            {"name": "Shipwreck Lodge", "where": "Skeleton Coast (cabañas-barco en dunas)", "img": "lodge-namibia-dunas-2.jpg"},
            {"name": "Onduli Ridge", "where": "Damaraland (lodge boutique, 6 suites)", "img": "lodge-namibia-dunas-3.jpg"},
            {"name": "Onguma the Fort", "where": "Borde oriental Etosha (concesión privada)", "img": "lodge-namibia-dunas-4.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $2,800 USD", "title": "Cataratas Victoria", "body": "Vuelo a Livingstone, dos noches en el Royal Livingstone con vista al spray. Ideal extensión post-Namibia.", "img": "dest-kenya.jpg"},
            {"meta": "+4 días · desde $4,500 USD", "title": "Delta Okavango Botswana", "body": "Mokoros en el delta más grande del mundo sin desembocadura al océano. Combo perfecto con Namibia.", "img": "j-botswana.jpg"},
            {"meta": "+4 días · desde $2,400 USD", "title": "Ciudad del Cabo + viñedos", "body": "Stay en Cape Town, almuerzo en La Colombe, Stellenbosch y Franschhoek.", "img": "dest-spain.jpg"},
        ],
        "dates": [
            {"date": "7 nov 2026", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "14 nov 2026", "status": "Pocas plazas", "status_class": "few", "price": "$10,800"},
            {"date": "21 nov 2026", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "28 nov 2026", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "5 dic 2026", "status": "Lista de espera", "status_class": "wait", "price": "$11,200"},
        ],
        "similar": [
            {"href": "alaska-salvaje.html", "img": "hero-alaska-salvaje.jpg", "pill": "11 días", "title": "Alaska salvaje"},
            {"href": "bahia-otro-carnaval.html", "img": "hero-bahia-otro-carnaval.jpg", "pill": "9 días", "title": "Bahía"},
            {"href": "laponia-auroras.html", "img": "hero-laponia-auroras.jpg", "pill": "10 días", "title": "Laponia"},
            {"href": "butan-nepal-himalaya.html", "img": "hero-butan-nepal-himalaya.jpg", "pill": "13 días", "title": "Bután y Nepal"},
        ],
        "includes": [
            "5 charters internos (Windhoek-Sossus-Skeleton-Damaraland-Etosha-Windhoek)",
            "Pensión completa en todos los lodges",
            "Geólogo en piso Sossusvlei",
            "Intérprete Himba con coordinación Save the Rhino Trust",
            "Astrónomo NamibRand Dark Sky Reserve",
            "Tracker de elefantes adaptados al desierto",
            "Especialista en arte rupestre San (Twyfelfontein)",
            "Game drives ilimitados Etosha + Onguma",
            "Champagne sunset en playa privada Skeleton Coast",
            "Kit B&amp;A pre-viaje (libros, journal, mapa)",
            "Fotógrafo profesional + libro custom",
            "Traslados, propinas a guías de lodge",
        ],
        "excludes": [
            "Vuelos internacionales desde BA (vía Johannesburgo)",
            "Visado Namibia (gratis para argentinos hasta 90 días)",
            "Bebidas premium",
            "Lavandería express",
        ],
    },
    {
        "slug": "laponia-auroras",
        "title": "Laponia",
        "headline": "Laponia",
        "subtitle": "Auroras Boreales y el Reino Sami · Edición enero 2027",
        "eyebrow": "Pequeña expedición · Ártico",
        "meta_desc": "Diez días entre Finlandia y Noruega, en busca de la aurora boreal y la cultura Sami. Cabañas de cristal en Ivalo, ritual sauna-hielo, husky sledding, y Lyngen Lodge en el fiordo ártico noruego.",
        "hero": "hero-laponia-auroras.jpg", "hero_alt": "Aurora boreal verde sobre lago helado",
        "portrait": "wildlife-laponia-auroras.jpg",
        "duration": "10 días", "nights": "9 noches", "max_guests": 8,
        "window": "Enero", "price_from": "$10,800 USD",
        "intro_h2": "La noche polar, la cultura Sami y la aurora boreal en su pico de actividad.",
        "intro_p1": "Laponia es la exacta inversa del desierto: oscuridad de 20 horas en enero, frío que se mete en los huesos, y un cielo que de repente se enciende en cintas verdes y violetas. La aurora boreal —Revontulet en finlandés, los zorros de fuego— está en pico de actividad solar. Pero la profundidad del viaje no es la aurora — es el pueblo Sami, la única población indígena reconocida por la Unión Europea, con su propia bandera, su parlamento (en Inari), nueve lenguas y un sistema cosmológico basado en una relación con el reno.",
        "intro_p2": "Cruzamos dos países —Finlandia y Noruega— y dos paisajes: el bosque boreal de la Laponia finlandesa, y el fiordo ártico noruego del Lyngenfjord. En el medio: cabaña de cristal sobre lago helado, familia de pastores de renos Sami en Inari, ritual sauna y plunge en lago helado, husky sledding, y la ciencia de las auroras explicada por un investigador del Observatorio Geofísico de Sodankylä.",
        "highlights": [
            {"t": "Cabaña de cristal en Aurora Village", "b": "Dormís bajo el cielo polar, la aurora viene a buscarte a la cama. Dos noches en Ivalo."},
            {"t": "Visita a familia Sami de pastores de renos", "b": "Encuentro real (no folclórico) con familia en Inari, conversación con intérprete, joik si la familia lo ofrece."},
            {"t": "Ritual sauna finlandés + plunge en lago helado", "b": "El centro espiritual de la cultura finlandesa: vapor, vihta de abedul, salto al lago a -25C, repetir tres veces."}
        ],
        "stops": ["Helsinki", "Inari", "Ivalo", "Sodankylä", "Tromsø", "Djupvik", "Lyngen Alps", "Lyngenfjord"],
        "itin_intro": "Diez días entre dos países árticos. Helsinki para el primer ritual de sauna, vuelo norte a la Laponia finlandesa para tres días con la cultura Sami y dos noches en cabaña de cristal, cruce a Noruega para el fiordo Lyngen, y husky sledding final entre los Alpes Lyngen.",
        "days": [
            {"n": 1, "label": "Día 1 · Helsinki", "title": "Llegada a Helsinki", "body": "Caminata por el design district (Marimekko, Iittala, Artek). Sauna ritual en Löyly. Cena en Olo (1 Michelin).", "meals": "Cena", "lodging": "Hotel St. George / Kämp", "img": "day-laponia-auroras-1.jpg"},
            {"n": 2, "label": "Día 2 · Vuelo norte", "title": "Helsinki → Laponia finlandesa", "body": "Vuelo a Ivalo (1h 50). Cena Sami tradicional en Wilderness Hotel Inari, propiedad de familia Sami.", "meals": "Pensión completa", "lodging": "Wilderness Hotel Inari", "img": "day-laponia-auroras-2.jpg"},
            {"n": 3, "label": "Día 3 · Sami", "title": "Inari · corazón Sami", "body": "SIIDA Museum con guía Sami. Visita a familia de pastores de renos. Aurora chase nocturna en motoreneves.", "meals": "Pensión completa", "lodging": "Wilderness Hotel Inari", "img": "day-laponia-auroras-2.jpg"},
            {"n": 4, "label": "Días 4 · 5", "title": "Aurora Village Ivalo", "body": "Cabañas de cristal. Husky sledding bosque boreal. Ice fishing. Snowshoes con naturalista. Sesión científica auroras con Sodankylä Observatory. Ritual sauna completo.", "meals": "Pensión completa", "lodging": "Aurora Village Ivalo", "img": "day-laponia-auroras-3.jpg"},
            {"n": 6, "label": "Día 6 · Tromsø", "title": "Vuelo a Tromsø", "body": "Vuelo vía Oslo. Caminata Arctic Cathedral (Ishavskatedralen) y Polar Museum (Amundsen, Nansen). Cena en Smak.", "meals": "Pensión completa", "lodging": "Clarion The Edge Tromsø", "img": "day-laponia-auroras-3.jpg"},
            {"n": 7, "label": "Día 7 · Lyngen", "title": "Tromsø → Lyngen Lodge", "body": "Opcional avistamiento orcas y jorobadas (noviembre-enero peak season). Traslado 2h a Lyngen Lodge — boutique de 9 suites frente al fiordo.", "meals": "Pensión completa", "lodging": "Lyngen Lodge", "img": "day-laponia-auroras-4.jpg"},
            {"n": 8, "label": "Día 8 · Fiordo", "title": "Lyngen — el fiordo", "body": "Opciones: ski touring en Lyngen Alps con guía UIAGM / navegación a comunidad Sea Sami / sauna y jacuzzi contemplativo.", "meals": "Pensión completa", "lodging": "Lyngen Lodge", "img": "day-laponia-auroras-4.jpg"},
            {"n": 9, "label": "Día 9 · Huskies", "title": "Husky sledding en Lyngendalen", "body": "Trineos por el valle Lyngen al fondo de las montañas. Almuerzo al fuego en gamme. Cena de despedida con lectura de Hamsun.", "meals": "Pensión completa", "lodging": "Lyngen Lodge", "img": "day-laponia-auroras-4.jpg"},
            {"n": 10, "label": "Día 10 · Vuelta", "title": "Lyngen → Tromsø → partida", "body": "Traslado 2h a Tromsø aeropuerto. Vuelos internacionales.", "meals": "Desayuno", "lodging": "—", "img": "day-laponia-auroras-1.jpg"},
        ],
        "lodges": [
            {"name": "Hotel St. George o Kämp", "where": "Helsinki (5 estrellas design boutique)", "img": "lodge-laponia-auroras-4.jpg"},
            {"name": "Wilderness Hotel Inari", "where": "Inari, Finlandia (propiedad Sami)", "img": "lodge-laponia-auroras-1.jpg"},
            {"name": "Aurora Village Ivalo", "where": "Ivalo, Finlandia (cabañas de cristal)", "img": "lodge-laponia-auroras-2.jpg"},
            {"name": "Lyngen Lodge", "where": "Djupvik, Noruega (9 suites en fiordo)", "img": "lodge-laponia-auroras-3.jpg"},
        ],
        "extensions": [
            {"meta": "+2 días · desde $1,600 USD", "title": "ICEHOTEL Jukkasjärvi", "body": "El hotel de hielo original en Suecia, una noche en habitación esculpida y otra en cabin caliente.", "img": "dest-arctic.jpg"},
            {"meta": "+4 días · desde $3,400 USD", "title": "Lofoten Islands", "body": "Las islas dramáticas del norte noruego — luz invernal singular, rorbu (cabañas de pescadores), aurora.", "img": "dest-arctic.jpg"},
            {"meta": "+2 días · desde $1,200 USD", "title": "Helsinki + Tallinn", "body": "Pre-trip cultural: ferry rápido a la capital estonia, casco medieval UNESCO.", "img": "dest-europe.jpg"},
        ],
        "dates": [
            {"date": "8 ene 2027", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "15 ene 2027", "status": "Pocas plazas", "status_class": "few", "price": "$10,800"},
            {"date": "22 ene 2027", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "29 ene 2027", "status": "Lista de espera", "status_class": "wait", "price": "$10,800"},
            {"date": "5 feb 2027", "status": "Abierta", "status_class": "open", "price": "$11,200"},
        ],
        "similar": [
            {"href": "alaska-salvaje.html", "img": "hero-alaska-salvaje.jpg", "pill": "11 días", "title": "Alaska salvaje"},
            {"href": "japon-mono-no-aware.html", "img": "hero-japon-mono-no-aware.jpg", "pill": "12 días", "title": "Japón · sakura"},
            {"href": "namibia-dunas.html", "img": "hero-namibia-dunas.jpg", "pill": "11 días", "title": "Namibia"},
            {"href": "butan-nepal-himalaya.html", "img": "hero-butan-nepal-himalaya.jpg", "pill": "13 días", "title": "Bután y Nepal"},
        ],
        "includes": [
            "Vuelos internos (Helsinki-Ivalo, Ivalo-Tromsø vía Oslo)",
            "Pensión completa en lodges (con ajustes en Helsinki y Tromsø)",
            "Equipo térmico para -30C provisto por los lodges",
            "Husky sledding (Aurora Village + Lyngen)",
            "Ice fishing con guía",
            "Ritual sauna finlandés",
            "Visita a familia Sami con intérprete",
            "SIIDA Museum guía especializado",
            "Sesión científica auroras con Sodankylä Observatory",
            "Ski touring guide UIAGM opcional (Lyngen)",
            "Avistamiento orcas opcional (Tromsø)",
            "Kit B&amp;A pre-viaje",
            "Fotógrafo profesional + libro custom",
        ],
        "excludes": [
            "Vuelos internacionales BA-Helsinki",
            "Visado (Schengen, sin requisito para argentinos)",
            "Bebidas premium",
            "Compras personales",
        ],
    },
    {
        "slug": "bahia-otro-carnaval",
        "title": "Bahía",
        "headline": "Bahía",
        "subtitle": "El Otro Carnaval · Salvador, Trancoso y la herencia afrobrasileña · Febrero 2027",
        "eyebrow": "Pequeña expedición · Sudamérica",
        "meta_desc": "Nueve días en el Carnaval más profundo culturalmente del Brasil. Cinco noches en Salvador con antropólogo UFBA, terreiro de candomblé y camarote privado para Filhos de Gandhy. Tres noches de descompresión en Trancoso.",
        "hero": "hero-bahia-otro-carnaval.jpg", "hero_alt": "Procesión Filhos de Gandhy en blanco con turbantes azules",
        "portrait": "wildlife-bahia-otro-carnaval.jpg",
        "duration": "9 días", "nights": "8 noches", "max_guests": 8,
        "window": "Febrero (Carnaval)", "price_from": "$10,200 USD",
        "intro_h2": "El Carnaval del Brasil que importa, sin el caos de Río.",
        "intro_p1": "El Carnaval de Río es global, comercial y mediático. El Carnaval de Salvador es otra cosa: es el más grande del planeta (2 millones de personas en la calle), pero es también el más profundo cultural y políticamente. Ilê Aiyê —el primer bloco afro— se fundó en 1974 como respuesta al Carnaval blanqueado. Filhos de Gandhy sale el domingo con 15.000 hombres vestidos de blanco, hilo azul al cuello. Es la procesión más bella del Carnaval mundial.",
        "intro_p2": "Y detrás del Carnaval: Salvador, el puerto donde entraron 4,5 millones de africanos esclavizados entre 1550 y 1850 — más que toda la América del Norte combinada. Donde el candomblé sigue vivo, donde nació la capoeira, donde el samba de roda del Recôncavo es UNESCO Inmaterial. Nueve días con antropólogo de UFBA en piso, visita educativa a Casa Branca (terreiro fundado en 1830), camarote privado para los dos días clave del Carnaval, y descompresión final en Trancoso.",
        "highlights": [
            {"t": "Camarote privado Filhos de Gandhy", "b": "Box exclusivo para los dos días clave del Carnaval (sábado Ilê Aiyê + domingo Filhos de Gandhy) con catering y antropólogo traduciendo lo que vemos."},
            {"t": "Terreiro de candomblé con antropólogo UFBA", "b": "Visita educativa a Casa Branca (1830, Patrimônio Cultural Brasileiro) con la iyalorixá y profesor de UFBA — no espectáculo, ritual real."},
            {"t": "Praia do Espelho en barco privado", "b": "Día completo en el sur de Bahía: Caraíva, comunidad Pataxó Aldeia Reserva da Jaqueira, y baño en las piscinas naturales del Espelho."}
        ],
        "stops": ["Salvador", "Cachoeira", "Porto Seguro", "Trancoso", "Praia dos Nativos", "Caraíva", "Aldeia Jaqueira", "Praia do Espelho"],
        "itin_intro": "Nueve días que comienzan en el corazón intenso de Salvador y terminan en el silencio de Trancoso. Cinco noches en Salvador para los dos días clave del Carnaval + cultura afrobrasileña profunda + un día al Recôncavo Baiano. Tres noches finales en Trancoso para descomprimir y cerrar con el sur de Bahía.",
        "days": [
            {"n": 1, "label": "Día 1 (mié) · Llegada", "title": "Llegada a Salvador", "body": "Vuelo BA-Salvador (~7h con escala). Aperitivo caipirinhas + acarajé. Presentación del antropólogo UFBA. Cena en Maria Mata Mouro.", "meals": "Cena", "lodging": "Villa Bahia Pelourinho", "img": "day-bahia-otro-carnaval-1.jpg"},
            {"n": 2, "label": "Día 2 (jue) · Pelourinho", "title": "Pelourinho y herencia yoruba", "body": "Caminata UNESCO con antropólogo: Igreja São Francisco (la más dorada del catolicismo americano), Pelourinho Square, Igreja Nossa Senhora do Rosário dos Pretos (construida por esclavos para esclavos). Fundação Pierre Verger. Casa do Carnaval.", "meals": "Pensión completa", "lodging": "Villa Bahia", "img": "day-bahia-otro-carnaval-2.jpg"},
            {"n": 3, "label": "Día 3 (vie) · Capoeira", "title": "Capoeira y candomblé", "body": "Sesión privada con Mestre de Capoeira Angola. Visita educativa a terreiro Casa Branca con iyalorixá. Salida nocturna a Pelourinho — Sextou, capoeira pública.", "meals": "Pensión completa", "lodging": "Villa Bahia", "img": "day-bahia-otro-carnaval-3.jpg"},
            {"n": 4, "label": "Día 4 (sáb) · Ilê Aiyê", "title": "Carnaval Día 1", "body": "Camarote privado Barra-Ondina. Salida histórica de Ilê Aiyê desde Liberdade — 5.000 percussionistas y bailarines con telas africanas.", "meals": "Pensión completa", "lodging": "Villa Bahia", "img": "day-bahia-otro-carnaval-3.jpg"},
            {"n": 5, "label": "Día 5 (dom) · Filhos de Gandhy", "title": "Carnaval Día 2", "body": "Camarote otra vez. Procesión Filhos de Gandhy — 15.000 hombres en blanco con turbante azul. Cena en casa de samba fuera del circuito.", "meals": "Pensión completa", "lodging": "Villa Bahia", "img": "day-bahia-otro-carnaval-1.jpg"},
            {"n": 6, "label": "Día 6 (lun) · Recôncavo", "title": "Recôncavo Baiano → Trancoso", "body": "Salida temprana a Cachoeira — convento São Francisco, museo Hansen Bahia. Almuerzo con familia samba de roda. Vuelo Salvador-Porto Seguro. Traslado a Trancoso.", "meals": "Pensión completa", "lodging": "UXUA Casa Hotel & Spa", "img": "day-bahia-otro-carnaval-4.jpg"},
            {"n": 7, "label": "Día 7 (mar) · Quadrado", "title": "Trancoso — el Quadrado", "body": "Mañana en el Quadrado con iglesia São João Batista (1652). Día completo en Praia dos Nativos con cabaña privada.", "meals": "Pensión completa", "lodging": "UXUA Casa", "img": "day-bahia-otro-carnaval-4.jpg"},
            {"n": 8, "label": "Día 8 (mié) · Espelho", "title": "Caraíva, Espelho y Pataxó", "body": "Barco privado a Caraíva. Visita a Aldeia Pataxó Reserva da Jaqueira. Tarde en Praia do Espelho, piscinas naturales. Cena de despedida en el Quadrado.", "meals": "Pensión completa", "lodging": "UXUA Casa", "img": "day-bahia-otro-carnaval-4.jpg"},
            {"n": 9, "label": "Día 9 (jue) · Despedida", "title": "Vuelta", "body": "Mañana libre. Traslado Porto Seguro aeropuerto. Vuelos.", "meals": "Desayuno", "lodging": "—", "img": "day-bahia-otro-carnaval-1.jpg"},
        ],
        "lodges": [
            {"name": "Villa Bahia Hotel", "where": "Pelourinho Salvador (palacete colonial XVII)", "img": "lodge-bahia-otro-carnaval-1.jpg"},
            {"name": "UXUA Casa Hotel & Spa", "where": "Trancoso (11 casitas restauradas en Quadrado)", "img": "lodge-bahia-otro-carnaval-2.jpg"},
            {"name": "Casa de Samba en Cachoeira", "where": "Recôncavo (almuerzo destino, no overnight)", "img": "lodge-bahia-otro-carnaval-3.jpg"},
            {"name": "Etnia Pousada", "where": "Trancoso (alternativa a UXUA si bookean grupos grandes)", "img": "lodge-bahia-otro-carnaval-4.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $2,400 USD", "title": "Chapada Diamantina", "body": "El parque nacional de cuevas, cascadas y mesas — la Patagonia bahiana. Pre-Carnaval o post-Trancoso.", "img": "dest-southamerica.jpg"},
            {"meta": "+3 días · desde $2,800 USD", "title": "Rio de Janeiro contraste", "body": "Para ver Río fuera de Carnaval — Copacabana en otoño, Christ Redeemer, Santa Teresa y Pão de Açúcar.", "img": "dest-southamerica.jpg"},
            {"meta": "+5 días · desde $4,800 USD", "title": "Pantanal · jaguares", "body": "Combo brasileño completo: cultura afro + el delta más grande del mundo y el felino top de América.", "img": "dest-southamerica.jpg"},
        ],
        "dates": [
            {"date": "3 feb 2027", "status": "Pocas plazas", "status_class": "few", "price": "$10,200"},
            {"date": "10 feb 2027", "status": "Abierta", "status_class": "open", "price": "$9,500"},
            {"date": "17 feb 2027", "status": "Abierta", "status_class": "open", "price": "$9,500"},
        ],
        "similar": [
            {"href": "marruecos-imperial.html", "img": "hero-marruecos-imperial.jpg", "pill": "10 días", "title": "Marruecos"},
            {"href": "namibia-dunas.html", "img": "hero-namibia-dunas.jpg", "pill": "11 días", "title": "Namibia"},
            {"href": "uzbekistan-ruta-seda.html", "img": "hero-uzbekistan-ruta-seda.jpg", "pill": "11 días", "title": "Uzbekistán"},
            {"href": "piamonte-tartufo.html", "img": "hero-piamonte-tartufo.jpg", "pill": "8 días", "title": "Piamonte"},
        ],
        "includes": [
            "Vuelo doméstico Salvador-Porto Seguro",
            "Traslados terrestres aeropuertos y Recôncavo",
            "Pensión completa con cocina baiana",
            "Antropólogo de UFBA en piso 5 días",
            "Camarote privado Carnaval Días 4 y 5 (catering ilimitado, bar abierto)",
            "Sesión privada Mestre Capoeira Angola",
            "Visita educativa terreiro Casa Branca con intermediación",
            "Familia samba de roda Recôncavo",
            "Visita Aldeia Pataxó Reserva da Jaqueira (donación incluida)",
            "Barco privado Caraíva + Praia do Espelho",
            "Tapones de oído para Carnaval",
            "Fotógrafo profesional + libro custom",
            "Kit B&amp;A pre-viaje",
        ],
        "excludes": [
            "Vuelos internacionales BA-Salvador",
            "Visado (no requerido para argentinos)",
            "Compras de artesanía",
            "Bebidas premium fuera del camarote",
        ],
    },
    {
        "slug": "japon-mono-no-aware",
        "title": "Japón",
        "headline": "Japón",
        "subtitle": "Tokio, Kioto y la Isla de Naoshima · Edición sakura marzo 2027",
        "eyebrow": "Pequeña expedición · Asia Oriental",
        "meta_desc": "Doce días siguiendo el frente del sakura de Tokio a Kanazawa a Kioto. Ceremonia del té con maestro Urasenke, kaiseki en Kikunoi 3 estrellas, machiya en Kioto, y dos noches en Benesse House Naoshima con Tadao Ando.",
        "hero": "hero-japon-mono-no-aware.jpg", "hero_alt": "Camino del Filósofo en plena floración con sakura sobre canal",
        "portrait": "wildlife-japon-mono-no-aware.jpg",
        "duration": "12 días", "nights": "11 noches", "max_guests": 8,
        "window": "Marzo–abril (sakura)", "price_from": "$11,000 USD",
        "intro_h2": "El sakura, los maestros y la isla de arte contemporáneo — Japón fuera del circuito Tokio-Kioto.",
        "intro_p1": "Hay una palabra japonesa que no se traduce: mono no aware — la conciencia de la transitoriedad, la belleza precisamente porque algo se va a terminar. El cerezo en flor es su símbolo perfecto: cinco días de plenitud, después la lluvia rosa, después la nada. Doce días en la filosofía nipona de la impermanencia, siguiendo el frente del sakura de sur a norte mientras el archipiélago lo abre.",
        "intro_p2": "Cuatro Japón distintos: Tokio (la megaciudad con sus maestros de té y sushi shokunin), Hakone (una noche de ryokan con onsen y kaiseki de doce pasos), Kanazawa (la pequeña Kioto del Mar de Japón con su distrito geisha intacto desde Edo), Kioto (cuatro noches en machiya privada, con Ryōan-ji, Kikunoi 3 estrellas y sesión de zazen), y Naoshima (dos noches en Benesse House — el museo donde se duerme, las Waterlilies de Monet en sala de Tadao Ando, el Teshima Art Museum).",
        "highlights": [
            {"t": "Ceremonia del té con maestro Urasenke", "b": "Sesión privada de 90 minutos en chashitsu tradicional, no performance — el ritual real de una de las dos escuelas de té más importantes del país."},
            {"t": "Kaiseki en Kikunoi (3 estrellas Michelin)", "b": "Mesa privada con el chef Yoshihiro Murata explicando cada plato del kaiseki más respetado de Kioto."},
            {"t": "Dos noches en Benesse House Naoshima", "b": "El único hotel del mundo donde dormís dentro de un museo. Tadao Ando, las Waterlilies de Monet, y el Teshima Art Museum de Ryue Nishizawa."}
        ],
        "stops": ["Tokio", "Asakusa", "Hakone", "Kanazawa", "Kioto", "Arashiyama", "Naoshima", "Teshima"],
        "itin_intro": "Doce días siguiendo el frente del sakura del sur al norte. Tokio para la primera ola, Hakone una noche con onsen, Kanazawa para los cerezos del norte y el distrito geisha, cuatro noches en Kioto en machiya privada con buyout completo del grupo, y cierre con dos noches en Naoshima donde dormís dentro del museo.",
        "days": [
            {"n": 1, "label": "Día 1 · Tokio", "title": "Llegada Tokio", "body": "Recepción en Lexus. Caminata por Imperial Palace East Gardens, primeros sakuras. Cena kaiseki en Kitcho Arashiyama Tokyo.", "meals": "Cena", "lodging": "Hoshinoya Tokyo", "img": "day-japon-mono-no-aware-1.jpg"},
            {"n": 2, "label": "Día 2 · Asakusa", "title": "Tokio · tradición y velocidad", "body": "Mañana en Asakusa (Senso-ji + río Sumida). Tarde en Roppongi: 21_21 Design Sight (Tadao Ando) + Mori Art Museum.", "meals": "Pensión completa", "lodging": "Hoshinoya Tokyo", "img": "day-japon-mono-no-aware-1.jpg"},
            {"n": 3, "label": "Día 3 · Maestros", "title": "Tokio · los maestros", "body": "Ceremonia del té privada con maestro Urasenke en chashitsu de Aoyama. Tarde: cena privada de sushi shokunin (1 Michelin, 8 cubiertos). Cierre en TeamLab Planets Toyosu.", "meals": "Pensión completa", "lodging": "Hoshinoya Tokyo", "img": "day-japon-mono-no-aware-2.jpg"},
            {"n": 4, "label": "Día 4 · Hakone", "title": "Tokio → Hakone", "body": "Mercado Toyosu opcional con experto. Shinkansen a Odawara. Onsen privado y público en Gora Kadan. Kaiseki de doce pasos en habitación. Vista Fuji al ocaso.", "meals": "Pensión completa", "lodging": "Gora Kadan", "img": "day-japon-mono-no-aware-3.jpg"},
            {"n": 5, "label": "Día 5 · Kanazawa", "title": "Hakone → Kanazawa", "body": "Hakone Open Air Museum (sala Picasso). Shinkansen Hakone-Tokio-Kanazawa en Green Car. Llegada al ocaso.", "meals": "Pensión completa", "lodging": "Beniya Mukayu Kanazawa", "img": "day-japon-mono-no-aware-3.jpg"},
            {"n": 6, "label": "Día 6 · Geisha", "title": "Kanazawa · jardín, geisha, oro", "body": "Kenrokuen Garden con especialista. Distrito Higashi Chaya. Taller de pan de oro. Encuentro privado con maiko en chaya histórica. Cena en Tsubajin.", "meals": "Pensión completa", "lodging": "Beniya Mukayu", "img": "day-japon-mono-no-aware-2.jpg"},
            {"n": 7, "label": "Día 7 · Kioto", "title": "Kanazawa → Kioto", "body": "21st Century Museum (SANAA). Shinkansen a Kioto. Check-in machiya buyout. Cena en kappo de Pontocho.", "meals": "Pensión completa", "lodging": "Machiya privada Higashiyama", "img": "day-japon-mono-no-aware-1.jpg"},
            {"n": 8, "label": "Día 8 · Templos", "title": "Kioto · templos y piedra", "body": "Hanami al amanecer en Camino del Filósofo. Ginkaku-ji. Shojin ryori en Tenryū-ji Arashiyama. Bambú. Cena en Kikunoi 3* con chef Murata.", "meals": "Pensión completa", "lodging": "Machiya", "img": "day-japon-mono-no-aware-1.jpg"},
            {"n": 9, "label": "Día 9 · Zen", "title": "Kioto · Zen y maestros", "body": "Zazen en Shunkō-in. Ryōan-ji jardín de piedra. Maestro ceramista de Kiyomizu + maestro kintsugi. Fushimi Inari al ocaso.", "meals": "Pensión completa", "lodging": "Machiya", "img": "day-japon-mono-no-aware-2.jpg"},
            {"n": 10, "label": "Día 10 · Naoshima", "title": "Kioto → Naoshima", "body": "Shinkansen a Okayama, ferry a Naoshima. Check-in Benesse House Park. Tarde en Chichu Art Museum (las Waterlilies de Monet en sala Ando).", "meals": "Pensión completa", "lodging": "Benesse House Park", "img": "day-japon-mono-no-aware-4.jpg"},
            {"n": 11, "label": "Día 11 · Teshima", "title": "Naoshima → Teshima → Naoshima", "body": "Lee Ufan Museum (Ando). Art House Project (Honmura). Ferry a Teshima, Teshima Art Museum de Ryue Nishizawa. Cena de despedida.", "meals": "Pensión completa", "lodging": "Benesse House Park", "img": "day-japon-mono-no-aware-4.jpg"},
            {"n": 12, "label": "Día 12 · Vuelta", "title": "Naoshima → Osaka → partida", "body": "Ferry, tren a Osaka KIX. Vuelos internacionales.", "meals": "Desayuno", "lodging": "—", "img": "day-japon-mono-no-aware-1.jpg"},
        ],
        "lodges": [
            {"name": "Hoshinoya Tokyo", "where": "Otemachi (ryokan contemporáneo con baño termal en azotea)", "img": "lodge-japon-mono-no-aware-1.jpg"},
            {"name": "Gora Kadan", "where": "Hakone (antigua villa imperial Meiji, 8 habitaciones)", "img": "lodge-japon-mono-no-aware-2.jpg"},
            {"name": "Beniya Mukayu", "where": "Kanazawa (ryokan boutique, baño termal propio)", "img": "lodge-japon-mono-no-aware-3.jpg"},
            {"name": "Benesse House Park", "where": "Naoshima (Tadao Ando — hotel-museo)", "img": "lodge-japon-mono-no-aware-4.jpg"},
        ],
        "extensions": [
            {"meta": "+5 días · desde $4,800 USD", "title": "Hokkaido invernal", "body": "Cambio de estación si querés combinar con febrero — Niseko snow, Sapporo, Furano.", "img": "dest-japan.jpg"},
            {"meta": "+6 días · desde $14,500 USD", "title": "Kyushu y Seven Stars", "body": "El tren de lujo más exclusivo de Asia, vagón de cedro y obras de arte, por Kagoshima y Yakushima.", "img": "j-japan.jpg"},
            {"meta": "+2 días · desde $1,400 USD", "title": "Tokio pre-trip extra", "body": "Dos días más en Tokio para los foodies — Tsukiji exterior, Shibuya, Harajuku con experto.", "img": "dest-japan.jpg"},
        ],
        "dates": [
            {"date": "22 mar 2027", "status": "Abierta", "status_class": "open", "price": "$11,000"},
            {"date": "27 mar 2027", "status": "Pocas plazas", "status_class": "few", "price": "$11,000"},
            {"date": "1 abr 2027", "status": "Abierta", "status_class": "open", "price": "$11,000"},
            {"date": "5 abr 2027", "status": "Lista de espera", "status_class": "wait", "price": "$11,000"},
            {"date": "10 abr 2027", "status": "Abierta", "status_class": "open", "price": "$10,500"},
        ],
        "similar": [
            {"href": "butan-nepal-himalaya.html", "img": "hero-butan-nepal-himalaya.jpg", "pill": "13 días", "title": "Bután y Nepal"},
            {"href": "piamonte-tartufo.html", "img": "hero-piamonte-tartufo.jpg", "pill": "8 días", "title": "Piamonte"},
            {"href": "uzbekistan-ruta-seda.html", "img": "hero-uzbekistan-ruta-seda.jpg", "pill": "11 días", "title": "Uzbekistán"},
            {"href": "croacia-islas-dalmatas.html", "img": "hero-croacia-islas-dalmatas.jpg", "pill": "9 días", "title": "Croacia"},
        ],
        "includes": [
            "Shinkansen Green Car (todos los traslados internos)",
            "Ferries Naoshima ↔ Teshima",
            "Sedán Lexus para recepciones aeropuerto + traslados",
            "Pensión completa con kaiseki en Hakone, Kanazawa y Kioto",
            "Ceremonia del té privada con maestro Urasenke",
            "Cena privada de sushi shokunin (1 Michelin)",
            "Cena en Kikunoi 3 estrellas Michelin (Kioto)",
            "Maiko privada en chaya Kanazawa",
            "Sesión de zazen con monje",
            "Talleres con maestro ceramista Kiyomizu + maestro kintsugi",
            "Especialista en jardines japoneses (Kenrokuen + Kioto)",
            "Acceso Chichu, Lee Ufan, Art House Project, Teshima Art Museum",
            "Guía cultural bilingüe español-japonés durante 11 días",
            "Yukata propias como regalo",
            "Fotógrafo profesional + libro custom",
            "Kit B&amp;A pre-viaje",
        ],
        "excludes": [
            "Vuelos internacionales BA-Tokio",
            "Visado (no requerido para argentinos hasta 90 días)",
            "Bebidas premium (sake de colección, whiskey)",
            "Compras personales (cerámica, kimonos, textiles)",
        ],
    },
    {
        "slug": "butan-nepal-himalaya",
        "title": "Bután y Nepal",
        "headline": "Bután y Nepal",
        "subtitle": "Corazón del Himalaya · Vajrayana, el festival Tsechu y el monasterio en el acantilado · Abril 2027",
        "eyebrow": "Pequeña expedición · Himalaya",
        "meta_desc": "Trece días en el último país Vajrayana del mundo. Festival Paro Tsechu con thongdrel al amanecer, subida al Tiger's Nest, monasterios sin filtro y Kathmandu como puerta del subcontinente.",
        "hero": "hero-butan-nepal-himalaya.jpg", "hero_alt": "Tiger's Nest contra acantilado y cielo himalayo",
        "portrait": "wildlife-butan-nepal-himalaya.jpg",
        "duration": "13 días", "nights": "12 noches", "max_guests": 8,
        "window": "Abril (Paro Tsechu)", "price_from": "$11,500 USD",
        "intro_h2": "El único país del mundo donde el Vajrayana sigue siendo religión de estado y donde un festival monástico medieval es el evento más importante del año.",
        "intro_p1": "Bután tiene dos singularidades constitucionales. Mide su éxito por la Felicidad Nacional Bruta (no por PIB), y es el último país donde el Budismo Vajrayana —la rama tántrica, la más esotérica del budismo— sigue siendo religión de estado y práctica viva ininterrumpida desde el siglo VIII, cuando Padmasambhava cruzó los Himalayas. Las visualizaciones tántricas, los mandalas, las ceremonias cham no son turismo cultural — son la práctica espiritual cotidiana.",
        "intro_p2": "El viaje gira alrededor del Paro Tsechu, el festival de máscaras que recrea episodios de la vida de Padmasambhava. El día final, antes del amanecer, se despliega el thongdrel — un thangka monumental de 30 metros que solo se ve este día. Verlo libera del karma negativo según la tradición. Trece días con Kathmandu como puerta y aclimatación, Bután en cuatro valles (Thimphu, Punakha, Gangtey, Paro), monasterios sin filtro, y el ascenso final al Tiger's Nest.",
        "highlights": [
            {"t": "Paro Tsechu y el thongdrel al amanecer", "b": "Dos días en el festival monástico más importante de Bután, con acceso a zona privilegiada y el desenrollo del thangka de 30m antes del amanecer."},
            {"t": "Subida al Tiger's Nest", "b": "El monasterio del siglo VIII que cuelga a 3.120 m sobre un acantilado, donde Padmasambhava meditó tres años, tres meses, tres semanas y tres días. Caballos disponibles."},
            {"t": "Encuentro con lopen en Cheri Monastery", "b": "Conversación filosófica privada con un maestro Vajrayana en el monasterio fundado por Shabdrung en el siglo XVII."}
        ],
        "stops": ["Kathmandu", "Boudhanath", "Bhaktapur", "Thimphu", "Punakha", "Gangtey", "Paro", "Tiger's Nest"],
        "itin_intro": "Trece días que comienzan en el valle Newar de Kathmandu para aclimatación y aclimatación cultural, cruzan en avión Druk Air a Bután, recorren los cuatro valles principales (Thimphu, Punakha, Gangtey, Paro) y culminan con el Tsechu en Paro y la subida al Tiger's Nest.",
        "days": [
            {"n": 1, "label": "Día 1 · Kathmandu", "title": "Llegada a Kathmandu", "body": "Recepción con guirnalda y khata blanco. Cena newari en Dwarika's. Presentación del guía cultural bilingüe español-inglés.", "meals": "Cena", "lodging": "Dwarika's Hotel Kathmandu", "img": "day-butan-nepal-himalaya-1.jpg"},
            {"n": 2, "label": "Día 2 · Valle Newar", "title": "Boudhanath y Bhaktapur", "body": "Boudhanath stupa con kora junto a peregrinos tibetanos. Monasterio tibetano. Pashupatinath (ghats de cremación). Bhaktapur — plaza Durbar, templo Nyatapola.", "meals": "Pensión completa", "lodging": "Dwarika's", "img": "day-butan-nepal-himalaya-1.jpg"},
            {"n": 3, "label": "Día 3 · Druk Air", "title": "Kathmandu → Paro → Thimphu", "body": "Vuelo Druk Air (aterrizaje espectacular entre cordilleras). Traslado a Thimphu. Memorial Chorten + Tashichhodzong.", "meals": "Pensión completa", "lodging": "Le Méridien Thimphu", "img": "day-butan-nepal-himalaya-2.jpg"},
            {"n": 4, "label": "Día 4 · Vajrayana", "title": "Thimphu · Vajrayana cotidiana", "body": "Cheri Monastery con encuentro privado con lopen. Almuerzo en farmhouse butanesa. Zorig Chusum (artesanías), maestro de thangka. Baño de piedras calientes dotsho.", "meals": "Pensión completa", "lodging": "Le Méridien Thimphu", "img": "day-butan-nepal-himalaya-2.jpg"},
            {"n": 5, "label": "Día 5 · Punakha", "title": "Thimphu → Punakha", "body": "Cruce del paso Dochu La (3.150m) con 108 chortens. Punakha Dzong en confluencia Pho Chhu + Mo Chhu.", "meals": "Pensión completa", "lodging": "Zhiwa Ling Punakha", "img": "day-butan-nepal-himalaya-2.jpg"},
            {"n": 6, "label": "Día 6 · Fertilidad", "title": "Punakha · fertilidad y tejido", "body": "Caminata por arrozales a Chimi Lhakhang (templo de fertilidad de Drukpa Kunley). Visita a familia tejedora kushuthara. Partida privada de tiro con arco.", "meals": "Pensión completa", "lodging": "Zhiwa Ling Punakha", "img": "day-butan-nepal-himalaya-2.jpg"},
            {"n": 7, "label": "Día 7 · Gangtey", "title": "Punakha → Gangtey", "body": "4-5 hrs a través del paso Pele La (3.420m) hasta el valle glacial Phobjikha. Visita al Gangtey Monastery (linaje Nyingma). Sendero Gangtey Nature Trail.", "meals": "Pensión completa", "lodging": "Gangtey Lodge", "img": "day-butan-nepal-himalaya-2.jpg"},
            {"n": 8, "label": "Día 8 · Paro", "title": "Gangtey → Paro", "body": "6-7 hrs a Paro via Wangdue. Paisajes del centro de Bután. Llegada al ocaso.", "meals": "Pensión completa", "lodging": "Zhiwa Ling Heritage Paro", "img": "day-butan-nepal-himalaya-3.jpg"},
            {"n": 9, "label": "Día 9 · Tsechu I", "title": "Paro Tsechu · Día 1", "body": "Vestidos con kira y gho (requerido por ley para entrar al dzong). Acceso a zona privilegiada del festival. Danzas cham: Baile de los Esqueletos, Cuerno Negro, Animales. Picnic gourmet.", "meals": "Pensión completa", "lodging": "Zhiwa Ling Heritage", "img": "day-butan-nepal-himalaya-3.jpg"},
            {"n": 10, "label": "Día 10 · Tsechu II", "title": "Paro Tsechu · thongdrel al amanecer", "body": "4:00 AM al dzong. 5:00 AM: el thongdrel de 30m se despliega antes del amanecer. Mañana libre. Museo Nacional de Bután en el Ta Dzong.", "meals": "Pensión completa", "lodging": "Zhiwa Ling Heritage", "img": "day-butan-nepal-himalaya-4.jpg"},
            {"n": 11, "label": "Día 11 · Tiger's Nest", "title": "Taktsang Palphug", "body": "Subida de 700m / 4km / 3hrs al monasterio del siglo VIII colgando del acantilado. Caballos hasta mitad para quien quiera. Cena de despedida con lectura del Bardo Thödol.", "meals": "Pensión completa", "lodging": "Zhiwa Ling Heritage", "img": "day-butan-nepal-himalaya-3.jpg"},
            {"n": 12, "label": "Día 12 · Vuelta a Nepal", "title": "Paro → Kathmandu", "body": "Vuelo Druk Air. Tarde libre o Patan Durbar Square.", "meals": "Pensión completa", "lodging": "Dwarika's", "img": "day-butan-nepal-himalaya-2.jpg"},
            {"n": 13, "label": "Día 13 · Despedida", "title": "Vuelta", "body": "Traslado Tribhuvan según horarios.", "meals": "Desayuno", "lodging": "—", "img": "day-butan-nepal-himalaya-1.jpg"},
        ],
        "lodges": [
            {"name": "Dwarika's Hotel", "where": "Kathmandu (palacio newari del siglo XV)", "img": "lodge-butan-nepal-himalaya-1.jpg"},
            {"name": "Le Méridien Thimphu", "where": "Thimphu (5 estrellas contemporáneo)", "img": "lodge-butan-nepal-himalaya-4.jpg"},
            {"name": "Zhiwa Ling Punakha", "where": "Punakha (lodge tradicional butanés)", "img": "lodge-butan-nepal-himalaya-2.jpg"},
            {"name": "Gangtey Lodge", "where": "Phobjikha (boutique 12 suites, vista al valle)", "img": "lodge-butan-nepal-himalaya-3.jpg"},
        ],
        "extensions": [
            {"meta": "+6 días · desde $4,200 USD", "title": "Everest base trek (Nepal)", "body": "Vuelo a Lukla y trek a Everest Base Camp (5.364m). Para los más aventureros, con guía sherpa.", "img": "dest-arctic.jpg"},
            {"meta": "+3 días · desde $2,800 USD", "title": "Bumthang Valley", "body": "Extender en Bután: el valle central, cuna espiritual del país, con Jakar Tsechu si las fechas coinciden.", "img": "dest-asia.jpg"},
            {"meta": "+4 días · desde $2,400 USD", "title": "Tigres en Bardia Nepal", "body": "Bardia National Park, los tigres de Bengala fuera del circuito Chitwan, en lodge sustentable.", "img": "dest-india.jpg"},
        ],
        "dates": [
            {"date": "8 abr 2027", "status": "Abierta", "status_class": "open", "price": "$11,500"},
            {"date": "11 abr 2027", "status": "Pocas plazas", "status_class": "few", "price": "$11,500"},
            {"date": "15 abr 2027", "status": "Lista de espera", "status_class": "wait", "price": "$11,500"},
            {"date": "22 abr 2027", "status": "Abierta", "status_class": "open", "price": "$10,900"},
            {"date": "29 abr 2027", "status": "Abierta", "status_class": "open", "price": "$10,900"},
        ],
        "similar": [
            {"href": "japon-mono-no-aware.html", "img": "hero-japon-mono-no-aware.jpg", "pill": "12 días", "title": "Japón · sakura"},
            {"href": "uzbekistan-ruta-seda.html", "img": "hero-uzbekistan-ruta-seda.jpg", "pill": "11 días", "title": "Uzbekistán"},
            {"href": "marruecos-imperial.html", "img": "hero-marruecos-imperial.jpg", "pill": "10 días", "title": "Marruecos"},
            {"href": "laponia-auroras.html", "img": "hero-laponia-auroras.jpg", "pill": "10 días", "title": "Laponia"},
        ],
        "includes": [
            "Vuelo Druk Air Kathmandu-Paro round trip",
            "Sustainable Development Fee de Bután ($100/día × 9 días)",
            "Visado de Bután",
            "Pensión completa en todos los lodges",
            "Guía cultural bilingüe español-inglés con doctorado en estudios himalayos",
            "Encuentro privado con lopen en Cheri Monastery",
            "Maestro de thangka workshop visit",
            "Familia tejedora kushuthara",
            "Ritual baño de piedras calientes (dotsho)",
            "Partida privada de tiro con arco",
            "Acceso a zona privilegiada del Paro Tsechu (2 días)",
            "Caballos para Tiger's Nest disponibles",
            "Alquiler de kira y gho para días del Tsechu",
            "Khata blancos de bienvenida y despedida",
            "Kit B&amp;A pre-viaje",
            "Fotógrafo profesional + libro custom",
        ],
        "excludes": [
            "Vuelos internacionales BA-Kathmandu (vía Delhi o Doha)",
            "Visado Nepal (USD 30 al arribo)",
            "Bebidas alcohólicas",
            "Compras personales (thangkas, joyería, textiles)",
            "Trekking extension a Everest",
        ],
    },
    {
        "slug": "marruecos-imperial",
        "title": "Marruecos",
        "headline": "Marruecos",
        "subtitle": "Las Cuatro Capitales y el Atlas · Edición mayo 2027",
        "eyebrow": "Pequeña expedición · Norte de África",
        "meta_desc": "Diez días por las cuatro ciudades imperiales y el Alto Atlas. Maestros de zellige, sufismo en Fez, gnawa en Marrakech, dos noches en Kasbah du Toubkal y noches en riads palaciales del siglo XIX.",
        "hero": "hero-marruecos-imperial.jpg", "hero_alt": "Patio de Bahia Palace con zellige y luz cenital",
        "portrait": "wildlife-marruecos-imperial.jpg",
        "duration": "10 días", "nights": "9 noches", "max_guests": 8,
        "window": "Mayo", "price_from": "$10,800 USD",
        "intro_h2": "Cuatro capitales imperiales más el corazón bereber del Atlas, sin nada del cliché orientalista.",
        "intro_p1": "Marruecos tiene una particularidad estructural: durante mil años fue gobernado por dinastías que mudaron la capital con cada cambio de poder. Fez (los meriníes), Mequínez (Moulay Ismail), Marrakech (los almorávides y saadíes), Rabat (los meriníes y los alauitas actuales). Las cuatro siguen siendo ciudades imperiales — todas amuralladas, todas con su medina, mellah y kasbah, todas con su sistema completo de souks especializados por gremio.",
        "intro_p2": "Lo que une a las cuatro: los oficios. El zellige (mosaico geométrico islámico) que cubre Bahia Palace sale de los talleres de Fez. El cuero del Chouara — la curtiembre del siglo XI todavía operativa. El damasquinado, el caftán, la caligrafía cúfica, los brocados de seda y oro. Más allá: el Alto Atlas, donde los Imazighen (bereberes, hombres libres) preceden al Islam por nueve mil años y donde el tamazight tiene rango constitucional. Mayo es la ventana exacta: roses florece en Kelaa M'Gouna, el calor del Sahara aún no es brutal, los almendros del Atlas terminan de florecer.",
        "highlights": [
            {"t": "Sesión privada Hadra El Fassia (sufí Fez)", "b": "Cuarteto de música devocional fasi con percusión y voces en qasidas mevleví — el sufismo de Marruecos en su forma más profunda."},
            {"t": "Dos noches en Kasbah du Toubkal", "b": "El Berber Hospitality Centre restaurado con la familia del moqaddem local. 14 habitaciones, vista al Toubkal, hospitalidad bereber real."},
            {"t": "Sesión privada Maâlem Gnawa Marrakech", "b": "Música de trance descendente de los esclavos sub-saharianos. Maestro con guembri (laud de tres cuerdas) y qarqaba."}
        ],
        "stops": ["Casablanca", "Rabat", "Volubilis", "Mequínez", "Fez", "Imlil", "Aremd", "Marrakech"],
        "itin_intro": "Diez días que comienzan en Rabat (capital actual), atraviesan Volubilis romano y Mequínez de Moulay Ismail, anclan tres noches en Fez (la capital de los oficios), suben dos noches al Alto Atlas para la cultura bereber, y cierran tres noches en Marrakech con el Gnawa.",
        "days": [
            {"n": 1, "label": "Día 1 · Rabat", "title": "Casablanca → Rabat", "body": "Aterrizaje y traslado terrestre a Rabat (1h 15). Kasbah de los Udayas, Torre Hassan, Mausoleo de Mohammed V. Cena en Dar Rbatia.", "meals": "Cena", "lodging": "Villa Diyafa Rabat", "img": "day-marruecos-imperial-1.jpg"},
            {"n": 2, "label": "Día 2 · Volubilis", "title": "Rabat → Volubilis → Mequínez → Fez", "body": "Ruinas romanas Volubilis con arqueólogo. Mequínez: Bab Mansour, establos reales, granero monumental. Llegada Fez al ocaso.", "meals": "Pensión completa", "lodging": "Riad Fès / Palais Faraj", "img": "day-marruecos-imperial-1.jpg"},
            {"n": 3, "label": "Día 3 · Medina sagrada", "title": "Fez · medina sagrada", "body": "Madrasa Bou Inania, Karaouine Mosque/University, Funduq Nejjarine. Chouara Tannery con guida específico de gremios del cuero.", "meals": "Pensión completa", "lodging": "Riad Fès", "img": "day-marruecos-imperial-2.jpg"},
            {"n": 4, "label": "Día 4 · Los oficios", "title": "Fez · los oficios", "body": "Maestro de zellige (cada estrella requiere 24 piezas talladas a mano). Calígrafo, damasquinador, brocados. Hammam ritual privado. Sesión privada Hadra El Fassia sufí al ocaso.", "meals": "Pensión completa", "lodging": "Riad Fès", "img": "day-marruecos-imperial-2.jpg"},
            {"n": 5, "label": "Día 5 · Atlas", "title": "Fez → Middle Atlas → Imlil", "body": "Cruce Atlas Medio vía Ifrane (la Suiza marroquí) y cedros del Atlas. Llegada Imlil (1.740m) por la tarde. Cena familiar bereber.", "meals": "Pensión completa", "lodging": "Kasbah du Toubkal", "img": "day-marruecos-imperial-3.jpg"},
            {"n": 6, "label": "Día 6 · Bereber", "title": "Imlil · vida bereber", "body": "Caminata desde Imlil a Aremd (45 min). Visita a familia bereber. Pan en horno comunal. Opcional Tizi n'Tamatert (2.270m).", "meals": "Pensión completa", "lodging": "Kasbah du Toubkal", "img": "day-marruecos-imperial-3.jpg"},
            {"n": 7, "label": "Día 7 · Marrakech", "title": "Imlil → Marrakech vía Tizi n'Tichka", "body": "Cruce paso Tizi n'Tichka (2.260m). Llegada Marrakech tarde. Jemaa el-Fnaa al ocaso.", "meals": "Pensión completa", "lodging": "La Sultana Marrakech", "img": "day-marruecos-imperial-4.jpg"},
            {"n": 8, "label": "Día 8 · Ciudad roja", "title": "Marrakech · la ciudad roja", "body": "Madrasa Ben Youssef, Saadian Tombs (escondidas 300 años hasta 1917), Bahia Palace. Souks especializados con guida de gremios. Maestro caftanero. Cena en Yacout.", "meals": "Pensión completa", "lodging": "La Sultana Marrakech", "img": "day-marruecos-imperial-4.jpg"},
            {"n": 9, "label": "Día 9 · Gnawa", "title": "Marrakech · Majorelle, jardines y Gnawa", "body": "Jardin Majorelle + Musée Yves Saint Laurent (Studio KO). Clase de cocina marroquí. Cena callejera Jemaa el-Fnaa con guía. Sesión privada Maâlem Gnawa noche.", "meals": "Pensión completa", "lodging": "La Sultana Marrakech", "img": "day-marruecos-imperial-4.jpg"},
            {"n": 10, "label": "Día 10 · Despedida", "title": "Vuelta", "body": "Mañana libre. Traslado Menara aeropuerto. Vuelos.", "meals": "Desayuno", "lodging": "—", "img": "day-marruecos-imperial-1.jpg"},
        ],
        "lodges": [
            {"name": "Villa Diyafa Boutique Hotel & Spa", "where": "Rabat (boutique 5 estrellas con jardines)", "img": "lodge-marruecos-imperial-4.jpg"},
            {"name": "Riad Fès / Palais Faraj", "where": "Fez (palacete colonial XIX en medina)", "img": "lodge-marruecos-imperial-1.jpg"},
            {"name": "Kasbah du Toubkal", "where": "Imlil (lodge bereber al pie del Toubkal)", "img": "lodge-marruecos-imperial-2.jpg"},
            {"name": "La Sultana Marrakech", "where": "Marrakech (riad-palacio en corazón de la medina)", "img": "lodge-marruecos-imperial-3.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $2,200 USD", "title": "Sahara · Erg Chebbi", "body": "Vuelo a Ouarzazate, drive a Merzouga, dos noches en desert camp con dunas, camellos y cielo estrellado del Sahara.", "img": "j-egypt.jpg"},
            {"meta": "+2 días · desde $1,400 USD", "title": "Essaouira · costa atlántica", "body": "El antiguo Mogador, ciudad amurallada portuguesa del XVI, gnawa festival si las fechas coinciden, playa atlántica.", "img": "dest-morocco.jpg"},
            {"meta": "+2 días · desde $1,300 USD", "title": "Chefchaouen · la ciudad azul", "body": "Pre-trip al norte, la ciudad pintada de azul del Rif, mucho más calma que las medinas imperiales.", "img": "dest-morocco.jpg"},
        ],
        "dates": [
            {"date": "8 may 2027", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "15 may 2027", "status": "Pocas plazas", "status_class": "few", "price": "$10,800"},
            {"date": "22 may 2027", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "29 may 2027", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "5 jun 2027", "status": "Lista de espera", "status_class": "wait", "price": "$11,200"},
        ],
        "similar": [
            {"href": "uzbekistan-ruta-seda.html", "img": "hero-uzbekistan-ruta-seda.jpg", "pill": "11 días", "title": "Uzbekistán"},
            {"href": "namibia-dunas.html", "img": "hero-namibia-dunas.jpg", "pill": "11 días", "title": "Namibia"},
            {"href": "piamonte-tartufo.html", "img": "hero-piamonte-tartufo.jpg", "pill": "8 días", "title": "Piamonte"},
            {"href": "bahia-otro-carnaval.html", "img": "hero-bahia-otro-carnaval.jpg", "pill": "9 días", "title": "Bahía"},
        ],
        "includes": [
            "Van privada Mercedes Sprinter con chofer durante 10 días",
            "Recepciones aeropuerto Mohammed V (llegada) + Menara (salida)",
            "Pensión completa con cocina marroquí",
            "Guía cultural bilingüe español-árabe (con tamazight para el Atlas) durante 9 días",
            "Acceso a maestros artesanos: zellige, calígrafo, damasquinador, brocado, caftán",
            "Sesión privada Hadra El Fassia (sufí Fez)",
            "Sesión privada Maâlem Gnawa (Marrakech)",
            "Hammam ritual privado en Fez",
            "Clase de cocina marroquí con chef de medina",
            "Familia bereber + caminata Aremd con guía local",
            "Guida específico de gremios para souks Fez y Marrakech",
            "Volubilis con arqueólogo",
            "Cenas en restaurantes notables (Yacout Marrakech, Dar Roumana Fez)",
            "Babuches + djellaba ligera como regalo",
            "Pieza de zellige original como recuerdo",
            "Kit B&amp;A pre-viaje",
            "Fotógrafo profesional + libro custom",
        ],
        "excludes": [
            "Vuelos internacionales BA-Casablanca (vía Madrid o Lisboa)",
            "Visado (no requerido para argentinos hasta 90 días)",
            "Bebidas alcohólicas (limitadas en Marruecos)",
            "Compras personales (alfombras, joyería, lámparas)",
        ],
    },
    {
        "slug": "croacia-islas-dalmatas",
        "title": "Croacia",
        "headline": "Croacia",
        "subtitle": "Las Islas Dálmatas en Catamarán · Edición junio 2027",
        "eyebrow": "Pequeña expedición · Mediterráneo",
        "meta_desc": "Nueve días en catamarán crewed Lagoon 55 desde Split hasta Dubrovnik. Cinco islas dálmatas, ostras de Mali Ston, klapa privado en iglesia de Korčula y la Cueva Azul de Biševo a la hora exacta.",
        "hero": "hero-croacia-islas-dalmatas.jpg", "hero_alt": "Catamarán anclado en cala azul turquesa",
        "portrait": "wildlife-croacia-islas-dalmatas.jpg",
        "duration": "9 días", "nights": "8 noches", "max_guests": 8,
        "window": "Junio", "price_from": "$10,500 USD",
        "intro_h2": "Cinco islas dálmatas en catamarán privado, en el mar más claro de Europa.",
        "intro_p1": "El Adriático es el mar más claro de Europa — la visibilidad submarina supera los 30 metros en las islas dálmatas centrales. La razón es estructural: mar pequeño y profundo, circulación lenta, sin grandes ríos sedimentarios, y una costa croata protegida 50 años por la Yugoslavia comunista que no permitió el desarrollo masivo. Las islas se preservaron casi por accidente histórico.",
        "intro_p2": "Recorremos cinco escenarios en catamarán Lagoon 55 crewed con capitán croata, primer oficial, chef y hostess: Split (Diocleciano), Brač (la piedra blanca que hizo la Casa Blanca), Hvar (lavanda y noches), Vis (cerrada hasta 1989 como base militar, la mejor preservada), Korčula (Marco Polo, las murallas, el klapa), Mljet (parque nacional con dos lagos salados), Ston (las ostras más antiguas del Mediterráneo) y Dubrovnik. Junio es el momento exacto: 22-24C de agua, antes del peak de julio-agosto.",
        "highlights": [
            {"t": "Klapa privado en iglesia de Korčula", "b": "Cuatro voces masculinas a capela en San Marcos al ocaso — Patrimonio Inmaterial UNESCO desde 2012, en acústica renacentista."},
            {"t": "Ostras Mali Ston con ostricultor de cuarta generación", "b": "Las ostras consideradas las mejores del Mediterráneo desde Brillat-Savarin (1825), abiertas en vivo frente al grupo con vino Pošip blanco."},
            {"t": "Cueva Azul de Biševo a la hora exacta", "b": "Entre 11AM y 12PM la luz refracta el azul cobalto en la cueva submarina. Excursión en lancha pequeña, una de las experiencias visuales más singulares del Mediterráneo."}
        ],
        "stops": ["Split", "Brač", "Hvar", "Vis", "Korčula", "Mljet", "Ston", "Dubrovnik"],
        "itin_intro": "Nueve días, cinco islas, una sola tripulación. El catamarán como hogar flotante, embarcando en Split tras la visita al Palacio de Diocleciano, navegando hacia el sur con paradas en las islas centrales y cerrando en Dubrovnik para la caminata sobre las murallas más fotografiadas del mundo.",
        "days": [
            {"n": 1, "label": "Día 1 · Split", "title": "Split — la Roma viva", "body": "Visita Palacio Diocleciano con arqueólogo (UNESCO, siglo III, único palacio imperial romano que sigue siendo centro de ciudad). Boarding del catamarán Lagoon 55 en ACI Marina Split. Vinos de bienvenida en cubierta. Navegación nocturna corta a Šolta.", "meals": "Cena", "lodging": "Catamarán Lagoon 55", "img": "day-croacia-islas-dalmatas-1.jpg"},
            {"n": 2, "label": "Día 2 · Brač", "title": "Brač — la piedra blanca", "body": "Anchor en Bol, playa Zlatni Rat. Snorkel y paddleboard. Excursión a Pučišća y su escuela de cantería (la piedra que hizo la Casa Blanca). Peka de cordero en konoba familiar.", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-2.jpg"},
            {"n": 3, "label": "Día 3 · Hvar", "title": "Hvar — lavanda y noche", "body": "Teatro de Hvar (1612, el más antiguo público de Europa), Fortaleza Španjola. Campos de lavanda y destilería Aromatica. Anchor opcional en Pakleni Islands.", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-2.jpg"},
            {"n": 4, "label": "Día 4 · Vis", "title": "Vis — la isla escondida", "body": "Komiža, pueblo pesquero. Excursión a la Cueva Azul de Biševo a hora exacta (11-12AM). Almuerzo en Konoba Roki's (peka). Tito's Cave + Stiniva Cove en barco.", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-3.jpg"},
            {"n": 5, "label": "Día 5 · Korčula", "title": "Korčula — Marco Polo y klapa", "body": "Caminata por la ciudad amurallada con historiador medieval. Casa Natal de Marco Polo. Moreška (danza de espadas del siglo XV). Cata de Grk en Lumbarda. Concierto privado de klapa en iglesia San Marcos al ocaso.", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-2.jpg"},
            {"n": 6, "label": "Día 6 · Mljet", "title": "Mljet — la isla nacional", "body": "Parque Nacional (72% protegido). Bicicleta o caminata alrededor de los dos lagos salados. Monasterio de Santa María (1151) en isla dentro del lago. Almuerzo en el monasterio.", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-2.jpg"},
            {"n": 7, "label": "Día 7 · Ston", "title": "Ston — ostras y muralla", "body": "Caminata sobre la muralla (5km, la más larga de Europa después de la Gran Muralla China). Salinas más antiguas de Europa en operación. Almuerzo de ostras Mali Ston abiertas en vivo. Tarde en Pelješac: cata vertical de Plavac Mali (madre genética del Zinfandel).", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-4.jpg"},
            {"n": 8, "label": "Día 8 · Dubrovnik", "title": "Dubrovnik — la perla del Adriático", "body": "Caminata sobre las Murallas de Dubrovnik (2km, 1.5h) con historiador. Stradun, Monasterio Franciscano + farmacia más antigua de Europa (1317), Palacio del Rector. Almuerzo en 360 Restaurant (1*) o Nautika. Tarde libre o nado en Lokrum. Cena de despedida en Pantarul con lectura de Matvejević.", "meals": "Pensión completa", "lodging": "Catamarán", "img": "day-croacia-islas-dalmatas-4.jpg"},
            {"n": 9, "label": "Día 9 · Vuelta", "title": "Disembark Dubrovnik", "body": "Disembarque a las 10:00. Traslado aeropuerto Čilipi 20 min. Vuelos internacionales.", "meals": "Desayuno", "lodging": "—", "img": "day-croacia-islas-dalmatas-1.jpg"},
        ],
        "lodges": [
            {"name": "Catamarán Lagoon 55 crewed", "where": "5 cabinas dobles, capitán + primer oficial + chef + hostess", "img": "lodge-croacia-islas-dalmatas-1.jpg"},
            {"name": "Konoba Roki's", "where": "Plisko Polje, Vis (almuerzo destino)", "img": "lodge-croacia-islas-dalmatas-2.jpg"},
            {"name": "LD Restaurant (Lešić Dimitri Palace)", "where": "Korčula (cena destino)", "img": "lodge-croacia-islas-dalmatas-3.jpg"},
            {"name": "360 Restaurant", "where": "Dubrovnik (1 estrella Michelin, almuerzo destino)", "img": "lodge-croacia-islas-dalmatas-4.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $1,800 USD", "title": "Plitvice Lakes + Zagreb", "body": "Pre-trip: dos noches en Plitvice (UNESCO, 16 lagos turquesas conectados por cascadas) + una en Zagreb.", "img": "dest-europe.jpg"},
            {"meta": "+3 días · desde $2,400 USD", "title": "Montenegro · Kotor + Sveti Stefan", "body": "Post-trip por tierra desde Dubrovnik. La Bahía de Kotor (UNESCO) y la antigua isla aristocrática de Sveti Stefan.", "img": "dest-europe.jpg"},
            {"meta": "+5 días · desde $4,200 USD", "title": "Islas griegas · Santorini + Mykonos", "body": "Cruce a Grecia para un segundo capítulo mediterráneo si la temporada de mar lo permite.", "img": "dest-europe.jpg"},
        ],
        "dates": [
            {"date": "5 jun 2027", "status": "Abierta", "status_class": "open", "price": "$10,500"},
            {"date": "12 jun 2027", "status": "Pocas plazas", "status_class": "few", "price": "$10,500"},
            {"date": "19 jun 2027", "status": "Abierta", "status_class": "open", "price": "$10,500"},
            {"date": "26 jun 2027", "status": "Lista de espera", "status_class": "wait", "price": "$10,500"},
            {"date": "3 jul 2027", "status": "Abierta", "status_class": "open", "price": "$10,900"},
        ],
        "similar": [
            {"href": "piamonte-tartufo.html", "img": "hero-piamonte-tartufo.jpg", "pill": "8 días", "title": "Piamonte"},
            {"href": "marruecos-imperial.html", "img": "hero-marruecos-imperial.jpg", "pill": "10 días", "title": "Marruecos"},
            {"href": "japon-mono-no-aware.html", "img": "hero-japon-mono-no-aware.jpg", "pill": "12 días", "title": "Japón · sakura"},
            {"href": "alaska-salvaje.html", "img": "hero-alaska-salvaje.jpg", "pill": "11 días", "title": "Alaska salvaje"},
        ],
        "includes": [
            "Catamarán Lagoon 55 crewed (capitán, primer oficial, chef, hostess) por 8 noches",
            "APA (Advance Provisioning Allowance) administrado: provisiones, combustible, port fees, drinks a bordo",
            "Pensión completa abordo + almuerzos destino seleccionados",
            "Historiador en piso bilingüe español-croata durante el viaje",
            "Arqueólogo romano Split (Día 1)",
            "Historiador medieval Dubrovnik (Día 8)",
            "Presentación privada Moreška en Korčula",
            "Concierto privado de klapa en iglesia San Marcos",
            "Almuerzo ostras Mali Ston con ostricultor de 4ta generación",
            "Cata vertical Plavac Mali en Pelješac",
            "Excursión Cueva Azul de Biševo en lancha pequeña",
            "Konoba Roki's (peka Vis)",
            "360 Restaurant Dubrovnik (1 Michelin almuerzo)",
            "Equipo snorkel, paddleboards, kayaks abordo",
            "Toalla turca con monograma B&amp;A (regalo de bienvenida)",
            "Fotógrafo profesional (3-4 días) + libro custom",
            "Kit B&amp;A pre-viaje",
        ],
        "excludes": [
            "Vuelos internacionales BA-Split (vía Madrid, Frankfurt o Roma) + salida Dubrovnik",
            "Visado (no requerido para argentinos en Schengen)",
            "Propinas a tripulación (suelen ser 10-15% del charter total, separadas)",
            "Compras personales",
        ],
    },
    {
        "slug": "alaska-salvaje",
        "title": "Alaska Salvaje",
        "headline": "Alaska Salvaje",
        "subtitle": "Lake Clark, Kenai Fjords y Denali · Edición julio 2027",
        "eyebrow": "Pequeña expedición · Wilderness norte",
        "meta_desc": "Once días entre osos pardos en Lake Clark, glaciares de Kenai Fjords y el flightseeing con aterrizaje sobre Denali. Naturalista en piso, kennel de Iditarod, Alaska Bear Camp y Kenai Fjords Wilderness Lodge.",
        "hero": "hero-alaska-salvaje.jpg", "hero_alt": "Oso pardo en pradera con macizo de fondo",
        "portrait": "wildlife-alaska-salvaje.jpg",
        "duration": "11 días", "nights": "10 noches", "max_guests": 8,
        "window": "Julio", "price_from": "$11,000 USD",
        "intro_h2": "El wilderness más grande de Norteamérica en el mes en que pulsa al ritmo del salmón.",
        "intro_p1": "Alaska es del tamaño de México con la población de Mendoza: 1,6 millones de km² para 730.000 habitantes. El 99,98% es wilderness administrado por el Servicio de Parques, BLM, o las tribus originarias. Es la única región del mundo desarrollado donde el wilderness sigue siendo realmente wilderness — no parque temático, sino territorio donde el ecosistema funciona como funcionó hace 10.000 años.",
        "intro_p2": "Julio es el mes específico. Veinte horas de luz, el salmón rojo corriendo río arriba, los osos pardos (hasta 700 kg) bajando de las montañas a concentrarse en las desembocaduras. Lake Clark National Park ofrece la mejor combinación de osos sin acostumbramiento turístico, opcional Brooks Falls. Después: Denali en flightseeing con aterrizaje en glaciar, y Kenai Fjords con orcas, ballenas jorobadas y catorce glaciares de marea. Once días con naturalista en piso, bush planes, kennel Iditarod y cultura Athabascan.",
        "highlights": [
            {"t": "Tres días de osos en Lake Clark", "b": "Alaska Bear Camp en Chinitna Bay, observación en pradera abierta con guías de 10+ años de experiencia, sin necesidad de torres ni distancias artificiales."},
            {"t": "Flightseeing Denali con aterrizaje en glaciar", "b": "Beechcraft King Air con skis aterriza sobre nieve compacta a 2.300m. Caminata sobre el glaciar con macizo Denali atrás."},
            {"t": "Kenai Fjords en barco privado", "b": "Catorce glaciares de marea desde un solo barco. Orcas residentes (tres pods), jorobadas alimentándose, leones marinos de Steller, frailecillos cornudos."}
        ],
        "stops": ["Anchorage", "Wasilla", "Lake Clark", "Talkeetna", "Denali", "Seward", "Aialik Glacier", "Heritage Center Anchorage"],
        "itin_intro": "Once días que comienzan en Anchorage, vuelan en hidroavión a Lake Clark para tres días de osos pardos en su rutina, suben a Talkeetna para el flightseeing sobre Denali con aterrizaje en glaciar, y cierran en Kenai Fjords con boat charter privado por los catorce glaciares de marea.",
        "days": [
            {"n": 1, "label": "Día 1 · Anchorage", "title": "Llegada", "body": "Vuelo BA vía LAX o Seattle (~18h). Cena en Crow's Nest con vista a Cook Inlet. Presentación del naturalista.", "meals": "Cena", "lodging": "Hotel Captain Cook Anchorage", "img": "day-alaska-salvaje-1.jpg"},
            {"n": 2, "label": "Día 2 · Iditarod", "title": "Anchorage → Lake Clark", "body": "Mañana visita a kennel de musher campeón (Seavey o equivalente) con carting ride. Hidroavión Lake Hood → Chinitna Bay (1h sobre volcán Iliamna).", "meals": "Pensión completa", "lodging": "Alaska Bear Camp Lake Clark", "img": "day-alaska-salvaje-1.jpg"},
            {"n": 3, "label": "Día 3 · Osos", "title": "Lake Clark · primera inmersión en osos", "body": "Salida 6 AM con guía de osos. Pradera abierta — osos pastando, mama con cachorros a 40m. Almuerzo de campo. Tarde en desembocadura del río con osos pescando.", "meals": "Pensión completa", "lodging": "Alaska Bear Camp", "img": "day-alaska-salvaje-2.jpg"},
            {"n": 4, "label": "Día 4 · Brooks Falls", "title": "Lake Clark · segundo día", "body": "Brooks Falls opcional: hidroavión a Katmai (~$450/pax adicional) para los osos saltando por salmón en cataratas. Alternativa: caminata extendida en Chinitna. Noche de salmón asado al fuego.", "meals": "Pensión completa", "lodging": "Alaska Bear Camp", "img": "day-alaska-salvaje-2.jpg"},
            {"n": 5, "label": "Día 5 · Talkeetna", "title": "Lake Clark → Talkeetna", "body": "Caminata final al amanecer. Hidroavión a Anchorage, vuelo doméstico a Talkeetna. Talkeetna Alaskan Lodge con vista a Denali.", "meals": "Pensión completa", "lodging": "Talkeetna Alaskan Lodge", "img": "day-alaska-salvaje-3.jpg"},
            {"n": 6, "label": "Día 6 · Denali", "title": "Flightseeing y aterrizaje en glaciar", "body": "K2 Aviation o Talkeetna Air Taxi — Beechcraft King Air o de Havilland Otter con skis. 1.5h sobre el macizo. Aterrizaje en glaciar a 2.300m, 30-45 min en la nieve.", "meals": "Pensión completa", "lodging": "Talkeetna Alaskan Lodge", "img": "day-alaska-salvaje-3.jpg"},
            {"n": 7, "label": "Día 7 · Seward", "title": "Talkeetna → Seward", "body": "Seward Highway (All-American Road). Paradas en Turnagain Arm (bore tides), Girdwood. Almuerzo en Sevenglaciers. Llegada Kenai Fjords Wilderness Lodge (boat-in).", "meals": "Pensión completa", "lodging": "Kenai Fjords Wilderness Lodge", "img": "day-alaska-salvaje-3.jpg"},
            {"n": 8, "label": "Día 8 · Glaciares", "title": "Kenai Fjords NP", "body": "Barco privado por Resurrection Bay. Aialik Glacier (calving constante), Bear Glacier, Northwestern Fjord. Almuerzo a bordo. Orcas, jorobadas, leones marinos, frailecillos.", "meals": "Pensión completa", "lodging": "Kenai Fjords Wilderness Lodge", "img": "day-alaska-salvaje-4.jpg"},
            {"n": 9, "label": "Día 9 · Vuelta", "title": "Seward → Anchorage", "body": "Mañana en lodge: kayak o caminata al glaciar cercano. Visita opcional Alaska SeaLife Center o Exit Glacier. Drive a Anchorage. Cena de despedida en Marx Bros. Café con lectura de John McPhee.", "meals": "Pensión completa", "lodging": "Hotel Captain Cook Anchorage", "img": "day-alaska-salvaje-4.jpg"},
            {"n": 10, "label": "Día 10 · Athabascan", "title": "Cultura Athabascan opcional", "body": "Mañana Alaska Native Heritage Center con guía Athabascan / Dena'ina. Conversación sobre soberanía tribal contemporánea. Traslado aeropuerto.", "meals": "Desayuno", "lodging": "—", "img": "day-alaska-salvaje-1.jpg"},
            {"n": 11, "label": "Día 11 · Partida", "title": "Vuelta", "body": "Vuelos internacionales desde Anchorage.", "meals": "Desayuno (lounge)", "lodging": "—", "img": "day-alaska-salvaje-1.jpg"},
        ],
        "lodges": [
            {"name": "Hotel Captain Cook", "where": "Anchorage (5 estrellas urbano histórico)", "img": "lodge-alaska-salvaje-4.jpg"},
            {"name": "Alaska Bear Camp", "where": "Chinitna Bay, Lake Clark NP (campamento tentado de lujo, fly-in)", "img": "lodge-alaska-salvaje-1.jpg"},
            {"name": "Talkeetna Alaskan Lodge", "where": "Talkeetna (lodge histórico con vista a Denali)", "img": "lodge-alaska-salvaje-2.jpg"},
            {"name": "Kenai Fjords Wilderness Lodge", "where": "Resurrection Bay (boat-in, dentro del parque nacional)", "img": "lodge-alaska-salvaje-3.jpg"},
        ],
        "extensions": [
            {"meta": "+1 día · $450 USD", "title": "Brooks Falls float plane", "body": "Excursión de día desde Lake Clark a Katmai. La imagen icónica de oso pardo saltando por salmón.", "img": "dest-northamerica.jpg"},
            {"meta": "+5 días · desde $4,800 USD", "title": "Glacier Bay y Inside Passage", "body": "Pre-trip por el sureste de Alaska: Juneau, Tracy Arm, Glacier Bay NP en barco pequeño.", "img": "dest-arctic.jpg"},
            {"meta": "+4 días · desde $3,800 USD", "title": "Kobuk Valley y Arctic Circle", "body": "Post-trip al verdadero Ártico: vuelo a Kotzebue, Kobuk Valley NP (las dunas árticas), Gates of the Arctic.", "img": "dest-arctic.jpg"},
        ],
        "dates": [
            {"date": "5 jul 2027", "status": "Abierta", "status_class": "open", "price": "$11,000"},
            {"date": "12 jul 2027", "status": "Pocas plazas", "status_class": "few", "price": "$11,000"},
            {"date": "19 jul 2027", "status": "Lista de espera", "status_class": "wait", "price": "$11,000"},
            {"date": "26 jul 2027", "status": "Abierta", "status_class": "open", "price": "$11,000"},
            {"date": "2 ago 2027", "status": "Abierta", "status_class": "open", "price": "$10,800"},
        ],
        "similar": [
            {"href": "namibia-dunas.html", "img": "hero-namibia-dunas.jpg", "pill": "11 días", "title": "Namibia"},
            {"href": "laponia-auroras.html", "img": "hero-laponia-auroras.jpg", "pill": "10 días", "title": "Laponia"},
            {"href": "butan-nepal-himalaya.html", "img": "hero-butan-nepal-himalaya.jpg", "pill": "13 días", "title": "Bután y Nepal"},
            {"href": "bahia-otro-carnaval.html", "img": "hero-bahia-otro-carnaval.jpg", "pill": "9 días", "title": "Bahía"},
        ],
        "includes": [
            "Hidroavión Anchorage ↔ Lake Clark (Lake Hood Seaplane Base)",
            "Vuelo doméstico Anchorage ↔ Talkeetna",
            "Denali flightseeing con aterrizaje en glaciar (K2 Aviation)",
            "Boat charter privado Kenai Fjords National Park",
            "Pensión completa en Alaska Bear Camp y Kenai Fjords Wilderness Lodge",
            "Naturalista en piso (biólogo de fauna alasqueña) durante 6 días",
            "Visita a kennel Iditarod con musher campeón (carting ride incluido)",
            "Guías de osos certificados en Lake Clark (10+ años experiencia)",
            "Cultura Athabascan: Alaska Native Heritage Center con guía",
            "Cenas notables (Crow's Nest, Marx Bros, Sevenglaciers)",
            "Van privada Seward Highway (Día 7)",
            "Equipo bear-resistant proporcionado por el campamento",
            "Botas Xtratuf (las Alaska sneakers) alquiladas para todo el grupo",
            "Recepciones aeropuerto Ted Stevens",
            "Kit B&amp;A pre-viaje",
            "Fotógrafo profesional + libro custom",
        ],
        "excludes": [
            "Vuelos internacionales BA-Anchorage (vía LAX o Seattle)",
            "Brooks Falls float plane opcional (USD 450/pax)",
            "Propinas a guías de lodge (significativas en USA, ~15%)",
            "Bebidas premium",
            "Lavandería express",
            "Compras personales",
        ],
    },
]

REGIONS = [
    {
        "slug": "africa",
        "name": "África",
        "meta_desc": "Safaris, deltas y desierto. Para 2026-2027 ofrecemos Namibia: dunas, Costa de los Esqueletos y Etosha.",
        "hero": "hero-savannah.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver el viaje 2026",
        "lede": "El desierto más antiguo del mundo bajo el cielo más limpio del planeta.",
        "body": "El calendario 2026-2027 lleva un solo viaje a África: Namibia en noviembre, en el peak de la luz seca, con geólogo en piso en Sossusvlei, intérprete Himba ético en Kaokoland y un astrónomo en NamibRand Dark Sky Reserve. Once días, ocho viajeros, cinco charters internos.",
        "countries": [
            {"name": "Namibia · Dunas, Esqueletos y Etosha", "blurb": "Sossusvlei, NamibRand, Skeleton Coast, Damaraland y el pan de Etosha al final de la estación seca.", "img": "hero-namibia-dunas.jpg", "href": "namibia-dunas.html"},
        ],
    },
    {
        "slug": "asia",
        "name": "Asia",
        "meta_desc": "Tres viajes en Asia para 2026-2027: la Ruta de la Seda en Uzbekistán, el sakura en Japón y el Tsechu en Bután.",
        "hero": "dest-japan.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver los viajes 2026-2027",
        "lede": "Templos al amanecer, mercados al alba, ríos que cruzan tres países sin que nadie los corte.",
        "body": "El calendario 2026-2027 tiene tres expediciones en Asia: Uzbekistán en septiembre (la Ruta de la Seda), Japón en marzo siguiendo el frente del sakura, y Bután y Nepal en abril para el festival monástico del Paro Tsechu. Cada una es la única ventana del año en que coinciden estación, festival y producto.",
        "countries": [
            {"name": "Uzbekistán · Ruta de la Seda", "blurb": "Tashkent, Khiva, Bujará y Samarcanda en pequeño grupo. Once días, once noches, historiador en piso.", "img": "hero-uzbekistan-ruta-seda.jpg", "href": "uzbekistan-ruta-seda.html"},
            {"name": "Japón · sakura y Naoshima", "blurb": "Doce días siguiendo el frente del sakura — Tokio, Kanazawa, Kioto y dos noches en Benesse House.", "img": "hero-japon-mono-no-aware.jpg", "href": "japon-mono-no-aware.html"},
            {"name": "Bután y Nepal · Paro Tsechu", "blurb": "Trece días en el Himalaya — el festival monástico, el Tiger's Nest y los cuatro valles butaneses.", "img": "hero-butan-nepal-himalaya.jpg", "href": "butan-nepal-himalaya.html"},
        ],
    },
    {
        "slug": "sudamerica",
        "name": "Sudamérica",
        "meta_desc": "Para 2026-2027 ofrecemos Bahía: el Otro Carnaval — nueve días entre Salvador y Trancoso.",
        "hero": "dest-patagonia.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver el viaje 2027",
        "lede": "El Carnaval del Brasil que importa, sin el caos de Río. Cinco noches en Salvador, tres en Trancoso.",
        "body": "Como sudamericanos, conocemos este continente de adentro. Para el calendario 2026-2027 elegimos un solo viaje: Bahía en febrero 2027, el Otro Carnaval. Con antropólogo de UFBA en piso, camarote privado para los dos días clave del Carnaval, terreiro de candomblé con la iyalorixá, y descompresión final en Trancoso.",
        "countries": [
            {"name": "Bahía · El Otro Carnaval", "blurb": "Nueve días entre Salvador y Trancoso, con antropólogo de UFBA, capoeira con mestre angoleiro, y barco privado al Espelho.", "img": "hero-bahia-otro-carnaval.jpg", "href": "bahia-otro-carnaval.html"},
        ],
    },
    {
        "slug": "polos",
        "name": "Ártico",
        "meta_desc": "Para 2026-2027 ofrecemos Laponia en enero: auroras boreales, cabañas de cristal y el reino Sami.",
        "hero": "dest-arctic.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver el viaje 2027",
        "lede": "La noche polar, la cultura Sami y la aurora boreal en su pico de actividad.",
        "body": "Los polos son los destinos más exigentes y los más generosos. Para el calendario 2026-2027 elegimos una sola expedición: Laponia entre Finlandia y Noruega, en enero 2027. Cabaña de cristal en Ivalo, familia Sami de pastores de renos en Inari, ritual sauna-hielo, husky sledding y el fiordo Lyngen del lado noruego.",
        "countries": [
            {"name": "Laponia · Auroras Boreales y el Reino Sami", "blurb": "Diez días entre Finlandia y Noruega, con investigador del Observatorio de Sodankylä y guía UIAGM opcional en Lyngen.", "img": "hero-laponia-auroras.jpg", "href": "laponia-auroras.html"},
        ],
    },
    {
        "slug": "norteamerica",
        "name": "Norteamérica",
        "meta_desc": "Para 2026-2027 ofrecemos Alaska Salvaje: Lake Clark, Kenai Fjords y aterrizaje en glaciar de Denali.",
        "hero": "dest-northamerica.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver el viaje 2027",
        "lede": "El wilderness más grande de Norteamérica en el mes en que pulsa al ritmo del salmón.",
        "body": "Norteamérica es el continente de los parques nacionales y de los caminos largos. Para 2026-2027 vamos una vez: Alaska en julio, el mes específico — veinte horas de luz, el salmón rojo corriendo río arriba, los osos pardos concentrándose en las desembocaduras. Once días con naturalista en piso y kennel de musher campeón de Iditarod.",
        "countries": [
            {"name": "Alaska Salvaje · Lake Clark y Denali", "blurb": "Tres días de osos en Chinitna Bay, flightseeing con aterrizaje en glaciar, y Kenai Fjords con catorce glaciares de marea.", "img": "hero-alaska-salvaje.jpg", "href": "alaska-salvaje.html"},
        ],
    },
    {
        "slug": "oceania",
        "name": "Oceanía",
        "meta_desc": "Australia, Nueva Zelanda y la Polinesia. Próximamente en el calendario B&A.",
        "hero": "dest-oceania.jpg",
        "nav_label": "Próximamente",
        "cta": "Avisame cuando esté disponible",
        "lede": "El último gran espacio salvaje del planeta y las islas más remotas del Pacífico.",
        "body": "Oceanía es el destino para quienes valoran el tiempo de vuelo. Estamos diseñando la primera expedición B&A a la región para el calendario 2028. Si querés que te avisemos cuando esté disponible, escribinos.",
        "countries": [
            {"name": "Nueva Zelanda · próximamente", "blurb": "Las dos islas en doce días, con helicóptero a Milford Sound. En diseño para 2028.", "img": "dest-oceania.jpg"},
            {"name": "Australia · próximamente", "blurb": "Sydney, Outback y Gran Barrera de Coral. En diseño para 2028.", "img": "dest-oceania.jpg"},
            {"name": "Polinesia francesa · próximamente", "blurb": "Tahití, Moorea, Bora Bora y atolones remotos. En diseño para 2028.", "img": "dest-caribbean.jpg"},
        ],
    },
    {
        "slug": "caribe",
        "name": "Mediterráneo y Caribe",
        "meta_desc": "Para 2026-2027 ofrecemos Croacia: las islas dálmatas en catamarán privado, junio 2027.",
        "hero": "dest-caribbean.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver el viaje 2027",
        "lede": "El Adriático es el mar más claro de Europa — visibilidad submarina de más de 30 metros.",
        "body": "Nuestra expedición de junio cruza el Adriático en catamarán crewed Lagoon 55, con capitán croata, primer oficial, chef y hostess. Cinco islas dálmatas en nueve días, desde el Palacio de Diocleciano en Split hasta las murallas de Dubrovnik, con concierto de klapa en una iglesia de Korčula y la Cueva Azul de Biševo a la hora exacta de luz cobalto.",
        "countries": [
            {"name": "Croacia · Islas Dálmatas en catamarán", "blurb": "Nueve días navegando entre Split, Brač, Hvar, Vis, Korčula, Mljet, Ston y Dubrovnik.", "img": "hero-croacia-islas-dalmatas.jpg", "href": "croacia-islas-dalmatas.html"},
        ],
    },
    {
        "slug": "oriente-medio",
        "name": "Oriente Medio y Norte de África",
        "meta_desc": "Para 2026-2027 ofrecemos Marruecos imperial: las cuatro capitales y el corazón bereber del Alto Atlas.",
        "hero": "dest-morocco.jpg",
        "nav_label": "Ver expediciones",
        "cta": "Ver el viaje 2027",
        "lede": "Cuatro capitales imperiales más el corazón bereber del Atlas, sin nada del cliché orientalista.",
        "body": "Esta región concentra algunas de las civilizaciones más antiguas y vivas del planeta. Para 2026-2027 vamos a Marruecos en mayo, en la ventana exacta — roses florece en Kelaa M'Gouna, el calor del Sahara aún no es brutal, los almendros del Atlas terminan de florecer. Con guía cultural bilingüe español-árabe y tamazight para el Atlas.",
        "countries": [
            {"name": "Marruecos · Las Cuatro Capitales y el Atlas", "blurb": "Diez días por Rabat, Mequínez, Fez, Imlil y Marrakech, con sufí en Fez y Maâlem Gnawa en Marrakech.", "img": "hero-marruecos-imperial.jpg", "href": "marruecos-imperial.html"},
        ],
    },
]

# =============================================================================
# RUN
# =============================================================================
def main():
    for j in JOURNEYS:
        path = os.path.join(REPO, j['slug'] + ".html")
        with open(path, "w") as f:
            f.write(build_journey(j))
        print(f"  ✓ {j['slug']}.html")

    for r in REGIONS:
        path = os.path.join(REPO, r['slug'] + ".html")
        with open(path, "w") as f:
            f.write(build_region(r))
        print(f"  ✓ {r['slug']}.html")

if __name__ == "__main__":
    main()
