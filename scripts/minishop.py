"""Shared shelf/hub/product-page builder for the smaller Namaste tarot/psychic shops (psychics, first-reading, psychic center)."""
import engine as G
import shop as S
E = G.E
def build(SELECT, COLLECTIONS, STYLES, KINDS, SHELVES, hub_path, hub_title, hub_desc, hub_h1, hub_intro, p_intro, rank_cols=(), crumb_label='Shop', feature_kinds=None, note='', feat_h='Picks to start with', search=None):
    prods, C = S.load(SELECT, COLLECTIONS)
    S.set_collections(C)
    items = S.build_items(prods, STYLES, rank_cols)
    shelf_of = {k: sh for sh in SHELVES for k in sh[2]}
    by = {}
    for x in items: by.setdefault(shelf_of[x['kind']][0], []).append(x)
    root = [('Home', '/'), (crumb_label, hub_path)]
    for slug, path, kinds, label, h1, intro in SHELVES:
        its = by.get(slug, [])
        if not its: continue
        n_in = sum(x['avail'] for x in its)
        S.shelf(path, slug, slug, f'{h1} ({n_in} in Stock) | {G.BRAND}', f'{intro.split(".")[0]}. {n_in} in stock now at {G.BRAND}.',
                h1, f'<p>{intro}</p>', its, KINDS, root + [(label, path)])
        for x in its:
            lab = KINDS[x['kind']][0]
            t = x['name'] + (f' by {x["author"]}' if x['author'] and len(x['name']) + len(x['author']) < 56 else '') + f' | {lab} | {G.BRAND}'
            d = (x['name'] + (f' by {x["author"]}' if x['author'] else '') + f': {lab.lower()}, {G.money(x["p"])}. '
                 + ('In stock; ships from New York City.' if x['avail'] else 'Sold out online right now; call to check the shelf.'))
            S.product_page(x, slug, label, path, its, root, p_intro(x), meta=(t, d))
    fk = feature_kinds or [k for k in KINDS]
    feat = sorted([x for x in items if x['avail'] and x['kind'] in fk], key=lambda x: x['r'])[:8]
    hub = (f'<section class="shop"><div class="shead"><h1>{hub_h1}</h1>{hub_intro}</div>{S.search_box(*(search[:1] if search else ()))}<ul class="shelves">'
           + ''.join(f'<li><a href="{path}"><b>{label}</b><span>{len(by.get(slug, []))} items, {sum(x["avail"] for x in by.get(slug, []))} in stock</span></a></li>'
                     for slug, path, _, label, _, _ in SHELVES if by.get(slug))
           + f'</ul><h2>{feat_h}</h2><ul class="grid">' + ''.join(S.card(x, shelf_of[x['kind']][0]) for x in feat) + '</ul>'
           + (f'<p class="small">{note}</p>' if note else '') + '</section>')
    G.add(hub_path, hub_title, hub_desc, hub, ld=[G.product_ld_items(feat, hub_h1)] if feat else [], crumbs=root)
    S.search_page(hub_path, intro=(search[1] if search else None))
    return items, by
