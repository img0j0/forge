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

# ---- icons: the pixel campfire, drawn cleanly at each size ----
G=[".........#........","........#Y#.......","........#Y#.......",".......#YY#.......","...#...#YYY#..#...","..#O#.#YYWY#.#O#..","..#O#.#YWWY#.#O#..",
   "..#OO#YYWWYY#OO#..","..#ROOYYWWYYOOR#..","..#ROOYYYYYYOOR#..","...#ROOOYYOOOR#...","...#RROOOOOORR#...","....#RRROORRR#....",".....##RRRR##.....",
   "...BBBBBBBBBBBB...","..BbbbbbbbbbbbbB..","...BBBBBBBBBBBB..."]
C={'#':(110,34,40),'Y':(255,214,90),'W':(255,246,207),'O':(255,138,46),'R':(229,68,30),'B':(70,46,30),'b':(122,84,52)}
def icon(S, frac):
    img=Image.new('RGB',(S,S)); d=ImageDraw.Draw(img)
    for y in range(S):
        t=y/S; d.line([(0,y),(S,y)],fill=(int(0x3A+(0x17-0x3A)*t),int(0x2C+(0x13-0x2C)*t),int(0x78+(0x36-0x78)*t)))
    px=max(1,int(S*frac/18)); w=18*px; h=len(G)*px; ox=(S-w)//2; oy=(S-h)//2
    glow=Image.new('RGB',(S,S)); gd=ImageDraw.Draw(glow); R=int(S*.43)
    for r in range(R,0,-max(1,S//90)):
        k=int(100*(1-r/R)**1.5); gd.ellipse([S/2-r,S/2+S*.1-r,S/2+r,S/2+S*.1+r],fill=(k,int(k*.55),int(k*.2)))
    img=ImageChops.add(img,glow); d=ImageDraw.Draw(img)
    for j,row in enumerate(G):
        for i,ch in enumerate(row):
            if ch!='.': d.rectangle([ox+i*px,oy+j*px,ox+i*px+px-1,oy+j*px+px-1],fill=C[ch])
    q=max(2,px//2)
    for (fx,fy,c) in [(.17,.12,(255,200,90)),(.78,.19,(255,150,70)),(.13,.39,(255,170,80)),(.83,.44,(255,200,90)),(.67,.08,(255,246,207))]:
        x=int(S*fx); y=int(S*fy); d.rectangle([x,y,x+q,y+q],fill=c)
    return img
icon(192,1.0).save(f'{OUT}/icon-192.png'); icon(512,1.0).save(f'{OUT}/icon-512.png')
icon(512,.72).save(f'{OUT}/icon-maskable-512.png'); icon(180,1.0).save(f'{OUT}/apple-touch-icon.png')

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

