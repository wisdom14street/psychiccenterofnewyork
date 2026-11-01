"""Catalog + storefront presentation for the Namaste tarot sites: full-catalog fetch (public products.json, read only),
per-site selection, clean display titles, galleries, variants, compare-at prices, sold-out handling, shelf pages with
static pagination plus client-side sort/filter (assets/shop.js), product pages with related items and JSON-LD."""
import json, os, re, time, math, html, urllib.request, urllib.parse, datetime
import engine as G
import present as PR
E = G.E
PER_PAGE = 48
DATA = os.path.join(G.ROOT, 'data')

# ---------- fetch ----------
def _get(url):
    for a in range(6):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': f'{G.DOMAIN}-build/1.0'})
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception as e:
            if a == 5: raise
            time.sleep(6 * (a + 1))
def _slim(p):
    return {'id': p['id'], 'title': p['title'], 'handle': p['handle'], 'body_html': (p.get('body_html') or '')[:9000], 'vendor': p.get('vendor') or '',
            'product_type': (p.get('product_type') or '').strip(), 'tags': p.get('tags') or [], 'created_at': p.get('created_at') or '',
            'options': [o.get('name') for o in p.get('options') or []],
            'variants': [{k: v.get(k) for k in ('id', 'title', 'price', 'compare_at_price', 'available', 'sku', 'option1', 'option2', 'option3')} for v in p['variants']],
            'images': [{'src': i['src'], 'w': i.get('width'), 'h': i.get('height')} for i in p.get('images') or []]}
def load(select, collections):
    """select(p, colsets) -> kind or None. Returns (products, colsets). Online: pages the whole public catalog and the
    named collections; falls back to the committed data/ copy if the store cannot be reached."""
    fp, fc = os.path.join(DATA, 'products.json'), os.path.join(DATA, 'collections.json')
    if not G.OFFLINE:
        try:
            cols = {}
            for c in collections:
                hs, pg = [], 1
                while True:
                    d = _get(f'{G.SHOP}/collections/{c}/products.json?limit=250&page={pg}')['products']
                    if not d: break
                    hs += [x['handle'] for x in d]; pg += 1; time.sleep(0.6)
                cols[c] = hs
            S = {k: set(v) for k, v in cols.items()}
            out, pg = [], 1
            while True:
                d = _get(f'{G.SHOP}/products.json?limit=250&page={pg}')['products']
                if not d: break
                for p in d:
                    k = select(p, S)
                    if k: q = _slim(p); q['kind'] = k; out.append(q)
                pg += 1; time.sleep(0.8)
            if len(out) > 20:
                json.dump(out, open(fp, 'w'), separators=(',', ':')); json.dump(cols, open(fc, 'w'), separators=(',', ':'))
        except Exception as e:
            print('catalog fetch failed, using cached copy:', e)
    prods = json.load(open(fp)); cols = json.load(open(fc))
    S = {k: set(v) for k, v in cols.items()}
    for p in prods: p['kind'] = select(p, S) or p.get('kind')
    return [p for p in prods if p.get('kind')], S

