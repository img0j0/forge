# Composes App Store screenshots (1320 x 2868, iPhone 6.9-inch) from raw app captures.
# Usage: python3 compose.py RAW_DIR FONTS_CSS OUT_DIR
import sys, os, base64
from playwright.sync_api import sync_playwright
raw, fonts_css, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
fonts = open(fonts_css, encoding='utf8').read()
SLIDES = [
  ('1-today-light.png',  'One small thing a day',      'Do it, and a new Forgeling joins you.'),
  ('2-hearth-light.png', 'They keep you company',      'Sit by the fire, play, and send them wandering.'),
  ('3b-card-light.png',  'Each one is unique', 'Pixel creatures from ten realms, each its own.'),
  ('4-map-light.png',    'A map that draws itself',  'Wander, and the map fills in around you.'),
  ('5-shelf-light.png',  'Curios and old tales',       'Find all four from a realm and a lost story returns.'),
  ('6-games-light.png',  'Five games by the fire',     'Little rounds that grow your bond.'),
  (None,                 'Kind by design',             ''),
]
CAMP = ''.join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>' for y, row in enumerate([
 ".........#........","........#Y#.......","........#Y#.......",".......#YY#.......","...#...#YYY#..#...","..#O#.#YYWY#.#O#..","..#O#.#YWWY#.#O#..",
 "..#OO#YYWWYY#OO#..","..#ROOYYWWYYOOR#..","..#ROOYYYYYYOOR#..","...#ROOOYYOOOR#...","...#RROOOOOORR#...","....#RRROORRR#....",".....##RRRR##.....",
 "...BBBBBBBBBBBB...","..BbbbbbbbbbbbbB..","...BBBBBBBBBBBB..."]) for x, ch in enumerate(row) if ch != '.'
 for c in [{'#':'#6E2228','Y':'#FFD65A','W':'#FFF6CF','O':'#FF8A2E','R':'#E5441E','B':'#462E1E','b':'#7A5434'}[ch]])
CSS = fonts + '''
*{margin:0;box-sizing:border-box}
body{width:1320px;height:2868px;overflow:hidden;background:linear-gradient(180deg,#2B2163 0%,#3A2C78 40%,#5B3A6E 100%);font-family:'Nunito Sans',sans-serif;color:#FFF6CF;position:relative}
.stars i{position:absolute;width:8px;height:8px;background:#FFF6CF;opacity:.5}
h1{font:600 100px/1.05 'Fredoka',sans-serif;text-align:center;margin:150px 50px 0;white-space:nowrap;letter-spacing:.5px}
p.sub{font:400 50px/1.3 'Nunito Sans',sans-serif;text-align:center;margin:36px 120px 0;color:#E9DFFF}
.phone{position:absolute;left:150px;top:600px;width:1020px;border-radius:84px;overflow:hidden;border:14px solid #15112E;box-shadow:0 40px 120px rgba(0,0,0,.45)}
.phone img{display:block;width:100%}
.kind{position:absolute;left:0;right:0;top:760px;text-align:center}
.kind svg{width:520px;height:auto;image-rendering:pixelated;shape-rendering:crispEdges}
.kind ul{list-style:none;padding:0;margin:90px 140px 0;font:600 64px/1.3 'Fredoka',sans-serif;color:#FFF6CF;text-align:left}
.kind li{margin:0 0 48px;padding-left:96px;position:relative}
.kind li::before{content:'';position:absolute;left:0;top:22px;width:44px;height:44px;background:#FFD36B;clip-path:polygon(0 50%,40% 90%,100% 10%,85% 0,40% 65%,15% 35%)}
.kind li span{display:block;font:400 44px/1.35 'Nunito Sans',sans-serif;color:#E9DFFF;margin-top:6px}
'''
import random
R = random.Random(3)
stars = ''.join(f'<i style="left:{R.randrange(20,1300)}px;top:{R.randrange(20,560)}px;opacity:{R.choice([.25,.4,.6])}"></i>' for _ in range(40))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1320,'height':2868})
    for i, (img, title, sub) in enumerate(SLIDES, 1):
        if img:
            data = base64.b64encode(open(os.path.join(raw, img), 'rb').read()).decode()
            body = f'<div class="stars">{stars}</div><h1>{title}</h1><p class="sub">{sub}</p><div class="phone"><img src="data:image/png;base64,{data}"></div>'
        else:
            body = (f'<div class="stars">{stars}</div><h1>{title}</h1><p class="sub">A habit app that is gentle with you.</p>'
                    f'<div class="kind"><svg viewBox="0 0 18 17">{CAMP}</svg><ul>'
                    '<li>Miss a day? Nothing is lost.<span>No streaks to break. Rest days are always fine.</span></li>'
                    '<li>Nothing is ever for sale.<span>Every Forgeling and pack is earned by showing up.</span></li>'
                    '<li>No accounts. No ads. No tracking.<span>Everything stays on your phone.</span></li></ul></div>')
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(out, f'forgelings-{i}.png'))
    b.close()
print('composed', len(SLIDES))
