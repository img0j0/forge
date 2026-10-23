/* Forge offline helper, version 0.38.0 */
const V='forge-0.38.0';
const ASSETS=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./icon-maskable-512.png','./apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);if(u.origin!==location.origin)return;
  /* Only the app page itself is cached as the app. Other pages (privacy, terms, support) load normally. */
  const appPage=/\/(index\.html)?$/.test(u.pathname);
  if(r.mode==='navigate'&&!appPage){e.respondWith(fetch(r).catch(()=>caches.match(r)));return;}
  if(r.mode==='navigate'){
    e.respondWith(Promise.race([fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(V).then(c=>c.put('./index.html',cp));}return res;}),
      new Promise((_,no)=>setTimeout(()=>no(new Error('slow')),4000))]).catch(()=>caches.match('./index.html').then(m=>m||fetch(r))));
    return;
  }
  e.respondWith(caches.match(r).then(m=>m||fetch(r)));
});
