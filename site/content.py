"""Psychic Center of New York: a reading center on two floors of one building at Fifth Avenue and 14th Street. Ground-floor tables inside
Namaste Bookshop, private rooms upstairs in Suite 1104, its readers, sessions, schedule and visit info."""
import json, os
import engine as G
E = G.E
BUSINESS_TYPE = 'LocalBusiness'
THEME_COLOR = '#14284b'
FONTS = 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;800&family=Karla:wght@400;600;700&display=swap'
ORG_DESC = 'Psychic Center of New York offers tarot, psychic, mediumship and astrology readings, hypnotherapy and energy sessions in two Manhattan spaces: reading tables inside Namaste Bookshop at 2 West 14th Street and private rooms upstairs at 80 Fifth Avenue, Suite 1104.'
LLMS_NOTE = ('Psychic Center of New York is operated by Wealth Edge Ventures Inc. Its ground-floor reading tables are inside Namaste Bookshop, 2 West 14th Street, New York, NY 10011, and its private rooms are on the 11th floor of the same building, 80 Fifth Avenue, Suite 1104 (the Namaste Healing Center suite). '
             'Each reader has a profile on this site; booking is the reader\'s own Square scheduling page.')
R = json.load(open(os.path.join(os.path.dirname(__file__), 'readers.json')))
UP = ['rebecca-martinez', 'catherine-marks', 'anthony-fusco', 'casey-deamoira', 'high-priestess-judith', 'damon-stang', 'jennifer-shanteau', 'dainichi-lazuli', 'mallika']
DOWN = ['alexander-d-santiago', 'andrea-dopewitchkira', 'priya', 'tyler-t-mann-tarot', 'sophia-strange', 'brinly-erin', 'lizanne']
PLACES = [{'@type': 'Place', 'name': 'Ground-floor reading tables, inside Namaste Bookshop', 'address': G.ADDRESS_LD},
          {'@type': 'Place', 'name': 'Suite 1104 private rooms (Namaste Healing Center)', 'address': {'@type': 'PostalAddress', 'streetAddress': '80 Fifth Avenue, Suite 1104', 'addressLocality': 'New York', 'addressRegion': 'NY', 'postalCode': '10011', 'addressCountry': 'US'}}]
ORG_EXTRA = {'location': PLACES}
NAV = [('/readers/', 'Readers'), ('/bookshop-floor/', 'Ground floor'), ('/healing-center/', 'Suite 1104'), ('/sessions/', 'Sessions'), ('/schedule-and-events/', 'Schedule'), ('/supplies/', 'Supplies'), ('/visit/', 'Visit'), ('/faq/', 'FAQ')]
CART = True
SHOP_PATH = '/supplies/'
import re
import minishop as MS
COLLECTIONS = []
STYLES = []
KINDS = {'cloth': ('Reading cloth', 'Reading cloths'), 'bag': ('Deck bag', 'Deck bags & pouches'), 'box': ('Deck box', 'Deck boxes'), 'stand': ('Card stand', 'Card stands'),
         'talisman': ('Talisman', 'Talismans'), 'journal': ('Journal', 'Journals'), 'bowl': ('Singing bowl', 'Singing bowls'), 'bell': ('Bell or chime', 'Bells & tingshas'),
         'sage': ('Smudge bundle', 'Sage & smudge'), 'mist': ('Cleansing spray', 'Cleansing sprays & waters')}
def SELECT(p, C):
    t = p['title']; ty = (p.get('product_type') or '').strip(); tl = t.lower()
    if re.search(r'wholesale|display of \d+|gift card', tl): return None
    if re.search(r'altar cloth|tarot cloth|reading cloth', tl): return 'cloth'
    if re.search(r'card (holder|stand)|tarot (holder|stand)|deck stand|card easel', tl): return 'stand'
    if ty in ('Bag', 'Bags & Pouches') and not re.search(r'paper carry', tl): return 'bag'
    if re.search(r'\b(pouch|bag)\b', tl) and re.search(r'tarot|velvet', tl) and ty not in ('books', 'Book', 'Tarot Deck', 'Oracle Cards', 'Oracle Deck', 'Sage'): return 'bag'
    if ty == 'Wood Storage Box' and not re.search(r'bowl', tl): return 'box'
    if ty in ('Tarot Talisman', 'Tarot Accessories'): return 'talisman'
    if ty in ('Journal', 'Journals'): return 'journal'
    if ty == 'Singing Bowl': return 'bowl'
    if ty in ('Hand Bells',): return 'bell'
    if ty == 'Sage': return 'sage'
    if ty in ('Smudge Sprays Fine Mists', 'Cleansing Water'): return 'mist'
    return None
