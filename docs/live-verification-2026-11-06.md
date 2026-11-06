# Release verification — November 6, 2026

Published source commit: 9f950e10d371ad0c69bcc066c5605c39cca13d7e on main.
GitHub Pages workflow https://github.com/wisdom14street/psychiccenterofnewyork/actions/runs/42296814339 completed successfully. Both build and deploy jobs passed, including the new pre-deploy link, sitemap, booking and checkout-tracking checks.

Local real-Chromium tests passed at mobile and desktop sizes; see release-2026-11-06.md and tests/booking-browser.cjs. All 18 existing reader links are preserved. Sampled public Bookshop links for Alexander and Anthony resolve to their recorded Square booking URLs through web tools. No appointment or payment was submitted; availability selection and completed booking were not verified.

Post-deploy public fetches of https://psychiccenterofnewyork.com/, /reserve/, and /sessions/tarot/ all returned inaccessible via web tools. The execution environment restricts outbound access to this domain. No bypass was attempted. This is a live-rendering verification blocker, not proof of a site outage. Deployment success is verified; full live behavior and GA event delivery are not.

Search Console discovery returned only sc-domain:namastebookshop.com, not psychiccenterofnewyork.com. No sitemap submission was made to the wrong property. GA4 discovery returned connected:false because Analytics scope is absent; no traffic or conversion baseline could be retrieved. Site code retains its existing GA4 ID. Booking clicks do not establish confirmed appointments or revenue.

Remaining prerequisites for complete verification and measurable growth: authorized access to the live domain, this domain's verified Search Console property, Google Analytics reporting access, and Square confirmation/report access. No paid advertising, credential creation, purchase or booking was performed. Search indexing and increased traffic/bookings cannot be claimed from this release alone.
