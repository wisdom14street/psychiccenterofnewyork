const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('scripts/ga.js', 'utf8');
// Fake DOM: like a browser, document keeps EVERY listener per event type and dispatches them in registration order.
function anchor(href, text) {
  const attrs = { href }, dataset = {};
  const a = { tagName: 'A', textContent: text, dataset,
    getAttribute: n => (Object.prototype.hasOwnProperty.call(attrs, n) ? attrs[n] : null),
    setAttribute: (n, v) => { attrs[n] = String(v); if (n.startsWith('data-')) dataset[n.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = String(v); },
    hasAttribute: n => Object.prototype.hasOwnProperty.call(attrs, n),
    closest: sel => (sel === 'a[href]' && attrs.href != null ? a : null) };
  return a;
}
function setup(gtag) {
  const listeners = {}; const events=[];
  const add = (n, f) => { (listeners[n] = listeners[n] || []).push(f); };
  const dispatch = (type, target, extra) => { const ev = { type, target, button: 0, defaultPrevented: false, preventDefault() { this.defaultPrevented = true; }, ...extra }; (listeners[type] || []).slice().forEach(f => f(ev)); return ev; };
  const context={URL, location:{href:'https://psychiccenterofnewyork.com/readers/',origin:'https://psychiccenterofnewyork.com',pathname:'/readers/',hostname:'psychiccenterofnewyork.com'},window:gtag===false?{}:{gtag:(...e)=>events.push(e)},document:{addEventListener:add}};
  vm.runInNewContext(source, context);
  return {events, listeners, dispatch,
    click(href,text='Reserve') {const a=anchor(href,text);dispatch('click',a);return a;},
    // Real pointer activation order: pointerdown -> mousedown -> click.
    press(href,text='Reserve') {const a=anchor(href,text);for(const t of ['pointerdown','mousedown','click'])dispatch(t,a);return a;}};
}
const s=setup();
s.click('https://book.squareup.com/appointments/123?email=private@example.com#private');
assert.equal(s.events[0][1],'booking_click');
assert.equal(s.events[0][2].link_url,'https://book.squareup.com/appointments/123');
assert.equal(s.events[0][2].measurement_stage,'click');
s.click('https://namastebookshop.com/pages/alexander-d-santiago');
assert.equal(s.events[1][1],'bookshop_click');
s.click('mailto:info@namastebookshop.com?body=private');
assert.equal(s.events[2][1],'contact_click');assert.equal(s.events[2][2].link_url,'mailto:');
for(const href of ['/readers/','https://example.com/?next=book.squareup.com','https://book.squareup.com.example.com/','https://namastebookshop.com/cart/123:1?attributes%5BStorefront%5D=test'])s.click(href,'Book now');
assert.equal(s.events.length,3);
assert.ok(s.events.every(e=>e[1]!=='purchase'&&e[1]!=='generate_lead'));
assert.doesNotThrow(()=>setup(false).click('https://book.squareup.com/appointments/123'));
console.log('Analytics regression checks passed');
// Fixture fidelity (unconditional): the existing click handler is still registered and runs even if other listeners exist.
assert.ok((s.listeners.click || []).length >= 1);
// NAM-SISTERS-002 Namaste Square attribution: checked only when that block is present in scripts/ga.js.
if (source.includes('__nsReadingAttrV1')) {
  const n = setup();
  const SQ = 'https://book.squareup.com/appointments/zwx2eltnh5vis3/location/LR25QQSXE9C2Q/services/CPQQWF7TW3OQHCV5ERJVPGA4';
  const a = n.press(SQ + '?email=private@example.com#private');
  assert.equal(a.getAttribute('href'), SQ + '?email=private@example.com&utm_source=psychiccenterofnewyork.com&utm_medium=referral&utm_campaign=namaste_readings#private');
  assert.equal(n.events.length, 1);
  assert.equal(n.events[0][1], 'booking_click');
  assert.equal(n.events[0][2].link_url, SQ);                      // event keeps path only; query is in the href, not in the event
  assert.ok(!/[?#]|email|example|utm_/.test(JSON.stringify(n.events[0][2])));
  assert.ok(n.events.every(e => e[1] !== 'reading_book_click'), 'no duplicate booking event on this site');
  n.press(SQ + '?email=private@example.com#private');               // idempotent per link
  const b = n.press(SQ + '?utm_source=gbp');
  assert.equal(b.getAttribute('href'), SQ + '?utm_source=gbp&utm_medium=referral&utm_campaign=namaste_readings');
  for (const other of ['https://book.squareup.com/appointments/123?email=private@example.com#private',
                       'https://book.squareup.com/appointments/abc123def456gh/location/LOTHERBIZ0001/services/X',
                       'http://book.squareup.com/appointments/zwx2eltnh5vis3/location/LR25QQSXE9C2Q/services/X',
                       'https://namastebookshop.com/cart/123:1?attributes%5BStorefront%5D=test'])
    assert.equal(n.press(other).getAttribute('href'), other);
  const r = setup(); const ctx = r.dispatch('contextmenu', anchor(SQ, 'Reserve'));
  assert.equal(ctx.target.getAttribute('href'), SQ + '?utm_source=psychiccenterofnewyork.com&utm_medium=referral&utm_campaign=namaste_readings');
  assert.equal(ctx.defaultPrevented, false);
  console.log('Namaste Square UTM tagging checks passed');
}
// Exercise the existing checkout builder without network calls or purchases.
const basket=[{v:'111',h:'one',t:'One',p:10,q:2},{v:'222',h:'two',t:'Two',p:20,q:1}];
const ctx={window:{NI_CART:{shop:'https://namastebookshop.com',attr:'?attributes%5BStorefront%5D=psychiccenterofnewyork.com',domain:'psychiccenterofnewyork.com',brand:'Psychic Center of New York',ref:'psychiccenterofnewyork'},addEventListener(){}},document:{querySelector:()=>null,querySelectorAll:()=>[],addEventListener(){}},localStorage:{getItem:()=>JSON.stringify(basket)}};
vm.runInNewContext(fs.readFileSync('scripts/cart.js','utf8'),ctx);
const checkout=new URL(ctx.window.NI_CART_URL());
assert.equal(checkout.origin,'https://namastebookshop.com');
assert.equal(checkout.pathname,'/cart/111:2,222:1');
assert.equal(checkout.searchParams.get('attributes[Storefront]'),'psychiccenterofnewyork.com');
assert.equal(checkout.searchParams.get('attributes[Site]'),'psychiccenterofnewyork.com');
assert.equal(checkout.searchParams.get('ref'),'psychiccenterofnewyork');
assert.match(checkout.searchParams.get('note'),/Psychic Center of New York/);
console.log('Multi-item checkout and source attributes preserved');