SHELVES = [('reading-table', '/supplies/reading-table/', ('cloth', 'stand', 'talisman'), 'Reading table', 'Reading Cloths, Card Stands and Talismans',
            'What sits on the table during a session: a cloth for the spread, a stand to hold a card up, and a small talisman or two.'),
           ('deck-care', '/supplies/deck-care/', ('bag', 'box'), 'Deck care', 'Deck Bags, Pouches and Boxes',
            'Velvet and cotton pouches and carved wooden boxes for keeping a deck safe between readings.'),
           ('journals', '/supplies/journals/', ('journal',), 'Journals', 'Journals for Readings and Dreams',
            'Blank and guided journals for writing down a spread, a dream or what a reader told you while it is fresh.'),
           ('sound', '/supplies/sound/', ('bowl', 'bell'), 'Bowls & bells', 'Singing Bowls, Bells and Tingshas',
            'Metal singing bowls with strikers, hand bells and tingshas, often rung to open or close a meditation or a session.'),
           ('clearing', '/supplies/clearing/', ('sage', 'mist'), 'Clearing the room', 'Sage, Smudge Sprays and Cleansing Waters',
            'Bundles to burn, plus sprays and waters for rooms where smoke is not allowed.')]
def p_intro(x):
    k = x['kind']
    if k in ('bowl', 'bell'): return '<p class="pnote">Strike the rim lightly, or circle it slowly with the striker for a long tone. Want to see the rooms upstairs? Read about <a href="/healing-center/">Suite 1104</a>.</p>'
    if k in ('sage', 'mist'): return '<p class="pnote">Burn sage with a window open and a heat-safe dish under it. Sprays are the easy choice for apartments and offices.</p>'
    return '<p class="pnote">For your own reading table at home. To sit at ours, <a href="/reserve/">reserve a session</a>.</p>'
def supply_pages():
    return MS.build(SELECT, COLLECTIONS, STYLES, KINDS, SHELVES, '/supplies/', 'Reading Room Supplies: Cloths, Deck Boxes, Singing Bowls & Sage | Psychic Center of New York',
                    'Supplies for a reading space at home: reading cloths, card stands, deck bags and boxes, journals, singing bowls, bells, sage and cleansing sprays.',
                    'Supplies for a reading space',
                    '<p>For setting up a reading space of your own: cloths and card stands for the table, bags and boxes for your deck, journals, '
                    'singing bowls and bells, and sage and sprays for clearing a room.</p>', p_intro, crumb_label='Supplies',
                    feature_kinds=('cloth', 'box', 'bowl', 'bag'), feat_h='From each shelf',
                    note='Collect what you need in the cart, then pay in one go on the secure Namaste Bookshop checkout; the bookshop packs and mails it.',
                    search=('Search supplies', 'For example: velvet bag, singing bowl, white sage or tingsha.'))

LINES = {
 'rebecca-martinez': 'Clairaudient tarot in English or Spanish, paced to whatever you bring in.',
 'catherine-marks': 'A clairvoyant and medium who prefers the questions that are bigger than yes or no.',
 'anthony-fusco': 'Twenty-five years with the Voyager deck; business, relationships and timing.',
 'casey-deamoira': 'Thoth cards together with Hellenistic astrology, for the long path or this week.',
 'high-priestess-judith': 'La Gitana: tarot, astrology and mediumship, with love as her specialty.',
 'damon-stang': 'A master tarot reader and folk magic practitioner, reading professionally for more than 25 years.',
 'jennifer-shanteau': 'Certified hypnotherapist; past-life and higher-self sessions, plus a short energy cleansing.',
 'dainichi-lazuli': 'Tarot, Vedic astrology, runes, numerology and aura reading, billed in 15-minute blocks.',
 'mallika': 'Lenormand for the facts and tarot for the reasons, with a push toward action.',
 'alexander-d-santiago': 'Tarot, or Western and Vedic chart work with gemstone and flower-essence suggestions.',
 'andrea-dopewitchkira': 'Clairvoyant tarot and longer Witch Talk conversations.',
 'priya': 'Astrology and tarot from a third-generation astrologer known for Chiron work.',
 'tyler-t-mann-tarot': 'Tarot with a motivational coach\'s eye for the practical next move.',
 'sophia-strange': 'Psychic medium and poet; you leave with a poem written from your spread.',
 'brinly-erin': 'Clairvoyant and clairaudient, centered on self-worth and inner strength.',
 'lizanne': 'Intuitive medium who opens with your question and works with art cards.',
 'lu-camy': 'Oracle readings with her own Soul Synergy deck, and clinical hypnosis.',
 'mychal-a-bryan': 'Hour-long Qabalistic tarot or traditional astrology, read remotely.',
}
WHERE = {'upstairs': 'Usually reads in the Suite 1104 rooms upstairs.', 'bookshop': 'Usually reads at the ground-floor tables.', 'remote': 'Currently reads remotely.', 'both': 'Works upstairs some days and downstairs on others.'}
ORDER = UP + ['lu-camy'] + DOWN + ['mychal-a-bryan']