# ---------- presentation ----------
PUB_TAIL = r'(U\.?\s?S\.? Games( Systems)?( Inc\.?)?|Lo Scarabeo|Llewellyn( Publications)?|Hay House( Inc\.?)?|Blue Angel( Publishing)?|Rockpool( Publishing)?|Schiffer( Publishing)?|Red Wheel ?/ ?Weiser|Weiser Books|Chronicle Books|Sterling( Publishing)?)'
def split_title(raw):
    t = PR.clean_title(raw)
    oop = bool(re.search(r'out of print', t, re.I))
    t = re.sub(r'\s*[-\u2013]?\s*collectable\s*/\s*out of print.*$', '', t, flags=re.I)
    t = re.sub(r'\s+[-\u2013]\s+' + PUB_TAIL + r'\s*$', '', t, flags=re.I)
    t = re.sub(r'\s*\((Author|Illustrator|Editor|Foreword|Contributor|Artist)\)', '', t, flags=re.I)
    author = ''
    m = re.search(r'\s+(?:[-\u2013]\s+)?(?:by|By|BY)[:\s]+(?!the\b)([^()]+?)\s*$', t)
    if m and len(t[:m.start()]) >= 4: author, t = m.group(1).strip(' .,'), t[:m.start()]
    author = re.split(r'\s+[-\u2013]\s+', author)[0].strip()
    if re.fullmatch(PUB_TAIL, author, re.I): author = ''
    sub = ''
    m = re.match(r'^(.*?)\s*\(([^()]+)\)\s*$', t)
    if m and len(m.group(1)) >= 4: t, sub = m.group(1).strip(' :-'), m.group(2).strip()
    if ':' in t:
        a, b = t.split(':', 1); a, b = a.strip(), b.strip()
        if len(a.split()) == 1:
            parts = re.split(r'\s*(?::|\u2015|\u2014)\s*', b, 1)
            if len(parts) == 2 and len(parts[1].split()) >= 2: t, sub = f'{a}: {parts[0]}', (parts[1] + ((' \u00b7 ' + sub) if sub else ''))
        elif len(b.split()) >= 4 and len(a) >= 4: t, sub = a, (b + ((' \u00b7 ' + sub) if sub else '')).strip(' :')
    t = re.sub(r'\s{2,}', ' ', t).strip(' :-\u2013,')
    sub = re.sub(r'^[-\u2013\u2015 ]+|[-\u2013 ]+$', '', sub)
    return t or PR.clean_title(raw), sub, author, oop
def n_cards(p):
    m = re.search(r'\b(\d{2,3})[- ]?(?:card|cards)\b', p['title'] + ' ' + re.sub(r'<[^>]+>', ' ', p.get('body_html') or '')[:1500], re.I)
    n = int(m.group(1)) if m else None
    return n if n and 10 <= n <= 120 else None
def pimg(u, w): return G.img(u, w)
PUBMAP = [(r'u\.?s\.? games.*', 'U.S. Games Systems'), (r'llewellyn.*', 'Llewellyn'), (r'(simon )?rockpool.*', 'Rockpool Publishing'),
          (r'blue angel.*', 'Blue Angel Publishing'), (r'red wheel.*|weiser.*', 'Red Wheel/Weiser'), (r'ag ?m(uller)?( urania)?', 'AGM-Urania'),
          (r'hay house.*', 'Hay House'), (r'harper ?collins.*', 'HarperCollins'), (r'lotus press', 'Lotus Press')]
PUBDROP = r"namaste.*|.*bookshop.*|texasbkmn|dsgnbdk|ocnlkw|nagimpinc|bnjint|vlorg|consignments?|mps distribution.*|ingram.*|benjamin international|lotus light.*|.*collectable|"
EMOJI = re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\uFE0F\u200D]+ ?')
def pub_clean(v):
    """Turn a Shopify vendor field into a publisher name shoppers recognise; drop distributor and internal codes."""
    v = (v or '').strip()
    if re.fullmatch(PUBDROP, v, re.I): return ''
    for pat, name in PUBMAP:
        if re.fullmatch(pat, v, re.I): return name
    return v
def build_items(prods, styles, rank_cols=()):
    """styles: [(collection_handle, label)]; rank_cols: collections whose members sort first in Featured."""
    out = []
    for p in prods:
        name, sub, author, oop = split_title(p['title'])
        vs = [v for v in p['variants']]
        live = [v for v in vs if v.get('available')]
        v0 = (live or vs)[0]
        price = float(v0['price']); cmp_ = float(v0['compare_at_price']) if v0.get('compare_at_price') else 0.0
        if cmp_ <= price: cmp_ = 0.0
        imgs = [i for i in p['images'] if i.get('src')]
        vendor = (p.get('vendor') or '').strip()
        vendor = pub_clean(vendor)
        x = {'h': p['handle'], 'raw': p['title'], 'name': name, 'sub': sub, 'author': author, 'oop': oop, 'pub': vendor, 'kind': p['kind'],
             'styles': [lab for c, lab in styles if p['handle'] in STY.get(c, ())], 'imgs': imgs, 'img': imgs[0]['src'] if imgs else '',
             'vars': vs, 'opts': [o for o in p.get('options') or [] if o and o != 'Title'], 'v': v0['id'], 'p': price, 'cmp': cmp_, 'avail': bool(live),
             'sku': (v0.get('sku') or '').strip(), 'gtin': '', 'vendor': vendor or G.BRAND, 'created': (p.get('created_at') or '')[:10],
             'cards': n_cards(p), 'body': p.get('body_html') or '', 'rank': 0, 'type': p.get('product_type') or ''}
        sk = x['sku']; x['gtin'] = sk if re.fullmatch(r'97[89]\d{10}|\d{12,13}', sk) else ''
        x['rank'] = next((i for i, c in enumerate(rank_cols) if p['handle'] in STY.get(c, ())), len(rank_cols))
        out.append(x)
    out.sort(key=lambda x: (not x['avail'], x['rank'], not x['img'], -int(x['created'].replace('-', '') or 0)))
    for i, x in enumerate(out): x['r'] = i
    return out
