from pathlib import Path
from html.parser import HTMLParser
import json
import xml.etree.ElementTree as ET
root=Path('dist'); errors=[]; pages=list(root.rglob('*.html'))
class Page(HTMLParser):
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href','').startswith('/'):
            path=a['href'].split('?')[0].split('#')[0]; target=root/path.lstrip('/')
            if path.endswith('/'): target=target/'index.html'
            if not target.exists(): errors.append((str(self.file),path))
for f in pages:
    p=Page(); p.file=f; p.feed(f.read_text())
readers=json.loads(Path('site/readers.json').read_text())
for k,r in readers.items():
    text=(root/'readers'/k/'index.html').read_text()
    assert r['book'] in text and r['profile'] in text,k
assert not errors,errors[:10]
urls=[e.text for e in ET.parse(root/'sitemap.xml').findall('.//{*}loc')]
assert all(u.startswith('https://psychiccenterofnewyork.com/') for u in urls)
assert not any(any(p in u for p in ('/cart/','/search/','/404.html')) for u in urls)
assert 'Buying something' in (root/'privacy/index.html').read_text()
assert 'data-cart-page' in (root/'cart/index.html').read_text()
assert 'noindex' in (root/'cart/index.html').read_text()
print(f'Passed: {len(pages)} HTML pages, local links, {len(readers)} reader booking/profile links, {len(urls)} sitemap URLs, cart privacy and page')