def shell(pg):
    nav = ''.join(f'<a href="{h}"' + (' aria-current="page"' if pg['path'].startswith(h) else '') + f'>{t}</a>' for h, t in NAV)
    return (f'<body><a class="skip" href="#main">Skip to content</a><header class="h"><div class="hi"><a class="brand" href="/"><span class="b1">Psychic Center</span><span class="b2">of New York</span></a>'
            f'<span class="hr"><a class="hb" href="/reserve/">Reserve a session</a>{G.cart_button()}</span></div><nav class="n" aria-label="Main">{nav}</nav></header><main id="main">{pg["body"]}</main>'
            f'<footer class="f"><div class="fi"><div><p class="fb">Psychic Center of New York</p><p>Ground floor: inside Namaste Bookshop, {G.ADDR}<br>Upstairs: 80 Fifth Avenue, Suite 1104</p></div>'
            f'<div><p><a href="tel:{G.TEL}">{G.PHONE}</a><br><a href="mailto:{G.EMAIL}">{G.EMAIL}</a></p><p>Operated by Wealth Edge Ventures Inc. <a href="/about/">About</a> &middot; <a href="/privacy/">Privacy</a></p></div></div></footer></body></html>')

def names(ks): return ', '.join(f'<a href="/readers/{k}/">{R[k]["name"]}</a>' for k in ks)
def tile(k):
    r = R[k]
    return (f'<li><a href="/readers/{k}/"><img src="{E(G.headshot(k, 200))}" alt="" width="64" height="64" loading="lazy"><span><b>{E(r["name"])}</b>{E(LINES[k])}<em>from ${r["from"]}</em></span></a></li>')

def reader_pages():
    for k in ORDER:
        r = R[k]; first = r['name'].split()[0]
        floor = {'upstairs': ('Suite 1104, 11th floor', '/healing-center/'), 'bookshop': ('Ground-floor tables', '/bookshop-floor/'), 'remote': ('Remote sessions', '/sessions/'), 'both': ('Both floors', '/visit/')}[r['home']]
        body = (f'<section class="pg"><p class="ov">Reader &middot; {floor[0]}</p><div class="rp"><img src="{E(G.headshot(k, 480))}" alt="{E(r["name"])}" width="200" height="200">'
                f'<div><h1>{E(r["name"])}</h1><p class="dek">{E(LINES[k])}</p><p>{WHERE[r["home"]]} <a href="{floor[1]}">About this space</a>.</p></div></div>'
                f'<h2>Sessions and prices</h2>{G.services_list(k, "dl")}'
                + (f'<p>{first} also takes phone sessions; choose the phone option when you reserve.</p>' if r['phone'] else '')
                + f'<p><a class="btn" href="{E(r["book"])}" rel="nofollow noopener">Reserve with {E(first)}</a></p>'
                f'<p class="sm">Reserving opens {E(first)}\'s Square scheduling page, where you see live open times and pay to confirm. Need help? Call {G.PHONE}.</p>'
                f'<p class="sm">Profile details come from the reader\'s own listing.</p><p><a href="/readers/">All readers</a></p></section>')
        G.add(f'/readers/{k}/', f'{r["name"]} | Readers at Psychic Center of New York',
              f'{r["name"]} at Psychic Center of New York: {LINES[k]} Sessions from ${r["from"]}.', body,
              ld=[G.person_ld(k, f'/readers/{k}/')], crumbs=[('Home', '/'), ('Readers', '/readers/'), (r['name'], f'/readers/{k}/')])