STY = {}
def set_collections(S): STY.clear(); STY.update(S)

def money(p): return G.money(p)
def price_html(x, cls='pp'):
    s = f'<span class="{cls}"><b>{money(x["p"])}</b>'
    if x['cmp']: s += f' <s aria-label="was">{money(x["cmp"])}</s>'
    return s + '</span>'
def ph(x, cls=''):
    return PR.placeholder([(x['name'], 'n1'), (x['author'] or x['pub'], 'n2')], cls, 'Photo coming soon')
def img_tag(x, w, cls, eager=False, alt=None, sizes='(min-width:1100px) 250px, (min-width:700px) 30vw, 46vw'):
    if not x['img']: return ph(x, cls)
    u = x['img']; a = E(alt if alt is not None else x['name'])
    ws = [160, 240, 360, 480, 640]
    return (f'<img class="{cls}" src="{E(pimg(u, w))}" srcset="{", ".join(E(pimg(u, n)) + f" {n}w" for n in ws)}" sizes="{sizes}" alt="{a}" width="{w}" height="{w}"'
            + (' fetchpriority="high"' if eager == 'high' else '') + ('' if eager else ' loading="lazy"') + ' decoding="async">')
def _cat(x, cat):
    G.CATALOG.setdefault(x['h'], {'h': x['h'], 't': x['name'], 'p': x['p'], 'v': x['v'], 'i': pimg(x['img'], 400) if x['img'] else '/assets/no-photo.svg',
                                  'c': cat, 'k': x['kind'], 'r': x['r'], 'x': not x['avail']})
def atc_attrs(x, cat):
    return (f'data-atc data-v="{x["v"]}" data-h="{E(x["h"])}" data-t="{E(x["name"])}" data-p="{x["p"]:.2f}" '
            f'data-i="{E(pimg(x["img"], 400) if x["img"] else "/assets/no-photo.svg")}" data-c="{E(cat)}" data-k="{E(x["kind"])}"')
def card(x, cat, eager=False, label='Add'):
    _cat(x, cat)
    byline = x['author'] or x['pub']
    flags = ('<span class="tag sold">Sold out</span>' if not x['avail'] else '') + ('<span class="tag sale">Sale</span>' if x['cmp'] and x['avail'] else '') + ('<span class="tag oop">Out of print</span>' if x['oop'] else '')
    if not x['avail']: btn = f'<a class="qa ghost" href="/products/{E(x["h"])}/">Details</a>'
    elif len([v for v in x['vars'] if v.get('available')]) > 1: btn = f'<a class="qa" href="/products/{E(x["h"])}/">Choose</a>'
    else: btn = f'<button type="button" class="qa" {atc_attrs(x, cat)} aria-label="Add {E(x["name"])} to cart">{label}</button>'
    return (f'<li class="pc{" out" if not x["avail"] else ""}"><a class="pbox" href="/products/{E(x["h"])}/" tabindex="-1" aria-hidden="true">{img_tag(x, 300, "pi", eager, "")}{flags}</a>'
            f'<div class="pm"><a class="pn" href="/products/{E(x["h"])}/">{E(x["name"])}</a>' + (f'<span class="pa">{E(byline)}</span>' if byline else '')
            + f'{price_html(x)}</div>{btn}</li>')
