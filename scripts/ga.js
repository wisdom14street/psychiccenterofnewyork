/* Google Analytics 4 events for the storefronts. Every call is guarded: if gtag is blocked or missing, nothing breaks.
   view_item on product pages, booking_click / contact_click / bookshop_click measure navigation intent, never confirmed bookings or revenue.
   add_to_cart and begin_checkout are sent from cart.js. */
(function(){
  function ga(n,p){try{if(typeof window.gtag==='function')window.gtag('event',n,p||{})}catch(_){}}
  window.niGA=ga;
  try{
    if(/^\/products\//.test(location.pathname)){
      var b=document.getElementById('buy'),it=null;
      if(b&&b.dataset&&b.dataset.v){var d=b.dataset;it={item_id:String(d.v),item_name:d.t+(d.vt&&d.vt!=='Default Title'?' - '+d.vt:''),price:+d.p||0,quantity:1};if(d.c)it.item_category=d.c}
      else{[].forEach.call(document.querySelectorAll('script[type="application/ld+json"]'),function(s){if(it)return;try{var j=JSON.parse(s.textContent);(Array.isArray(j)?j:[j]).forEach(function(o){if(!it&&o&&o['@type']==='Product'){var of=Array.isArray(o.offers)?o.offers[0]:(o.offers||{});it={item_id:String(o.sku||location.pathname.split('/')[2]),item_name:o.name,price:+of.price||0,quantity:1}}})}catch(_){}})}
      if(it)ga('view_item',{currency:'USD',value:it.price,items:[it]});
    }
  }catch(_){}
  var MAPS=/(google\.[a-z.]+\/maps|maps\.google\.|goo\.gl\/maps|maps\.app\.goo\.gl|maps\.apple\.com)/i;
  function kind(a){
    var h=a.getAttribute('href')||'';
    if(/^tel:/i.test(h))return'phone';
    if(/^mailto:/i.test(h))return/^mailto:claim@/i.test(h)?'claim':'email';
    var u;try{u=new URL(h,location.href)}catch(_){return''}
    if(u.origin===location.origin&&/^\/claim(\/|$)/.test(u.pathname))return'claim';
    if(MAPS.test(u.href))return'directions';
    if(u.protocol!=='https:'&&u.protocol!=='http:')return'';
    // Match the destination, not words in query strings or unrelated link labels.
    if(u.hostname==='book.squareup.com'||(u.hostname==='squareup.com'&&u.pathname.indexOf('/appointments')===0))return'booking';
    if((u.hostname==='namastebookshop.com'||u.hostname==='www.namastebookshop.com')&&!/^\/cart(?:\/|$)/.test(u.pathname))return u.pathname==='/pages/book-a-reading'?'booking':'bookshop';
    return'';
  }
  document.addEventListener('click',function(e){try{
    var a=e.target&&e.target.closest&&e.target.closest('a[href]');if(!a)return;var k=kind(a);if(!k)return;
    var u=new URL(a.getAttribute('href'),location.href);
    ga(k==='booking'?'booking_click':k==='bookshop'?'bookshop_click':'contact_click',{link_type:k,measurement_stage:'click',link_url:(u.protocol==='https:'||u.protocol==='http:'?u.origin+u.pathname:u.protocol).slice(0,200),transport_type:'beacon'});
  }catch(_){}},true);
})();
