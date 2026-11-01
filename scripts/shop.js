/* shelf sort/filter, product gallery, variant picker, sticky add bar, live stock check */
(function(){
  const $=(s,r)=>(r||document).querySelector(s),$$=(s,r)=>[...(r||document).querySelectorAll(s)];
  const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const money=v=>'$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
  const C=window.NI_CART||{};
  /* ---------- shelves ---------- */
  const form=$('form.tools[data-shelf]'),grid=$('[data-grid]'),more=$('[data-more]');
  const tf=$('[data-tf]');if(tf&&matchMedia('(min-width:700px)').matches)tf.open=true;
  if(form&&grid){
    let data=null,list=[],shown=0;const PER=48;const B={u20:[0,20],'20-35':[20,35],'35-50':[35,50],'50':[50,1e9]};
    const ph=x=>`<div class="noph" role="img" aria-label="${esc(x.n)}: photo coming soon"><span class="n1">${esc(x.n)}</span>${x.a?`<span class="n2">${esc(x.a)}</span>`:''}<em>Photo coming soon</em></div>`;
    const card=x=>{const u=`/products/${esc(x.h)}/`;
      const tags=(x.s?'':'<span class="tag sold">Sold out</span>')+(x.c&&x.s?'<span class="tag sale">Sale</span>':'')+(x.o?'<span class="tag oop">Out of print</span>':'');
      const img=x.i?`<img class="pi" src="${esc(x.i)}" srcset="${[160,240,360,480,640].map(n=>esc(x.i.replace(/width=\d+/,'width='+n))+' '+n+'w').join(', ')}" sizes="(min-width:1100px) 250px, (min-width:700px) 30vw, 46vw" alt="" width="300" height="300" loading="lazy" decoding="async">`:ph(x);
      const btn=!x.s?`<a class="qa ghost" href="${u}">Details</a>`:x.m?`<a class="qa" href="${u}">Choose</a>`:
        `<button type="button" class="qa" data-atc data-v="${x.v}" data-h="${esc(x.h)}" data-t="${esc(x.n)}" data-p="${Number(x.p).toFixed(2)}" data-i="${esc(x.i?x.i.replace(/width=300/,'width=400'):'/assets/no-photo.svg')}" data-c="${esc(form.dataset.shelf)}" data-k="${esc(x.k)}" aria-label="Add ${esc(x.n)} to cart">Add</button>`;
      return `<li class="pc${x.s?'':' out'}"><a class="pbox" href="${u}" tabindex="-1" aria-hidden="true">${img}${tags}</a><div class="pm"><a class="pn" href="${u}">${esc(x.n)}</a>${x.a?`<span class="pa">${esc(x.a)}</span>`:''}<span class="pp"><b>${money(x.p)}</b>${x.c?` <s aria-label="was">${money(x.c)}</s>`:''}</span></div>${btn}</li>`};
    const val=n=>{const el=$(`[data-f="${n}"]`,form);return el?(el.type==='checkbox'?(el.checked?'1':''):el.value):''};
    function apply(){
      const q=val('q').trim().toLowerCase(),k=val('k'),st=val('st'),pr=val('pr'),pb=val('pb'),s=val('s'),so=val('sort');
      list=data.filter(x=>(!q||(x.n+' '+(x.a||'')+' '+(x.pb||'')).toLowerCase().includes(q))&&(!k||x.k===k)&&(!st||x.st.includes(st))&&(!pb||x.pb===pb)&&(!s||x.s)&&(!pr||(x.p>=B[pr][0]&&x.p<B[pr][1])));
      const by={new:(a,b)=>(b.s-a.s)||(b.d>a.d?1:b.d<a.d?-1:0),lo:(a,b)=>(b.s-a.s)||a.p-b.p,hi:(a,b)=>(b.s-a.s)||b.p-a.p,az:(a,b)=>a.n.localeCompare(b.n)}[so]||((a,b)=>a.r-b.r);
      list.sort(by);shown=0;grid.innerHTML='';page();
      const pg=$('.pager');if(pg)pg.hidden=true;
      $('[data-count]',form).textContent=`${list.length} item${list.length===1?'':'s'} match`+(list.length?'':'. Try clearing a filter.');
    }
    function page(){grid.insertAdjacentHTML('beforeend',list.slice(shown,shown+PER).map(card).join(''));shown+=PER;if(more)more.hidden=shown>=list.length}
    const go=()=>{if(data)return apply();fetch(`/data/shelf/${form.dataset.shelf}.json`).then(r=>r.json()).then(d=>{data=d;apply()}).catch(()=>{})};
    let tq;form.addEventListener('change',go);form.addEventListener('input',e=>{if(e.target.type==='search'){clearTimeout(tq);tq=setTimeout(go,180)}});
    if(more)more.addEventListener('click',page);
  }
  /* ---------- site search ---------- */
  const sq=$('[data-sq]'),sg=$('[data-sgrid]');
  if(sq&&sg){let cat=null,t;const cnt=$('[data-scount]');
    const run=()=>{const q=sq.value.trim().toLowerCase();if(history.replaceState)history.replaceState(null,'',q?'?q='+encodeURIComponent(q):location.pathname);
      if(q.length<2){sg.innerHTML='';cnt.textContent='';return}
      const ws=q.split(/\s+/),r=cat.filter(x=>{const s=x.t.toLowerCase();return ws.every(w=>s.includes(w))}).sort((a,b)=>(a.x-b.x)||(a.r-b.r)).slice(0,96);
      cnt.textContent=r.length?`${r.length===96?'96+':r.length} result${r.length===1?'':'s'}`:'Nothing matched. Try fewer words.';
      sg.innerHTML=r.map(x=>{const u=`/products/${esc(x.h)}/`;return `<li class="pc${x.x?' out':''}"><a class="pbox" href="${u}" tabindex="-1" aria-hidden="true"><img class="pi" src="${esc(x.i)}" alt="" width="300" height="300" loading="lazy" decoding="async">${x.x?'<span class="tag sold">Sold out</span>':''}</a><div class="pm"><a class="pn" href="${u}">${esc(x.t)}</a><span class="pp"><b>${money(x.p)}</b></span></div>`+(x.x?`<a class="qa ghost" href="${u}">Details</a>`:`<a class="qa" href="${u}">View</a>`)+'</li>'}).join('')};
    const q0=new URLSearchParams(location.search).get('q');if(q0)sq.value=q0;
    fetch('/data/catalog.json').then(r=>r.json()).then(d=>{cat=d;run()}).catch(()=>{});
    sq.addEventListener('input',()=>{clearTimeout(t);t=setTimeout(()=>cat&&run(),150)})}
  /* ---------- product page ---------- */
  const gimg=$('#gimg');
  $$('.thumbs .th').forEach(b=>b.addEventListener('click',()=>{if(!gimg)return;gimg.src=b.dataset.src;gimg.srcset=[480,640,800,1100,1400].map(n=>b.dataset.src.replace(/width=\d+/,'width='+n)+' '+n+'w').join(', ');$$('.thumbs .th').forEach(t=>t.classList.toggle('on',t===b))}));
  const buy=$('#buy'),sel=$('[data-variant]');
  function setVar(id,p,c,ok){if(!buy)return;buy.dataset.v=id;buy.dataset.p=Number(p).toFixed(2);buy.disabled=!ok;buy.textContent=ok?'Add to cart':'Sold out';
    const bp=$('.bigp');if(bp)bp.innerHTML=`<b>${money(p)}</b>`+(c>p?` <s aria-label="was">${money(c)}</s>`:'');
    $$('[data-sbuy] [data-atc]').forEach(b=>{b.dataset.v=id;b.dataset.p=Number(p).toFixed(2)})}
  if(sel)sel.addEventListener('change',()=>{const o=sel.selectedOptions[0];setVar(o.value,+o.dataset.p,+o.dataset.c,!o.disabled)});
  const sb=$('[data-sbuy]');
  if(sb&&buy&&'IntersectionObserver' in window){sb.hidden=false;new IntersectionObserver(es=>es.forEach(e=>sb.classList.toggle('show',!e.isIntersecting&&e.boundingClientRect.top<0))).observe(buy)}
  const P=window.NI_PRODUCT;
  if(P&&C.shop&&buy)fetch(`${C.shop}/products/${encodeURIComponent(P.handle)}.js`).then(r=>r.ok?r.json():null).then(p=>{if(!p)return;
    const v=p.variants.find(v=>String(v.id)===String(buy.dataset.v))||p.variants.find(v=>v.available);if(!v)return;
    if(!sel)setVar(v.id,v.price/100,(v.compare_at_price||0)/100,v.available);
    if(!v.available&&!$('.soldnote')){buy.insertAdjacentHTML('afterend',`<p class="soldnote">Sold out online right now. Call <a href="tel:+12126450141">212-645-0141</a> to check the shelf.</p>`);if(sb)sb.remove()}
  }).catch(()=>{});
})();