def js_row(x):
    return {'h': x['h'], 'n': x['name'], 'a': x['author'] or x['pub'], 'p': x['p'], 'c': x['cmp'], 'i': pimg(x['img'], 300) if x['img'] else '', 's': 1 if x['avail'] else 0,
            'k': x['kind'], 'st': x['styles'], 'pb': x['pub'], 'd': x['created'], 'v': x['v'], 'm': 1 if len([v for v in x['vars'] if v.get('available')]) > 1 else 0,
            'o': 1 if x['oop'] else 0, 'r': x['r']}

PRICE_BUCKETS = [('u20', 'Under $20', 0, 20), ('20-35', '$20 to $35', 20, 35), ('35-50', '$35 to $50', 35, 50), ('50', '$50 and up', 50, 1e9)]
def toolbar(items, kinds, slug):
    ks = sorted({x['kind'] for x in items}, key=lambda k: list(kinds).index(k) if k in kinds else 99)
    sts = {}
    for x in items:
        for s in x['styles']: sts[s] = sts.get(s, 0) + 1
    pubs = {}
    for x in items:
        if x['pub']: pubs[x['pub']] = pubs.get(x['pub'], 0) + 1
    top = sorted(pubs.items(), key=lambda kv: (-kv[1], kv[0]))[:30]
    sel = lambda name, label, opts: (f'<label class="fl"><span>{label}</span><select name="{name}" data-f="{name}"><option value="">All</option>'
                                      + ''.join(f'<option value="{E(v)}">{E(t)}</option>' for v, t in opts) + '</select></label>')
    h = (f'<form class="tools" data-shelf="{E(slug)}" aria-label="Sort and filter" onsubmit="return false">'
         f'<label class="fl"><span>Sort</span><select name="sort" data-f="sort"><option value="">Featured</option><option value="new">Newest</option>'
         f'<option value="lo">Price, low to high</option><option value="hi">Price, high to low</option><option value="az">A to Z</option></select></label>')
    h += '<details class="tf" data-tf><summary>Filter</summary><div class="tfi">'
    if len(ks) > 1: h += sel('k', 'Type', [(k, kinds[k][1]) for k in ks])
    if sts: h += sel('st', 'Style', sorted(((s, f'{s} ({n})') for s, n in sts.items()), key=lambda t: t[0]))
    h += sel('pr', 'Price', [(a, b) for a, b, _, _ in PRICE_BUCKETS])
    if len(top) > 1: h += sel('pb', 'Publisher', [(p, f'{p} ({n})') for p, n in sorted(top)])
    h += (f'<label class="chk"><input type="checkbox" data-f="s" value="1"> In stock only</label></div></details>'
          f'<p class="cnt" data-count aria-live="polite">{len(items)} items, {sum(x["avail"] for x in items)} in stock</p></form>')
    return h
def shelf(path, slug, cat, title, desc, h1, intro, items, kinds, crumbs, after='', ld_name=None):
    """static, paginated shelf + JSON for client-side sort/filter"""
    os.makedirs(os.path.join(G.ROOT, 'dist', 'data', 'shelf'), exist_ok=True)
    SHELF_JSON[slug] = [js_row(x) for x in items]
    for x in items: _cat(x, cat)
    pages = max(1, math.ceil(len(items) / PER_PAGE))
    for n in range(1, pages + 1):
        chunk = items[(n - 1) * PER_PAGE: n * PER_PAGE]
        url = path if n == 1 else f'{path}page/{n}/'
        nav = ''
        if pages > 1:
            nums = sorted({1, pages, n - 1, n, n + 1} & set(range(1, pages + 1)))
            parts, last = [], 0
            for k in nums:
                if k - last > 1: parts.append('<span class="gap">&hellip;</span>')
                u = path if k == 1 else f'{path}page/{k}/'
                parts.append(f'<span class="cur" aria-current="page">{k}</span>' if k == n else f'<a href="{u}">{k}</a>'); last = k
            prev = f'<a rel="prev" href="{path if n == 2 else f"{path}page/{n-1}/"}">&larr; Previous</a>' if n > 1 else ''
            nxt = f'<a rel="next" href="{path}page/{n+1}/">Next &rarr;</a>' if n < pages else ''
            nav = f'<nav class="pager" aria-label="Pages">{prev}{"".join(parts)}{nxt}</nav>'
        body = (f'<section class="shop"><div class="shead"><h1>{h1}' + (f' <span class="pgn">page {n} of {pages}</span>' if n > 1 else '') + f'</h1>{intro if n == 1 else ""}</div>'
                f'{toolbar(items, kinds, slug)}<ul class="grid" data-grid>' + ''.join(card(x, cat, eager=(('high' if i < 2 else True) if (i < 4 and n == 1) else False)) for i, x in enumerate(chunk)) + '</ul>'
                f'<button type="button" class="more" data-more hidden>Show more</button>{nav}{after if n == 1 else ""}</section>')
        t = title if n == 1 else f'{title.split(" | ")[0]}, Page {n} | {G.BRAND}'
        G.add(url, t, desc if n == 1 else f'{desc.rstrip(".")}. Page {n} of {pages}.', body,
              ld=[G.product_ld_items(chunk, ld_name or h1)] if chunk else [], crumbs=crumbs + ([(f'Page {n}', url)] if n > 1 else []))
