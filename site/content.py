"""Psychic Center of New York: the physical side of Namaste's readings. The two reading spots on the Bookshop floor, the three rooms of the
Healing Center upstairs at 80 Fifth Ave Suite 1104, the services held there, the schedule, and how to visit."""
import json, os
import engine as G
E = G.E
BUSINESS_TYPE = 'LocalBusiness'
THEME_COLOR = '#14284b'
FONTS = 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;800&family=Karla:wght@400;600;700&display=swap'
ORG_DESC = 'Psychic Center of New York describes the reading spaces of Namaste Bookshop at 2 West 14th Street and the Namaste Healing Center upstairs at 80 Fifth Avenue, Suite 1104, in Manhattan.'
LLMS_NOTE = ('Psychic Center of New York is a Wealth Edge Ventures Inc. brand connected to Namaste Bookshop. It covers the physical spaces where Namaste readings and sessions take place: '
             'two reading spots in the Bookshop at 2 West 14th Street and three rooms in the Namaste Healing Center, 80 Fifth Avenue, 11th floor, Suite 1104 (same building). Bookings go through Namaste Bookshop.')
R = json.load(open(os.path.join(os.path.dirname(__file__), 'readers.json')))
UP = ['rebecca-martinez', 'catherine-marks', 'anthony-fusco', 'casey-deamoira', 'high-priestess-judith', 'damon-stang', 'jennifer-shanteau', 'dainichi-lazuli', 'mallika']
DOWN = ['alexander-d-santiago', 'andrea-dopewitchkira', 'priya', 'tyler-t-mann-tarot', 'sophia-strange', 'brinly-erin', 'lizanne']
NAV = [('/bookshop-floor/', 'Bookshop floor'), ('/healing-center/', 'Healing Center'), ('/sessions/', 'Sessions'), ('/schedule-and-events/', 'Schedule'), ('/visit/', 'Visit'), ('/faq/', 'FAQ')]
HC_LD = {'@context': 'https://schema.org', '@type': 'HealthAndBeautyBusiness', 'name': 'Namaste Healing Center', 'telephone': '+1-212-645-0141',
         'address': {'@type': 'PostalAddress', 'streetAddress': '80 Fifth Avenue, Suite 1104', 'addressLocality': 'New York', 'addressRegion': 'NY', 'postalCode': '10011', 'addressCountry': 'US'},
         'parentOrganization': {'@type': 'Organization', 'name': 'Namaste Bookshop', 'url': 'https://namastebookshop.com/'}, 'url': 'https://namastebookshop.com/pages/namaste-healing-center'}

def shell(pg):
    nav = ''.join(f'<a href="{h}"' + (' aria-current="page"' if pg['path'].startswith(h) else '') + f'>{t}</a>' for h, t in NAV)
    return (f'<body><a class="skip" href="#main">Skip to content</a><header class="h"><div class="hi"><a class="brand" href="/"><span class="b1">Psychic Center</span><span class="b2">of New York</span></a>'
            f'<a class="hb" href="{G.BOOK}">Reserve a session</a></div><nav class="n" aria-label="Main">{nav}</nav></header><main id="main">{pg["body"]}</main>'
            f'<footer class="f"><div class="fi"><div><p class="fb">Psychic Center of New York</p><p>Namaste Bookshop, {G.ADDR}<br>Healing Center upstairs, Suite 1104 at 80 Fifth Ave</p></div>'
            f'<div><p><a href="tel:{G.TEL}">{G.PHONE}</a><br><a href="mailto:{G.EMAIL}">{G.EMAIL}</a></p><p>A Wealth Edge Ventures Inc. brand, connected to Namaste Bookshop. <a href="/about/">About</a> &middot; <a href="/privacy/">Privacy</a></p></div></div></footer></body></html>')

def names(ks): return ', '.join(R[k]['name'] for k in ks)