def pages():
    supply_pages()
    reader_pages()
    home = (f'<section class="hero"><p class="ov">Fifth Avenue &amp; 14th Street &middot; Manhattan</p><h1>Readings on two floors of one Manhattan building</h1>'
            f'<p class="dek">Psychic Center of New York offers tarot, psychic, mediumship and astrology readings, plus hypnotherapy, in two spaces: open reading tables on the ground floor inside Namaste Bookshop, and three private rooms upstairs in Suite 1104.</p>'
            f'<p><a class="btn" href="/reserve/">Reserve a session</a> <a class="lnk" href="/readers/">Meet the readers</a></p></section>'
            f'<section class="board" aria-label="Building directory"><h2>Directory</h2><table><tbody>'
            f'<tr><th>11</th><td><b>Suite 1104</b> &middot; private rooms<br><span>Windowed room &middot; second room &middot; third room. Readings, mediumship, hypnotherapy.</span></td><td><a href="/healing-center/">Details</a></td></tr>'
            f'<tr><th>G</th><td><b>Ground-floor tables</b> &middot; inside Namaste Bookshop<br><span>Main table at the back of the sales floor &middot; window table at the front.</span></td><td><a href="/bookshop-floor/">Details</a></td></tr>'
            f'</tbody></table></section>'
            f'<section class="cols"><div><h2>Downstairs or upstairs?</h2><p>The ground-floor tables have the bustle of a busy shop around you. The upstairs rooms have doors that close. Each reader has a usual space, and your confirmation says where to go.</p></div>'
            f'<div><h2>What we offer</h2><p>Tarot, psychic and mediumship readings, astrology, oracle and Lenormand, hypnotherapy and short energy-cleansing sessions. <a href="/sessions/">See all sessions</a>.</p></div>'
            f'<div><h2>Hours</h2><p>' + '<br>'.join(f'{d}: {h}' for d, h in G.HOURS) + f'</p><p><a href="/visit/">Plan a visit</a></p></div></section>'
            f'<section class="pg"><h2>Readers at the center</h2><ul class="tiles">' + ''.join(tile(k) for k in ORDER[:6]) + '</ul><p><a href="/readers/">All 18 readers</a></p></section>'
            f'<section class="pg sup"><h2>Take the room home with you</h2><p>Set up a reading space at home: reading cloths, card stands, deck boxes and journals, plus singing bowls, bells, sage and cleansing sprays.</p>'
            f'<p><a class="hb" href="/supplies/">Browse supplies</a></p></section>')
    G.add('/', 'Psychic Center of New York | Tarot, Psychic & Medium Readings, Union Square',
          'Psychic Center of New York: tarot, psychic, mediumship and astrology readings and hypnotherapy at Fifth Ave & 14th St, with ground-floor tables and private rooms in Suite 1104.', home,
          ld=[G.shop_ld()])
    rd = ('<section class="pg"><h1>Our readers</h1><p class="dek">Eighteen readers and practitioners work at the center. Open a profile for prices and to reserve a time.</p>'
          '<h2>Upstairs, Suite 1104</h2><ul class="tiles">' + ''.join(tile(k) for k in UP) + '</ul>'
          '<h2>Ground-floor tables</h2><ul class="tiles">' + ''.join(tile(k) for k in DOWN) + '</ul>'
          '<h2>Both floors, or remote</h2><ul class="tiles">' + tile('lu-camy') + tile('mychal-a-bryan') + '</ul></section>')
    G.add('/readers/', 'Readers & Practitioners | Psychic Center of New York',
          'The eighteen tarot readers, psychics, mediums, astrologers and hypnotherapists of Psychic Center of New York, grouped by the floor where they usually work.', rd,
          crumbs=[('Home', '/'), ('Readers', '/readers/')])
    rs = ('<section class="pg"><h1>Reserve a session</h1><ol class="rooms"><li><b>Pick a reader</b>Choose by style below, or by floor on the <a href="/readers/">readers page</a>.</li>'
          '<li><b>Open their profile</b>Prices for every session length are listed there.</li><li><b>Press Reserve</b>Their scheduling page shows live openings; pay to confirm.</li></ol>'
          '<h2>By kind of session</h2><dl class="faq">'
          f'<dt>Tarot</dt><dd>{names(["anthony-fusco", "casey-deamoira", "damon-stang", "tyler-t-mann-tarot", "mallika"])}</dd>'
          f'<dt>Psychic and clairvoyant</dt><dd>{names(["catherine-marks", "rebecca-martinez", "brinly-erin", "andrea-dopewitchkira"])}</dd>'
          f'<dt>Mediumship</dt><dd>{names(["lizanne", "sophia-strange", "high-priestess-judith"])}</dd>'
          f'<dt>Astrology</dt><dd>{names(["priya", "alexander-d-santiago", "dainichi-lazuli", "mychal-a-bryan"])}</dd>'
          f'<dt>Hypnotherapy and energy</dt><dd>{names(["jennifer-shanteau", "lu-camy"])}</dd></dl>'
          f'<p class="sm">Prefer to talk it through? Call {G.PHONE} and we will help you pick.</p></section>')
    G.add('/reserve/', 'Reserve a Reading or Session | Psychic Center of New York',
          'How to reserve a session at Psychic Center of New York: pick a reader by style or floor, check prices on their profile, and confirm a live opening.', rs,
          crumbs=[('Home', '/'), ('Reserve', '/reserve/')])
    bf = (f'<section class="pg"><p class="ov">Ground floor</p><h1>The ground-floor tables</h1><p class="dek">Our two downstairs tables sit inside Namaste Bookshop at {G.ADDR}, among the shelves of the shop.</p>'
          f'<div class="two"><article><h2>Main table</h2><p>At the back of the sales floor. It is the first table filled each day.</p></article>'
          f'<article><h2>Window table</h2><p>By the front window, used when more than one reader is working downstairs.</p></article></div>'
          f'<h2>Readers usually based downstairs</h2><p>{names(DOWN)}.</p><p class="sm">Usual tables can change on a given day. <a href="/readers/lu-camy/">Lu Camy</a> works both floors.</p>'
          f'<h2>Good to know</h2><ul><li>The shop is open to the public, so the floor can be lively, especially on weekends.</li><li>For more privacy, choose a reader who works in the upstairs rooms.</li></ul>'
          f'<p><a class="btn" href="/reserve/">Reserve a table session</a></p></section>')
    G.add('/bookshop-floor/', 'Ground-Floor Reading Tables at 2 W 14th St | Psychic Center of New York',
          'Psychic Center of New York\'s two ground-floor reading tables inside Namaste Bookshop, the main table and the window table, and the readers usually based there.', bf,
          crumbs=[('Home', '/'), ('Ground floor', '/bookshop-floor/')])
    hc = (f'<section class="pg"><p class="ov">11th floor &middot; Suite 1104</p><h1>The upstairs rooms</h1><p class="dek">80 Fifth Avenue, Suite 1104, New York, NY 10011. The same building as the ground-floor tables, with its own entrance at 80 Fifth Avenue, around the corner. The suite is also known as the Namaste Healing Center.</p>'
          f'<h2>The rooms</h2><ol class="rooms"><li><b>The windowed room</b>Natural light from the window.</li><li><b>The second room</b>A standard private session room.</li><li><b>The third room</b>Smaller, and it doubles as storage, but works fine for a reading.</li></ol>'
          f'<h2>Who works upstairs</h2><p>{names(UP)}. <a href="/readers/mychal-a-bryan/">Mychal A. Bryan</a> belongs to the upstairs team but currently reads remotely.</p>'
          f'<h2>Getting there</h2><p>Enter the building at 80 Fifth Avenue and go up to Suite 1104 on the 11th floor. If you are unsure where your session is, check your confirmation or call {G.PHONE}.</p>'
          f'<p class="sm">Sessions here are for wellbeing and reflection. For any health concern, see a licensed clinician.</p>'
          f'<p><a class="btn" href="/reserve/">Reserve an upstairs session</a></p></section>')
    G.add('/healing-center/', 'Private Reading Rooms, 80 Fifth Ave Suite 1104 | Psychic Center of New York',
          'The upstairs side of Psychic Center of New York: three private rooms on the 11th floor at 80 Fifth Avenue, Suite 1104, who works there, and how to find it.', hc,
          crumbs=[('Home', '/'), ('Suite 1104', '/healing-center/')])
    svc = [('Tarot readings', '15 to 60 minutes', 'From $35', ["anthony-fusco", "casey-deamoira", "damon-stang", "tyler-t-mann-tarot"]),
           ('Psychic and clairvoyant readings', '15 to 60 minutes', 'From $35', ["catherine-marks", "rebecca-martinez", "brinly-erin", "andrea-dopewitchkira"]),
           ('Mediumship', 'Varies by reader', 'From $35', ["lizanne", "sophia-strange", "high-priestess-judith", "catherine-marks"]),
           ('Astrology', '15 to 60 minutes', 'From $40 (some 1-hour sessions cost more)', ["priya", "casey-deamoira", "alexander-d-santiago", "dainichi-lazuli", "mychal-a-bryan"]),
           ('Oracle and Lenormand', '15 to 60 minutes', 'From $35', ["lu-camy", "mallika"]),
           ('Hypnotherapy and hypnosis', '60 to 75 minutes', '$175', ["jennifer-shanteau", "lu-camy"]),
           ('Energy cleansing', '15 minutes', '$44', ["jennifer-shanteau"])]
    sv = ('<section class="pg"><h1>Sessions at the center</h1><p class="dek">Each reader sets their own prices, and every profile lists them. The prices below are typical starting points.</p>'
          '<div class="tbl"><table><thead><tr><th>Session</th><th>Length</th><th>Price</th><th>Readers</th></tr></thead><tbody>'
          + ''.join(f'<tr><td data-l="Session"><b>{a}</b></td><td data-l="Length"><span>{b}</span></td><td data-l="Price"><span>{c}</span></td><td data-l="Readers"><span>{names(d)}</span></td></tr>' for a, b, c, d in svc) + '</tbody></table></div>'
          f'<h2>Remote sessions</h2><p>Some readers take phone sessions: {names([k for k in ORDER if R[k]["phone"]])}. Choose a phone session when you book.</p><p><a class="btn" href="/reserve/">Reserve a session</a></p></section>')
    G.add('/sessions/', 'Readings, Astrology & Hypnotherapy Sessions | Psychic Center of New York',
          'Sessions at Psychic Center of New York near Union Square: tarot, psychic, mediumship, astrology, oracle, hypnotherapy and energy cleansing, with typical lengths and prices.', sv,
          crumbs=[('Home', '/'), ('Sessions', '/sessions/')])
    se = (f'<section class="pg"><h1>Schedule and events</h1><h2>Who is working this week</h2><p>Readers set their own days, and schedules change often, so we do not print them here. '
          f'Each reader\'s Reserve button shows their live openings; start from the <a href="/readers/">readers page</a>.</p>'
          f'<h2>Events</h2><p>No events are listed right now. When the center announces a reading event, workshop or special day, it will appear on this page. '
          f'To ask about anything coming up, call {G.PHONE} or email {G.EMAIL}.</p></section>')
    G.add('/schedule-and-events/', 'Reader Schedule & Events | Psychic Center of New York',
          'How to see which Psychic Center of New York readers are working on a given day, and where events will be announced.', se,
          crumbs=[('Home', '/'), ('Schedule and events', '/schedule-and-events/')])
    vi = (f'<section class="pg"><h1>Plan your visit</h1><div class="two"><article><h2>Ground floor</h2><p>Inside Namaste Bookshop<br>{G.ADDR}</p></article><article><h2>Upstairs, 11th floor</h2><p>80 Fifth Avenue, Suite 1104<br>New York, NY 10011</p></article></div>'
          f'<h2>Opening hours</h2><table class="hrs"><tbody>' + ''.join(f'<tr><th>{d}</th><td>{h}</td></tr>' for d, h in G.HOURS) + '</tbody></table><p class="sm">Hours can change on public holidays. Upstairs sessions are by appointment only.</p>'
          f'<h2>Transit</h2><ul><li>Union Square station is the nearest big hub, a few minutes on foot to the east.</li><li>The Sixth Avenue station at 14th Street (PATH included) is about the same distance west.</li></ul>'
          f'<h2>Arriving for a session</h2><p>Your confirmation names the reader; their profile here says which floor they usually use. Upstairs sessions go straight to Suite 1104.</p>'
          f'<p><a class="btn" href="{G.DIRECTIONS}">Get directions</a> <a class="lnk" href="tel:{G.TEL}">{G.PHONE}</a></p></section>')
    G.add('/visit/', 'Visit: Address, Hours & Transit | Psychic Center of New York',
          'Find Psychic Center of New York: ground-floor tables at 2 W 14th St and private rooms at 80 Fifth Ave Suite 1104, opening hours, subway and check-in tips.', vi,
          crumbs=[('Home', '/'), ('Visit', '/visit/')])
    fq = [('Why are the ground-floor tables inside a bookshop?', 'Our downstairs tables are set up inside Namaste Bookshop, and the center and the shop have the same owner. The private rooms are upstairs in Suite 1104.'),
          ('Can I choose which room I sit in?', 'Rooms follow the reader. If you want a private room, book a reader who works upstairs.'),
          ('Are the rooms private?', 'The Suite 1104 rooms are closed rooms. The ground-floor tables are inside the open shop.'),
          ('Do you offer Reiki?', 'Short energy-cleansing sessions are offered now. Ask us about other energy work, because practitioner availability changes.'),
          ('Can someone come in with me?', 'Ask your reader when you book; it is up to them.')]
    G.add('/faq/', 'Questions About the Center | Psychic Center of New York',
          'Answers about Psychic Center of New York: the ground-floor tables, private rooms, choosing a room, energy work, and bringing a friend.',
          '<section class="pg"><h1>Questions about the center</h1><dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q, a in fq) + '</dl></section>',
          ld=[G.faq_ld(fq)], crumbs=[('Home', '/'), ('FAQ', '/faq/')])
    G.add('/about/', 'About Psychic Center of New York', 'Psychic Center of New York is a reading center at Fifth Avenue and 14th Street, operated by Wealth Edge Ventures Inc.',
          f'<section class="pg"><h1>About Psychic Center of New York</h1><p>Psychic Center of New York is a reading center with tables on the ground floor inside Namaste Bookshop, {G.ADDR}, and private rooms upstairs at 80 Fifth Avenue, Suite 1104. '
          f'It is operated by Wealth Edge Ventures Inc., which also owns Namaste Bookshop.</p><p>Reader profiles are based on each reader\'s own listing. We do not post reviews or ratings.</p>'
          f'<p><a href="tel:{G.TEL}">{G.PHONE}</a> &middot; <a href="mailto:{G.EMAIL}">{G.EMAIL}</a></p></section>', crumbs=[('Home', '/'), ('About', '/about/')])
    G.add('/privacy/', 'Privacy | Psychic Center of New York', 'Analytics and booking privacy on psychiccenterofnewyork.com.',
          '<section class="pg">' + G.privacy('psychiccenterofnewyork.com is an information and booking site. It has no sign-up and takes no payments itself.') + '</section>',
          crumbs=[('Home', '/'), ('Privacy', '/privacy/')])