SHELF_JSON = {}
def write_json(dist):
    d = os.path.join(dist, 'data', 'shelf'); os.makedirs(d, exist_ok=True)
    for k, v in SHELF_JSON.items(): json.dump(v, open(os.path.join(d, k + '.json'), 'w'), separators=(',', ':'), ensure_ascii=False)

def p_ld(x, url):
    av = 'https://schema.org/InStock' if x['avail'] else 'https://schema.org/OutOfStock'
    pr = {'@context': 'https://schema.org', '@type': 'Product', 'name': x['name'] + (f': {x["sub"]}' if x['sub'] else ''), 'url': url,
          'sku': x['sku'] or str(x['v']), 'offers': {'@type': 'Offer', 'price': f'{x["p"]:.2f}', 'priceCurrency': 'USD', 'availability': av, 'url': url,
          'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@id': G.SITE + '/#business'}}}
    if x['imgs']: pr['image'] = [pimg(i['src'], 1000) for i in x['imgs'][:6]]
    if x['pub']: pr['brand'] = {'@type': 'Brand', 'name': x['pub']}
    if x['gtin']: pr['gtin'] = x['gtin']
    if x['author']: pr['author'] = {'@type': 'Person', 'name': x['author']}
    d = PR.body_text(x.get('_desc', ''))[:480]
    if d: pr['description'] = d
    return pr
def related(x, pool, n=8):
    st = set(x['styles'])
    def score(y):
        return (not y['avail'], -(len(st & set(y['styles'])) * 3 + (y['pub'] == x['pub'] and bool(x['pub'])) * 2 + (y['kind'] == x['kind'])), not y['img'], y['r'])
    return sorted((y for y in pool if y['h'] != x['h']), key=score)[:n]
def gallery(x):
    if not x['imgs']: return f'<div class="gal">{ph(x, "big")}</div>'
    main = x['imgs'][0]['src']
    th = ''
    if len(x['imgs']) > 1:
        th = '<div class="thumbs" role="list">' + ''.join(
            f'<button type="button" role="listitem" class="th{" on" if i == 0 else ""}" data-src="{E(pimg(im["src"], 800))}" data-src2="{E(pimg(im["src"], 1400))}" aria-label="Show image {i + 1} of {len(x["imgs"])}">'
            f'<img src="{E(pimg(im["src"], 120))}" alt="" width="64" height="64" loading="lazy"></button>' for i, im in enumerate(x['imgs'][:10])) + '</div>'
    return (f'<div class="gal"><div class="gmain"><img id="gimg" src="{E(pimg(main, 800))}" srcset="{", ".join(E(pimg(main, n)) + f" {n}w" for n in (480, 640, 800, 1100, 1400))}" sizes="(min-width:860px) 460px, 92vw" '
            f'alt="{E(x["name"])}" width="800" height="800" fetchpriority="high"></div>{th}</div>')
def variant_picker(x):
    vs = x['vars']
    if len(vs) < 2: return ''
    lab = x['opts'][0] if x['opts'] else 'Option'
    return (f'<label class="vsel"><span>{E(lab)}</span><select data-variant>' + ''.join(
        f'<option value="{v["id"]}" data-p="{float(v["price"]):.2f}" data-c="{float(v["compare_at_price"] or 0):.2f}"' + ('' if v.get('available') else ' disabled')
        + (' selected' if v['id'] == x['v'] else '') + f'>{E(v["title"])}' + ('' if v.get('available') else ' (sold out)') + '</option>' for v in vs) + '</select></label>')
