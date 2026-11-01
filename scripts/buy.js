/* GA4 add_to_cart + begin_checkout when a Buy link (Shopify cart permalink) is tapped. Never blocks the link. */
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-buy]');if(!a)return;
try{if(typeof gtag!=='function')return;var d=a.dataset,it={item_id:String(d.v),item_name:d.t,price:+d.p||0,quantity:1};if(d.c)it.item_category=d.c;
var p={currency:'USD',value:it.price,items:[it]};gtag('event','add_to_cart',p);gtag('event','begin_checkout',Object.assign({transport_type:'beacon'},p))}catch(_){}});
