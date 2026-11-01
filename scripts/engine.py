#!/usr/bin/env python3
"""Small static-site engine for the Namaste tarot/psychic sites. Each site supplies site/content.py (pages, layout, copy)
and site/config.json. Builds dist/: pages, sitemap.xml, robots.txt, llms.txt, 404.html, CNAME."""
import json, os, re, sys, html, shutil, urllib.request, urllib.parse, time, datetime
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'site'))
CFG = json.load(open(os.path.join(ROOT, 'site', 'config.json')))
DOMAIN = CFG['domain']; SITE = 'https://' + DOMAIN; BRAND = CFG['brand']
PREVIEW = '--preview' in sys.argv
OFFLINE = '--offline' in sys.argv
E = lambda s: html.escape(str(s), quote=True)
TODAY = datetime.date.today().isoformat()
SHOP = 'https://namastebookshop.com'
BOOK = SHOP + '/pages/book-a-reading'
PHONE, TEL, EMAIL = '212-645-0141', '+12126450141', 'info@namastebookshop.com'
STREET, CITY, REGION, ZIP = '2 West 14th Street', 'New York', 'NY', '10011'
ADDR = f'{STREET}, {CITY}, {REGION} {ZIP}'
GEO = (40.73602, -73.99404)
HC_STREET = '80 Fifth Avenue, Suite 1104'
HOURS = [('Monday to Thursday', '11 AM to 8 PM'), ('Friday and Saturday', '11 AM to 9 PM'), ('Sunday', '11 AM to 7 PM')]
HOURS_LD = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': d, 'opens': o, 'closes': c} for d, o, c in
            [(['Monday', 'Tuesday', 'Wednesday', 'Thursday'], '11:00', '20:00'), (['Friday', 'Saturday'], '11:00', '21:00'), (['Sunday'], '11:00', '19:00')]]
MAPS = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote_plus('Namaste Bookshop, 2 West 14th Street, New York, NY 10011')
DIRECTIONS = 'https://www.google.com/maps/dir/?api=1&destination=' + urllib.parse.quote_plus('2 West 14th Street, New York, NY 10011')
PHONE_PAGE = SHOP + '/pages/phone-tarot-readings'
CALENDAR = SHOP + '/pages/calendar'
GA_ID = (CFG.get('GA_MEASUREMENT_ID') or '').strip()
C = None

def ldjson(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>'
ADDRESS_LD = {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': CITY, 'addressRegion': REGION, 'postalCode': ZIP, 'addressCountry': 'US'}
def org_ld():
    o = {'@context': 'https://schema.org', '@type': C.BUSINESS_TYPE, '@id': SITE + '/#business', 'name': BRAND, 'url': SITE + '/', 'logo': SITE + '/icon-512.png',
         'image': SITE + '/og.jpg', 'description': C.ORG_DESC, 'email': EMAIL, 'telephone': '+1-212-645-0141', 'priceRange': '$$',
         'address': getattr(C, 'ADDRESS_LD', ADDRESS_LD), 'geo': {'@type': 'GeoCoordinates', 'latitude': GEO[0], 'longitude': GEO[1]},
         'openingHoursSpecification': HOURS_LD, 'hasMap': MAPS,
         'parentOrganization': {'@type': 'Organization', 'name': 'Wealth Edge Ventures Inc.'},
         'containedInPlace': {'@type': 'BookStore', 'name': 'Namaste Bookshop', 'address': ADDRESS_LD}}
    o.update(getattr(C, 'ORG_EXTRA', {}))
    return o
def shop_ld(kind=None):
    """WebSite node for the home page (kept under the old name so site modules need no change)."""
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '/#website', 'name': BRAND, 'url': SITE + '/', 'publisher': {'@id': SITE + '/#business'}}
def crumbs_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (n, p) in enumerate(trail)]}
def faq_ld(qas):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a)}} for q, a in qas]}

# ---------- products (live from the public namastebookshop.com catalog) ----------
def _get(url):
    for a in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': f'{DOMAIN}-build/1.0'})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            if a == 4: raise
            time.sleep(8 * (a + 1))
