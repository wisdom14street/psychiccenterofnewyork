"""Download a site's Google Fonts (latin subset, woff2) into static/fonts/ and write static/fonts/fonts.css.
Usage: python3 scripts/selfhost_fonts.py  (run from the repo root). Reads FONTS from site/content.py."""
import re, os, urllib.request, hashlib
src = open('site/content.py').read()
url = re.search(r"^FONTS = '([^']+)'", src, re.M).group(1)
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
css = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30).read().decode()
os.makedirs('static/fonts', exist_ok=True)
for f in os.listdir('static/fonts'): os.remove(os.path.join('static/fonts', f))
out, seen, pre = [], {}, []
for sub, block in re.findall(r'/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]+})', css):
    if sub != 'latin': continue
    u = re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    if u not in seen:
        name = re.sub(r'[^a-z0-9]+', '-', fam.lower()) + '-' + hashlib.sha1(u.encode()).hexdigest()[:8] + '.woff2'
        open(f'static/fonts/{name}', 'wb').write(urllib.request.urlopen(u, timeout=30).read()); seen[u] = name
        if 'font-style: normal' in block and fam not in [p[0] for p in pre]: pre.append((fam, name))
    out.append(block.replace(u, '/fonts/' + seen[u]))
open('static/fonts/fonts.css', 'w').write('\n'.join(out) + '\n')
open('static/fonts/preload.txt', 'w').write('\n'.join(n for _, n in pre) + '\n')
print(url.split('?')[1][:60], 'files', len(seen), 'preload', [n for _, n in pre])