NOTFOUND_DESC = 'Page not found on psychiccenterofnewyork.com.'
NOTFOUND = '<section class="pg"><h1>No such room</h1><p>This page is not in the building. Try the <a href="/">directory</a> or <a href="/visit/">visit info</a>.</p></section>'

CSS = """@media(max-width:640px){.tbl thead{display:none}.tbl table,.tbl tbody,.tbl tr,.tbl td{display:block;width:100%}.tbl tr{border-bottom:2px solid #e2ddd1;padding:6px 0}.tbl td{border:0;padding:3px 10px;display:grid;grid-template-columns:76px 1fr;gap:8px}.tbl td::before{content:attr(data-l);font-size:.8rem;color:#6b5a3a;font-weight:700;text-transform:uppercase;letter-spacing:.04em}}
.tiles{list-style:none;padding:0;display:grid;gap:10px}@media(min-width:700px){.tiles{grid-template-columns:1fr 1fr}}.tiles a{display:flex;gap:12px;background:#fff;padding:12px;text-decoration:none;color:var(--ink);border-left:4px solid var(--brass)}.tiles img{object-fit:cover;flex:none}.tiles span{display:flex;flex-direction:column}.tiles b{color:var(--navy);font-family:'Playfair Display',serif}.tiles em{font-style:normal;color:#8a6d3e;font-weight:700;font-size:.88rem}
.rp{display:grid;gap:16px}@media(min-width:640px){.rp{grid-template-columns:200px 1fr;align-items:center}}.rp img{width:200px;height:200px;object-fit:cover;border:4px solid var(--brass)}.rp h1{margin-top:0}
dl.svc{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;background:#fff;padding:14px;border-top:3px solid var(--navy)}dl.svc dt{font-weight:700;color:var(--navy)}dl.svc dd{margin:0}
:root{--navy:#14284b;--brass:#b08d57;--stone:#f2efe8;--ink:#1b2130;--accent:#14284b;--onaccent:#fff;--onink:#fff;--paper:#f2efe8;--soft:#e9e3d6;--body:Karla,system-ui,sans-serif;--display:'Playfair Display',Georgia,serif;--btnr:4px;--r:6px;--line:#d8d0bf;--muted:#5a5f6b;--focus:#b08d57}
.hr{display:flex;align-items:center;gap:14px}.sup .hb{display:inline-block;background:var(--navy);color:#fff;border:0;padding:12px 20px;text-decoration:none;font-weight:700;border-radius:4px}.cartbtn{position:relative;display:block;color:currentColor;width:28px;height:28px}.cartbtn svg{width:26px;height:26px}.cartn{position:absolute;top:-6px;right:-9px;background:var(--brass);color:#fff;border-radius:99px;font:700 .7rem sans-serif;padding:2px 6px}
*{box-sizing:border-box}body{margin:0;background:var(--stone);color:var(--ink);font:16.5px/1.65 Karla,system-ui,sans-serif}a{color:#1f4f8f}
h1,h2{font-family:'Playfair Display',Georgia,serif;line-height:1.15;color:var(--navy)}h1{font-size:clamp(2rem,7vw,3.1rem);font-weight:800;margin:.2em 0 .35em}
.skip{position:absolute;left:-999px}.skip:focus{left:6px;top:6px;background:#fff;padding:6px}
.h{background:var(--navy);color:#fff;border-bottom:4px solid var(--brass)}.hi{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;max-width:1080px;margin:0 auto}
.brand{text-decoration:none;color:#fff;line-height:1}.b1{display:block;font:800 1.35rem 'Playfair Display',serif}.b2{display:block;font:600 .78rem Karla,sans-serif;letter-spacing:.32em;text-transform:uppercase;color:var(--brass);margin-top:3px}
.hb{border:1.5px solid var(--brass);color:#fff;text-decoration:none;padding:8px 12px;font-weight:700;font-size:.88rem}
.n{display:flex;gap:2px;overflow-x:auto;max-width:1080px;margin:0 auto;padding:0 10px 8px;scrollbar-width:none}.n a{color:#d6dcea;text-decoration:none;padding:6px 10px;white-space:nowrap;font-weight:600;font-size:.9rem}
.n a[aria-current]{color:var(--brass)}
main{max-width:1080px;margin:0 auto;padding:0 16px 30px}.ov{text-transform:uppercase;letter-spacing:.2em;font-size:.72rem;font-weight:700;color:#7a5f33;margin:0}.dek{font-size:1.12rem;max-width:720px}
.hero{padding:30px 0 10px}
.board{background:#0d1b33;color:#e9e2d2;padding:16px;border-radius:4px;border:6px solid #2a3b5c;font-family:'Courier New',monospace}.board h2{color:var(--brass);font-family:'Courier New',monospace;letter-spacing:.3em;text-transform:uppercase;font-size:.95rem;margin:.2em 0 .6em}
.board table{width:100%;border-collapse:collapse}.board th{font-size:1.8rem;color:var(--brass);width:56px;vertical-align:top;text-align:left;padding:8px 4px}.board td{padding:8px 4px;border-top:1px dashed #3b4d70;vertical-align:top}.board span{color:#b9c2d6;font-size:.9rem}.board a{color:var(--brass)}
.cols{display:grid;gap:18px;margin-top:24px}@media(min-width:800px){.cols{grid-template-columns:repeat(3,1fr)}}.cols>div{background:#fff;padding:4px 16px 14px;border-top:3px solid var(--navy)}
.pg{max-width:820px;padding-top:16px}.two{display:grid;gap:12px}@media(min-width:640px){.two{grid-template-columns:1fr 1fr}}.two article{background:#fff;padding:2px 16px 10px;border-left:4px solid var(--brass)}
.rooms{padding-left:1.2em}.rooms li{margin:.5em 0}.rooms b{display:block;color:var(--navy)}.sm{font-size:.9rem;color:#4d5568}
.tbl{overflow-x:auto}.tbl table,.hrs{border-collapse:collapse;width:100%;background:#fff}.tbl th,.tbl td,.hrs th,.hrs td{padding:9px 10px;border-bottom:1px solid #e2ddd1;text-align:left;vertical-align:top}.tbl thead th{background:var(--navy);color:#fff}
.btn{display:inline-block;background:var(--navy);color:#fff;text-decoration:none;font-weight:700;padding:12px 18px;border-bottom:3px solid var(--brass)}.lnk{display:inline-block;padding:12px;font-weight:700}
.faq dt{font-weight:700;margin-top:1em;color:var(--navy)}.faq dd{margin:.2em 0 0}
.f{background:#0d1b33;color:#cdd4e3;margin-top:30px}.fi{max-width:1080px;margin:0 auto;padding:24px 16px;display:grid;gap:12px}@media(min-width:760px){.fi{grid-template-columns:1fr 1fr}}.f a{color:var(--brass)}.fb{font:800 1.2rem 'Playfair Display',serif;color:#fff;margin:0 0 .3em}
"""