CACHE = os.path.join(ROOT, 'data'); os.makedirs(CACHE, exist_ok=True)
def _norm(p):
    v = next((v for v in p['variants'] if v.get('available')), None)
    if not v or not p.get('images') and not p.get('featured_image'): return None
    img = p.get('featured_image') or (p['images'][0]['src'] if isinstance(p['images'][0], dict) else p['images'][0])
    if img.startswith('//'): img = 'https:' + img
    price = v['price'] / 100 if isinstance(v['price'], int) else float(v['price'])
    bc = (v.get('barcode') or '').strip()
    sku = (v.get('sku') or '').strip()
    gtin = bc if re.fullmatch(r'\d{8}|\d{12,14}', bc) else (sku if re.fullmatch(r'\d{12,14}', sku) else '')
    return {'h': p['handle'], 't': p['title'], 'v': v['id'], 'p': price, 'img': img, 'vendor': p.get('vendor') or 'Namaste Bookshop', 'gtin': gtin, 'sku': sku}
def product_js(handle):
    try: return _get(f'{SHOP}/products/{handle}.js')
    except Exception: return None
def by_handles(handles):
    out = []
    for h in handles:
        p = product_js(h); n = _norm(p) if p else None
        if n: out.append(n)
        time.sleep(0.25)
    return out
def from_collection(handle, n, skip=None):
    d = _get(f'{SHOP}/collections/{handle}/products.json?limit=250')['products']
    out = []
    for p in d:
        if skip and re.search(skip, p['title'], re.I): continue
        if not any(v['available'] for v in p['variants']) or not p['images']: continue
        full = product_js(p['handle']); x = _norm(full) if full else None
        if x: out.append(x)
        time.sleep(0.25)
        if len(out) >= n: break
    return out
def cached(key, fn):
    f = os.path.join(CACHE, key + '.json')
    if OFFLINE and os.path.exists(f): return json.load(open(f))
    try:
        d = fn(); json.dump(d, open(f, 'w')); return d
    except Exception as e:
        print('fetch failed', key, e, file=sys.stderr)
        return json.load(open(f)) if os.path.exists(f) else []
def buy_url(x):
    q = urllib.parse.urlencode({'attributes[Storefront]': DOMAIN, 'note': f'Ordered on {BRAND} ({DOMAIN})', 'ref': DOMAIN.split('.')[0]})
    return f"{SHOP}/cart/{x['v']}:1?{q}"
def img(u, w): return re.sub(r'([?&])width=\d+', '', u) + ('&' if '?' in u else '?') + f'width={w}'
def money(p): return f'${p:,.2f}'
def p_ld(x):
    u = f"{SITE}/products/{x['h']}/"
    pr = {'@context': 'https://schema.org', '@type': 'Product', 'name': x['t'], 'image': img(x['img'], 800), 'url': u,
          'brand': {'@type': 'Brand', 'name': x['vendor']}, 'sku': x['sku'] or str(x['v']),
          'offers': {'@type': 'Offer', 'price': f"{x['p']:.2f}", 'priceCurrency': 'USD', 'availability': 'https://schema.org/InStock', 'url': u,
                     'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@id': SITE + '/#business'}}}
    if x['gtin']: pr['gtin'] = x['gtin']
    return pr
def product_ld(items, name):
    return {'@context': 'https://schema.org', '@type': 'ItemList', 'name': name, 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'url': f"{SITE}/products/{x['h']}/", 'name': x['t']} for i, x in enumerate(items)]}
CATALOG = {}
def _cat(x, cat):
    CATALOG.setdefault(x['h'], {'h': x['h'], 't': x['t'], 'p': x['p'], 'v': x['v'], 'i': img(x['img'], 400), 'c': cat, 'k': cat, 'r': len(CATALOG), 'x': False})
def atc(x, cat, label='Add to cart', cls='atc', ident=False):
    _cat(x, cat)
    return (f'<button type="button" class="{cls}"' + (' id="buy"' if ident else '') + f' data-atc data-v="{x["v"]}" data-h="{E(x["h"])}" data-t="{E(x["t"])}" '
            f'data-p="{x["p"]:.2f}" data-i="{E(img(x["img"], 400))}" data-c="{E(cat)}" data-k="{E(cat)}" aria-label="Add {E(x["t"])} to cart">{label}</button>')
def buy_attrs(x, cat=''):  # product cards now link to the on-site product page
    _cat(x, cat)
    return f'href="/products/{E(x["h"])}/"'
def product_pages(items, cat, shelf_name, shelf_path, crumbs_root):
    for x in items:
        _cat(x, cat)
        add(f"/products/{x['h']}/", f"{x['t']} | {BRAND}", C.product_desc(x, shelf_name), C.product_body(x, cat, shelf_name, shelf_path), ld=[p_ld(x)],
            crumbs=crumbs_root + [(shelf_name, shelf_path), (x['t'], f"/products/{x['h']}/")])
