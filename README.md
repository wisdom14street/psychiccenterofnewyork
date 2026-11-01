# psychiccenterofnewyork.com

Psychic Center of New York: static site built by `scripts/build.py` and deployed to GitHub Pages by Actions. A Wealth Edge Ventures Inc. brand connected to Namaste Bookshop, 2 W 14th St, New York.

- `site/content.py`: this site's pages, layout, copy and CSS (all wording is unique to this site).
- `site/config.json`: brand, domain, GA4 ID (G-Y7R5K9NMW0, sends `site_brand`).
- `site/readers.json`: active Namaste readers (name, booking link, starting price) taken from namastebookshop.com.
- `scripts/engine.py`: page assembly, JSON-LD, sitemap.xml, robots.txt, llms.txt, 404.
- `static/`: og.jpg link preview, favicon and icons.
- Checkout (if the site sells): Shopify cart permalinks to namastebookshop.com tagged `attributes[Storefront]=psychiccenterofnewyork.com`; `data/` keeps the last good product fetch as a fallback.