def buy_block(x, cat, label='Add to cart'):
    if x['avail']:
        btn = f'<button type="button" id="buy" class="buy" {atc_attrs(x, cat)}>{label}</button>'
    else:
        btn = (f'<button type="button" id="buy" class="buy" disabled aria-disabled="true" {atc_attrs(x, cat)}>Sold out</button>'
               f'<p class="soldnote">Sold out online right now. It may still be on the shelf; call <a href="tel:{G.TEL}">{G.PHONE}</a> to check.</p>')
    return f'<div class="buyrow">{price_html(x, "bigp")}{variant_picker(x)}{btn}</div>'
def sticky(x, cat):
    if not x['avail']: return ''
    return (f'<div class="sbuy" data-sbuy hidden><span class="sn">{E(x["name"])}</span>{price_html(x, "sp")}'
            f'<button type="button" class="qa" {atc_attrs(x, cat)}>Add</button></div>')
def product_page(x, cat, shelf_name, shelf_path, pool, crumbs_root, intro_html, desc_mode='strict', desc_limit=1400, desc_head='From the publisher', meta=None, extra=''):
    _cat(x, cat)
    url = f'{G.SITE}/products/{urllib.parse.quote(x["h"])}/'
    desc = PR.clean_body(EMOJI.sub('', x['body'] or ''), desc_mode, desc_limit, x['raw']) if desc_limit else ''
    x['_desc'] = desc
    facts = [('By', x['author']), ('Publisher', x['pub']), ('Cards', str(x['cards']) if x['cards'] else ''), ('ISBN' if x['gtin'].startswith('97') else 'Barcode', x['gtin']), ('SKU', '' if x['gtin'] else x['sku'])]
    dl = '<dl class="facts">' + ''.join(f'<dt>{a}</dt><dd>{E(b)}</dd>' for a, b in facts if b) + '</dl>'
    rel = related(x, pool)
    body = (f'<section class="prod"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span> <a href="{shelf_path}">{E(shelf_name)}</a>'
            f' <span aria-hidden="true">&rsaquo;</span> <span aria-current="page">{E(x["name"])}</span></nav><div class="pgrid">{gallery(x)}<div class="pinfo">'
            f'<p class="kick">{E(shelf_name)}' + (' &middot; out of print' if x['oop'] else '') + f'</p><h1>{E(x["name"])}</h1>'
            + (f'<p class="psub">{E(x["sub"])}</p>' if x['sub'] else '') + (f'<p class="pby">by {E(x["author"])}</p>' if x['author'] else '')
            + buy_block(x, cat) + f'<p class="ship">Ships from New York City. Shipping and tax are shown at checkout.</p>{intro_html}{dl}</div></div>'
            + (f'<section class="pdesc"><h2>{desc_head}</h2>{desc}</section>' if desc else '') + extra
            + (f'<section class="rel"><h2>You might also like</h2><ul class="grid">' + ''.join(card(y, cat) for y in rel) + '</ul></section>' if rel else '')
            + f'</section>{sticky(x, cat)}<script>window.NI_PRODUCT={json.dumps({"handle": x["h"], "v": x["v"]})}</script>')
    t = meta[0] if meta else f'{x["name"]}' + (f' by {x["author"]}' if x['author'] and len(x['name']) < 40 else '') + f' | {G.BRAND}'
    dsc = meta[1] if meta else ''
    pre = ''
    if x['imgs']:
        m0 = x['imgs'][0]['src']
        pre = (f'<link rel="preload" as="image" fetchpriority="high" href="{E(pimg(m0, 800))}" imagesrcset="{", ".join(E(pimg(m0, n)) + f" {n}w" for n in (480, 640, 800, 1100, 1400))}" imagesizes="(min-width:860px) 460px, 92vw">')
    G.add(f'/products/{x["h"]}/', t, dsc, body, ld=[p_ld(x, url)], crumbs=crumbs_root + [(shelf_name, shelf_path), (x['name'], f'/products/{x["h"]}/')], preload=pre)