CART_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></svg>'
def cart_button():
    return f'<a class="cartbtn" href="/cart/" data-cart-open aria-label="Cart">{CART_ICON}<span class="cartn" data-cart-count hidden>0</span></a>'
def cart_boot():
    cfg = json.dumps({'shop': SHOP, 'shopName': 'namastebookshop.com', 'attr': '?attributes%5BStorefront%5D=' + urllib.parse.quote(DOMAIN), 'brand': BRAND, 'domain': DOMAIN,
                      'ref': DOMAIN.split('.')[0], 'pickup': False, 'ready': '', 'street': STREET, 'addr': ADDR, 'pair': {}, 'pairTitle': getattr(C, 'PAIR_TITLE', 'Often added too'),
                      'shopPath': getattr(C, 'SHOP_PATH', '/shop/')}).replace('</', '<\\/')
    return (f'<div class="cdim" data-cart-close hidden></div><aside id="cart" class="cdrawer" role="dialog" aria-modal="true" aria-labelledby="ctitle" hidden>'
            f'<div class="chead"><h2 id="ctitle">Your cart</h2><button type="button" class="cx" data-cart-close aria-label="Close cart">&times;</button></div>'
            f'<p class="cmsg" id="cmsg" role="status" aria-live="polite"></p><div class="cbody" data-cart-body></div></aside>'
            f'<script>window.NI_CART={cfg}</script><script src="/assets/cart.js" defer></script>')
_R = None
def readers():
    global _R
    if _R is None: _R = json.load(open(os.path.join(ROOT, 'site', 'readers.json')))
    return _R
def services_list(k, fmt):
    sv = readers()[k].get('services') or []
    if fmt == 'table': return '<table class="svc"><tbody>' + ''.join(f'<tr><td>{E(a) or "Session"}</td><td>{E(b)}</td></tr>' for a, b in sv) + '</tbody></table>'
    if fmt == 'dl': return '<dl class="svc">' + ''.join(f'<dt>{E(b)}</dt><dd>{E(a) or "Session"}</dd>' for a, b in sv) + '</dl>'
    if fmt == 'chips': return '<ul class="svc">' + ''.join(f'<li><b>{E(b)}</b> {E(a)}</li>' for a, b in sv) + '</ul>'
    return '<p class="svc">' + ' &middot; '.join(f'{E(a)}: {E(b)}' for a, b in sv) + '</p>'
def person_ld(k, path):
    r = readers()[k]
    return {'@context': 'https://schema.org', '@type': 'Person', 'name': r['name'], 'image': r['img'], 'url': SITE + path, 'jobTitle': r.get('spec', ''),
            'worksFor': {'@id': SITE + '/#business'}}
# ---------- page assembly ----------
PAGES = []
def add(path, title, desc, body, ld=(), crumbs=None, nav=None, robots=None, sitemap=True, ogimg='/og.jpg'):
    PAGES.append(dict(path=path, title=title, desc=desc, body=body, ld=list(ld), crumbs=crumbs, nav=nav, robots=robots, sitemap=sitemap, ogimg=ogimg))
def ga_head():
    if PREVIEW or not GA_ID: return ''
    cfg = json.dumps({'site_brand': BRAND}).replace('</', '<\\/')
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}",{cfg});</script>')
def render(pg):
    canon = SITE + pg['path']
    ld = [org_ld()] + pg['ld']
    if pg['crumbs']: ld.append(crumbs_ld(pg['crumbs']))
    head = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{ga_head()}'
            f'<title>{E(pg["title"])}</title><meta name="description" content="{E(pg["desc"])}">'
            + (f'<meta name="robots" content="{pg["robots"]}">' if pg['robots'] else '')
            + (f'<link rel="canonical" href="{canon}">' if pg['robots'] is None else '')
            + f'<meta property="og:type" content="website"><meta property="og:site_name" content="{E(BRAND)}"><meta property="og:title" content="{E(pg["title"])}">'
            f'<meta property="og:description" content="{E(pg["desc"])}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}{pg["ogimg"]}">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="theme-color" content="{C.THEME_COLOR}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">'
            + (f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{C.FONTS}">' if C.FONTS else '')
            + ('<link rel="stylesheet" href="/assets/cart.css">' if getattr(C, 'CART', False) else '') + '<link rel="stylesheet" href="/assets/site.css">' + ''.join(ldjson(x) for x in ld) + '</head>')
    body = C.shell(pg)
    tail = (cart_boot() if getattr(C, 'CART', False) else '') + ('<script src="/assets/ga.js" defer></script>' if ga_head() else '')
    return head + body.replace('</body>', tail + '</body>') if '</body>' in body else head + body + tail + '</body></html>'