def pages():
    home = (f'<section class="hero"><p class="ov">Union Square &middot; Fifth Avenue &amp; 14th Street</p><h1>Two floors of readings in one Manhattan building</h1>'
            f'<p class="dek">Psychic Center of New York is the guide to where Namaste readings actually happen: two reading spots on the ground floor of Namaste Bookshop, and three private rooms in the Namaste Healing Center on the 11th floor upstairs.</p></section>'
            f'<section class="board" aria-label="Building directory"><h2>Directory</h2><table><tbody>'
            f'<tr><th>11</th><td><b>Namaste Healing Center</b> &middot; Suite 1104<br><span>Windowed room &middot; second room &middot; third room. Private sessions, readings, hypnotherapy.</span></td><td><a href="/healing-center/">Details</a></td></tr>'
            f'<tr><th>G</th><td><b>Namaste Bookshop</b> &middot; 2 W 14th St<br><span>Main spot at the back of the sales floor &middot; Window spot at the front.</span></td><td><a href="/bookshop-floor/">Details</a></td></tr>'
            f'</tbody></table></section>'
            f'<section class="cols"><div><h2>Downstairs or upstairs?</h2><p>The shop floor has the bustle of the bookshop around you. The Healing Center rooms have doors that close. Each reader has a usual space, and your booking confirmation says where to go.</p></div>'
            f'<div><h2>What happens here</h2><p>Tarot, psychic and mediumship readings, astrology, oracle and Lenormand, hypnotherapy and short energy-cleansing sessions. <a href="/sessions/">See all sessions</a>.</p></div>'
            f'<div><h2>Hours</h2><p>' + '<br>'.join(f'{d}: {h}' for d, h in G.HOURS) + f'</p><p><a href="/visit/">Plan a visit</a></p></div></section>')
    G.add('/', 'Psychic Center of New York | Reading Rooms at Namaste, Union Square',
          'Where Namaste readings happen in Manhattan: two reading spots in Namaste Bookshop at 2 W 14th St and three private rooms at the Healing Center, 80 Fifth Ave Suite 1104.', home,
          ld=[G.shop_ld('LocalBusiness'), HC_LD])
    bf = (f'<section class="pg"><p class="ov">Ground floor</p><h1>The Bookshop floor</h1><p class="dek">Namaste Bookshop, {G.ADDR}. Readings on this floor happen inside the shop itself.</p>'
          f'<div class="two"><article><h2>Main spot</h2><p>The reading table at the back of the sales floor. It is the first spot the shop fills each day.</p></article>'
          f'<article><h2>Window spot</h2><p>A second table at the front, by the store window, used when more than one reader is working downstairs.</p></article></div>'
          f'<h2>Readers usually based downstairs</h2><p>{names(DOWN)}.</p><p class="sm">Usual spots can change on a given day. Lu Camy works both floors depending on the day.</p>'
          f'<h2>Good to know</h2><ul><li>The shop is open to the public, so the floor can be lively, especially on weekends.</li><li>If you want more privacy, ask for a reader who works in the Healing Center upstairs.</li></ul>'
          f'<p><a class="btn" href="{G.BOOK}">Book a reader</a></p></section>')
    G.add('/bookshop-floor/', 'Reading Spots Inside Namaste Bookshop, 2 W 14th St | Psychic Center of New York',
          'The two reading tables on the Namaste Bookshop sales floor, the main spot and the window spot, and which readers usually work downstairs.', bf,
          crumbs=[('Home', '/'), ('Bookshop floor', '/bookshop-floor/')])
    hc = (f'<section class="pg"><p class="ov">11th floor &middot; Suite 1104</p><h1>The Namaste Healing Center</h1><p class="dek">{G.HC_STREET}, New York, NY 10011. The same building as the bookshop, with its own entrance at 80 Fifth Avenue, around the corner from the shop door.</p>'
          f'<h2>The rooms</h2><ol class="rooms"><li><b>The windowed room</b>Natural light from the window.</li><li><b>The second room</b>A standard private session room.</li><li><b>The third room</b>Smaller, and it doubles as storage, but works fine for a reading.</li></ol>'
          f'<h2>Who works upstairs</h2><p>{names(UP)}. Mychal A. Bryan belongs to the Healing Center but currently reads remotely.</p>'
          f'<h2>Getting there</h2><p>Enter the building at 80 Fifth Avenue and go up to Suite 1104 on the 11th floor. If you are unsure where your session is, check your booking confirmation or call {G.PHONE}.</p>'
          f'<p class="sm">Sessions here are for wellbeing and reflection. For any health concern, see a licensed clinician.</p>'
          f'<p><a class="btn" href="{G.SHOP}/pages/namaste-healing-center">Healing Center page on namastebookshop.com</a></p></section>')
    G.add('/healing-center/', 'Namaste Healing Center, 80 Fifth Ave Suite 1104 | Psychic Center of New York',
          'The Namaste Healing Center on the 11th floor at 80 Fifth Avenue, Suite 1104: three private rooms for readings and sessions, who works there, and how to find it.', hc,
          ld=[HC_LD], crumbs=[('Home', '/'), ('Healing Center', '/healing-center/')])
    svc = [('Tarot readings', '15 to 60 minutes', 'from about $35', 'Most readers on both floors.'),
           ('Psychic and clairvoyant readings', '15 to 60 minutes', 'from about $35', 'Catherine Marks, Rebecca Martinez, Brinly Erin, Andrea.'),
           ('Mediumship', 'varies', 'from about $35', 'Lizanne, Sophia Strange, High Priestess Judith, Catherine Marks.'),
           ('Astrology', '15 to 60 minutes', 'from about $40; one-hour specialist sessions cost more', 'Priya, Casey Deamoira, Alexander D. Santiago, Dainichi Lazuli, Mychal A. Bryan.'),
           ('Oracle and Lenormand', '15 to 60 minutes', 'from about $35', 'Lu Camy (oracle), Mallika (Lenormand with tarot).'),
           ('Hypnotherapy and hypnosis', '60 to 75 minutes', 'about $175', 'Jennifer Shanteau, Lu Camy.'),
           ('Energy cleansing', '15 minutes', 'about $44', 'Jennifer Shanteau.')]
    sv = ('<section class="pg"><h1>Sessions held at the center</h1><p class="dek">Rates belong to the individual reader and appear at booking. The figures here are approximate starting points from their posted price lists.</p>'
          '<div class="tbl"><table><thead><tr><th>Session</th><th>Length</th><th>Price</th><th>With</th></tr></thead><tbody>'
          + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in svc) + '</tbody></table></div>'
          f'<p>Phone sessions are also available with some readers. <a href="{G.PHONE_PAGE}">See phone readings</a>.</p><p><a class="btn" href="{G.BOOK}">Reserve a session</a></p></section>')
    G.add('/sessions/', 'Readings, Astrology & Hypnotherapy Sessions | Psychic Center of New York',
          'Sessions offered in Namaste\'s reading spaces near Union Square: tarot, psychic, mediumship, astrology, oracle, hypnotherapy and energy cleansing, with typical lengths and prices.', sv,
          crumbs=[('Home', '/'), ('Sessions', '/sessions/')])
    se = (f'<section class="pg"><h1>Schedule and events</h1><h2>Who is working this week</h2><p>Readers set their own days. Namaste Bookshop keeps a live <a href="{G.CALENDAR}">reader calendar</a>, and every booking page shows real open times. '
          f'Schedules change often, so this site does not copy them.</p><h2>Events</h2><p>No events are listed here right now. When Namaste Bookshop announces a reading event, workshop or special day, it will be posted on namastebookshop.com first. '
          f'To ask about anything coming up, call {G.PHONE} or email {G.EMAIL}.</p><p><a class="btn" href="{G.CALENDAR}">Open the reader calendar</a></p></section>')
    G.add('/schedule-and-events/', 'Reader Schedule & Events | Psychic Center of New York',
          'Where to find who is reading at Namaste Bookshop and the Healing Center each day, and how events are announced.', se,
          crumbs=[('Home', '/'), ('Schedule and events', '/schedule-and-events/')])
    vi = (f'<section class="pg"><h1>Plan your visit</h1><div class="two"><article><h2>Bookshop (ground floor)</h2><p>{G.ADDR}</p></article><article><h2>Healing Center (11th floor)</h2><p>{G.HC_STREET}<br>New York, NY 10011</p></article></div>'
          f'<h2>Opening hours</h2><table class="hrs"><tbody>' + ''.join(f'<tr><th>{d}</th><td>{h}</td></tr>' for d, h in G.HOURS) + '</tbody></table><p class="sm">Hours can change on public holidays. Upstairs sessions are by appointment only.</p>'
          f'<h2>Transit</h2><ul><li>Union Square station is the nearest big hub, a few minutes on foot to the east.</li><li>The Sixth Avenue station at 14th Street (PATH included) is about the same distance west.</li></ul>'
          f'<h2>Arriving for a session</h2><p>Come five minutes early. Downstairs, tell a staff member you have a booking. Upstairs, go straight to Suite 1104.</p>'
          f'<p><a class="btn" href="{G.DIRECTIONS}">Get directions</a> <a class="lnk" href="tel:{G.TEL}">{G.PHONE}</a></p></section>')
    G.add('/visit/', 'Visit: Address, Hours & Transit | Psychic Center of New York',
          'Addresses for Namaste Bookshop (2 W 14th St) and the Namaste Healing Center (80 Fifth Ave Suite 1104), opening hours, subway lines and check-in tips.', vi,
          crumbs=[('Home', '/'), ('Visit', '/visit/')])
    fq = [('Is Psychic Center of New York a separate business?', 'No. It is a guide to the reading spaces of Namaste Bookshop and its Healing Center, both run by the same owners.'),
          ('Can I choose which room I sit in?', 'Rooms follow the reader. If you want a private room, book a reader who works upstairs.'),
          ('Are the rooms private?', 'The Healing Center rooms are closed rooms. The Bookshop spots are inside the open shop.'),
          ('Do you offer Reiki?', 'Short energy-cleansing sessions are offered now. Ask the shop about other energy work, because practitioner availability changes.'),
          ('Can someone come in with me?', 'Ask your reader when you book; it is up to them.')]
    G.add('/faq/', 'Questions About the Reading Rooms | Psychic Center of New York',
          'Answers about Namaste\'s reading spaces: privacy, choosing a room, energy work, and bringing a friend.',
          '<section class="pg"><h1>Questions about the center</h1><dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q, a in fq) + '</dl></section>',
          ld=[G.faq_ld(fq)], crumbs=[('Home', '/'), ('FAQ', '/faq/')])
    G.add('/about/', 'About Psychic Center of New York', 'Psychic Center of New York is a Wealth Edge Ventures Inc. guide to the reading spaces of Namaste Bookshop.',
          f'<section class="pg"><h1>About this site</h1><p>Wealth Edge Ventures Inc., owner of both Namaste Bookshop and the Namaste Healing Center, publishes this site. '
          f'It describes the spaces, sessions and practical details of visiting. All bookings are handled by Namaste Bookshop.</p><p>Reader information comes from namastebookshop.com and from the shop itself. We do not post reviews or ratings here.</p>'
          f'<p><a href="tel:{G.TEL}">{G.PHONE}</a> &middot; <a href="mailto:{G.EMAIL}">{G.EMAIL}</a></p></section>', crumbs=[('Home', '/'), ('About', '/about/')])
    G.add('/privacy/', 'Privacy | Psychic Center of New York', 'Analytics and booking privacy on psychiccenterofnewyork.com.',
          '<section class="pg">' + G.privacy('psychiccenterofnewyork.com is an information site about a physical place. It has no sign-up and takes no payments.') + '</section>',
          crumbs=[('Home', '/'), ('Privacy', '/privacy/')])

