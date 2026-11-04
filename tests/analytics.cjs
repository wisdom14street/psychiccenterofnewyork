const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('scripts/ga.js', 'utf8');
function setup(gtag) {
  let click; const events=[];
  const context={URL, location:{href:'https://psychiccenterofnewyork.com/readers/',origin:'https://psychiccenterofnewyork.com',pathname:'/readers/'},window:gtag===false?{}:{gtag:(...e)=>events.push(e)},document:{addEventListener:(n,f)=>click=f}};
  vm.runInNewContext(source, context);
  return {events, click(href,text='Reserve') {const a={getAttribute:()=>href,textContent:text};click({target:{closest:()=>a}});}};
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