def write(path, s):
    f = os.path.join(ROOT, 'dist', path.lstrip('/'))
    if f.endswith('/') or not os.path.splitext(f)[1]: f = os.path.join(f, 'index.html')
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, 'w').write(s)
def build():
    global C
    import content as C
    dist = os.path.join(ROOT, 'dist')
    if os.path.exists(dist): shutil.rmtree(dist)
    os.makedirs(os.path.join(dist, 'assets'))
    C.pages()
    for pg in PAGES: write(pg['path'], render(pg))
    nf = dict(path='/404.html', title=f'Page not found | {BRAND}', desc=C.NOTFOUND_DESC, body=C.NOTFOUND, ld=[], crumbs=None, nav=None, robots='noindex', sitemap=False, ogimg='/og.jpg')
    open(os.path.join(dist, '404.html'), 'w').write(render(nf))
    open(os.path.join(dist, 'assets', 'site.css'), 'w').write(C.CSS)
    for f in ('ga.js', 'cart.js', 'cart.css'): shutil.copy(os.path.join(ROOT, 'scripts', f), os.path.join(dist, 'assets', f))
    if CATALOG:
        os.makedirs(os.path.join(dist, 'data'), exist_ok=True); json.dump(list(CATALOG.values()), open(os.path.join(dist, 'data', 'catalog.json'), 'w'))
    st = os.path.join(ROOT, 'static')
    if os.path.isdir(st):
        for f in os.listdir(st): shutil.copy(os.path.join(st, f), os.path.join(dist, f))
    open(os.path.join(dist, 'CNAME'), 'w').write(DOMAIN + '\n')
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pg in PAGES:
        if pg['sitemap'] and pg['robots'] is None: sm.append(f'<url><loc>{SITE}{pg["path"]}</loc><lastmod>{TODAY}</lastmod></url>')
    sm.append('</urlset>'); open(os.path.join(dist, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'ChatGPT-User', 'GPTBot', 'PerplexityBot', 'Google-Extended', 'ClaudeBot', 'Applebot']
    open(os.path.join(dist, 'robots.txt'), 'w').write(''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots) + f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    ll = [f'# {BRAND}', '', f'> {C.ORG_DESC}', '', C.LLMS_NOTE, '', f'Contact: {PHONE}, {EMAIL}. Address: Namaste Bookshop, {ADDR}.', '', '## Pages', '']
    ll += [f'- [{pg["title"]}]({SITE}{pg["path"]}): {pg["desc"]}' for pg in PAGES if pg['sitemap']]
    open(os.path.join(dist, 'llms.txt'), 'w').write('\n'.join(ll) + '\n')
    print(f'built {len(PAGES)} pages + 404 into dist/ for {SITE}')
def privacy(intro, products=False):
    shop = ('<h2>Buying something</h2><p>Your cart is kept in this browser. When you press Check out, it is handed to a secure Shopify checkout run by Namaste Bookshop (namastebookshop.com), which fills orders for this site. '
            'The order is tagged with this site\'s name so the shop knows where it came from. Payment, shipping and pickup details are collected there, under the '
            'privacy policy shown at checkout.</p>') if products else ''
    return (f'<h1>Privacy</h1><p>{intro}</p><h2>Analytics</h2><p>This site uses Google Analytics to count visits and see which pages are viewed and which '
            'links are tapped, such as booking, call or directions links. Google may set cookies to do this. You can block these with your browser settings or an '
            'ad blocker, and the site will still work.</p><h2>Bookings</h2><p>Reading appointments are booked on Square, the scheduling service our readers use. '
            'Anything you enter there is handled by Square and Namaste Bookshop, not stored by this site.</p>' + shop +
            f'<h2>Contact</h2><p>Questions about your data: {EMAIL} or {PHONE}. {BRAND} is run by Wealth Edge Ventures Inc., {ADDR}.</p><p class="small">Updated {TODAY}.</p>')
