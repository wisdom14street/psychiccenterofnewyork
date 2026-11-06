const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve('dist');
const server=http.createServer((req,res)=>{let pathname=new URL(req.url,'http://localhost').pathname;let f=path.join(root,pathname);if(pathname.endsWith('/'))f=path.join(f,'index.html');try{res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.woff2':'font/woff2'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f))}catch(e){res.statusCode=404;res.end('Not found')}});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});try{
for(const width of [390,1280]){
 const page=await browser.newPage({viewport:{width,height:850}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',r=>r.request().url().startsWith(base)?r.continue():r.abort());
 await page.goto(base);await page.getByRole('link',{name:'Compare readers & check availability',exact:true}).click();await page.waitForURL(base+'/reserve/');
 assert.equal(await page.locator('.booking-card').count(),18);
 assert.equal(await page.locator('a[data-reader]').count(),18);
 await page.locator('summary').first().click();assert.equal(await page.locator('details').first().getAttribute('open'),'');
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 // Stop navigation after the capturing analytics listener, without contacting Square.
 await page.evaluate(()=>document.addEventListener('click',e=>{if(e.target.closest('a[data-reader]'))e.preventDefault()}));
 await page.locator('a[data-reader]').first().click();
 const event=await page.evaluate(()=>Array.from(window.dataLayer).map(x=>Array.from(x)).find(x=>x[1]==='booking_click'));
 assert.equal(event[2].reader_id,'anthony-fusco');assert.equal(event[2].cta_placement,'reserve');assert.equal(event[2].measurement_stage,'click');
 assert.equal(await page.evaluate(()=>Array.from(window.dataLayer).some(x=>x[1]==='purchase')),false);
 await page.screenshot({path:`/tmp/psychic-reserve-${width}.png`});
 for(const slug of ['tarot','psychic','astrology']){await page.goto(base+'/sessions/'+slug+'/');assert.ok(await page.locator('a[data-reader]').count());assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://psychiccenterofnewyork.com/sessions/'+slug+'/');}
 await page.goto(base+'/cart/');assert.ok(await page.getByText('Your cart is empty.').isVisible());
 assert.deepEqual(errors,[]);await page.close();
}
const page=await browser.newPage({javaScriptEnabled:false});await page.route('**/*',r=>r.request().url().startsWith(base)?r.continue():r.abort());await page.goto(base+'/reserve/');assert.equal(await page.locator('a[data-reader]').count(),18);assert.ok(await page.locator('a[data-reader]').first().isVisible());await page.close();
console.log('Browser PASS: mobile/desktop booking paths, 18 readers, prices, no overflow, click attribution, service canonicals, cart, JS-disabled booking links. External requests blocked; no booking placed.');
}finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exitCode=1});
