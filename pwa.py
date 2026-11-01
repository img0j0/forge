# Packs work.html into an installable web app in ./pwa (for GitHub Pages or any static host).
import os, json, re, shutil
from PIL import Image, ImageDraw, ImageChops
OUT = 'pwa'; os.makedirs(OUT, exist_ok=True)
src = open('work.html', encoding='utf8').read()
ver = re.search(r"const VERSION='prototype ([0-9.]+)'", src).group(1)

# ---- the page: mark it as the release copy, link the manifest, plain title ----
src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="forge-build" content="release">\n<link rel="manifest" href="manifest.webmanifest">', 1)
src = re.sub(r'<title>Forgelings \(prototype [0-9.]+\)</title>', '<title>Forgelings</title>', src, count=1)
assert 'forge-build' in src and '<title>Forgelings</title>' in src
open(f'{OUT}/index.html', 'w', encoding='utf8').write(src)

# ---- icons: the seal mark (November 2026), rendered by art/make_icons.py from art/forgelings-icon.svg ----
import shutil
for _f in ('icon-192.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png'):
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),'art','out',_f), f'{OUT}/{_f}')

# ---- manifest ----
json.dump({"name":"Forgelings","short_name":"Forgelings","description":"One small thing a day. A small creature to keep it.",
  "start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#16132E","theme_color":"#16132E",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},
           {"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
  open(f'{OUT}/manifest.webmanifest','w'),indent=1)

# ---- offline helper: always try for the newest app, fall back to the saved copy when offline ----
open(f'{OUT}/sw.js','w').write("""/* Forge offline helper, version %s */
const V='forge-%s';
const ASSETS=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./icon-maskable-512.png','./apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>/^forge-[0-9]+\\.[0-9]+\\.[0-9]+$/.test(k)&&k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
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
""" % (ver, ver))
open(f'{OUT}/.nojekyll','w').write('')
open(f'{OUT}/README.md','w').write(f"# Forge\n\nOne small thing a day. A small creature to keep it.\n\nA cozy pixel-creature habit app. Prototype {ver}. Everything stays on your device.\n\nOpen it on your phone, then add it to your home screen.\n")
print('pwa built', ver, sorted(os.listdir(OUT)))

# ---- public pages (privacy, terms, support) for the site and App Store Connect ----
import glob as _g
for _f in _g.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legal', 'out', '*.html')):
    shutil.copy(_f, os.path.join(OUT, os.path.basename(_f)))