NOTFOUND_DESC = 'Page not found on psychiccenterofnewyork.com.'
NOTFOUND = '<section class="pg"><h1>No such room</h1><p>This page is not in the building. Try the <a href="/">directory</a> or <a href="/visit/">visit info</a>.</p></section>'

CSS = """:root{--navy:#14284b;--brass:#b08d57;--stone:#f2efe8;--ink:#1b2130}
*{box-sizing:border-box}body{margin:0;background:var(--stone);color:var(--ink);font:16.5px/1.65 Karla,system-ui,sans-serif}a{color:#1f4f8f}
h1,h2{font-family:'Playfair Display',Georgia,serif;line-height:1.15;color:var(--navy)}h1{font-size:clamp(2rem,7vw,3.1rem);font-weight:800;margin:.2em 0 .35em}
.skip{position:absolute;left:-999px}.skip:focus{left:6px;top:6px;background:#fff;padding:6px}
.h{background:var(--navy);color:#fff;border-bottom:4px solid var(--brass)}.hi{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;max-width:1080px;margin:0 auto}
.brand{text-decoration:none;color:#fff;line-height:1}.b1{display:block;font:800 1.35rem 'Playfair Display',serif}.b2{display:block;font:600 .78rem Karla,sans-serif;letter-spacing:.32em;text-transform:uppercase;color:var(--brass);margin-top:3px}
.hb{border:1.5px solid var(--brass);color:#fff;text-decoration:none;padding:8px 12px;font-weight:700;font-size:.88rem}
.n{display:flex;gap:2px;overflow-x:auto;max-width:1080px;margin:0 auto;padding:0 10px 8px;scrollbar-width:none}.n a{color:#d6dcea;text-decoration:none;padding:6px 10px;white-space:nowrap;font-weight:600;font-size:.9rem}
.n a[aria-current]{color:var(--brass)}
main{max-width:1080px;margin:0 auto;padding:0 16px 30px}.ov{text-transform:uppercase;letter-spacing:.2em;font-size:.72rem;font-weight:700;color:#8a6d3e;margin:0}.dek{font-size:1.12rem;max-width:720px}
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
