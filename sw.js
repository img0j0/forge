/* Forge offline helper, version 0.39.0 */
const V='forge-0.39.0';
const ASSETS=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./icon-maskable-512.png','./apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>/^forge-[0-9]+\.[0-9]+\.[0-9]+$/.test(k)&&k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);if(u.origin!==location.origin)return;
  /* Only the app page itself is cached as the app. Other pages (privacy, terms, support) load normally. */
  const root=new URL('./',self.registration.scope);
  const appPage=u.pathname===root.pathname||u.pathname===new URL('index.html',root).pathname;
  if(r.mode==='navigate'&&!appPage){e.respondWith(fetch(r).catch(()=>caches.match(r)));return;}
  if(r.mode==='navigate'){
    const network=fetch(r).then(res=>{if(!res.ok)throw new Error('HTTP '+res.status);return res;});
    e.waitUntil(network.then(res=>{const cp=res.clone();return caches.open(V).then(c=>c.put('./index.html',cp));}).catch(()=>{}));
    let timer;
    const timeout=new Promise((_,no)=>{timer=setTimeout(()=>no(new Error('slow')),4000);});
    e.respondWith(Promise.race([network,timeout]).catch(()=>caches.match('./index.html').then(m=>{if(m)return m;return fetch(r);})).finally(()=>clearTimeout(timer)));
    return;
  }
  e.respondWith(caches.match(r).then(m=>m||fetch(r)));
});
