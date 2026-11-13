# Composes App Store screenshots (1320 x 2868, iPhone 6.9-inch) from raw app captures, in the field journal look.
# Usage: python3 compose.py RAW_DIR FONTS_CSS OUT_DIR [en|ja]
#   FONTS_CSS: the app's own @font-face rules (Caveat, Nunito Sans, Fredoka, VT323), pulled out of the build.
import sys, os, base64
from playwright.sync_api import sync_playwright
raw, fonts_css, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
fonts = open(fonts_css, encoding='utf8').read()
LANG = sys.argv[4] if len(sys.argv) > 4 else 'en'
SLIDES = {
 'en': [
  ('1-choose.png',  'One small thing a day',        'Turn over three cards and choose the one you will do.'),
  ('2-card.png',    'Each one drawn just for you',  'Do it, and a pixel creature joins your journal. No two alike.'),
  ('8-evening.png', 'A journal that writes itself', 'Answer one small question, and the day becomes a page.'),
  ('3-hearth.png',  'They keep you company',        'Sit by the fire, play, and send them wandering.'),
  ('5-binder.png',  'A binder that fills up',       'Every day you showed up, kept for good.'),
  ('6-map.png',     'A map that draws itself',      'Wander, and the realms ink themselves in.'),
  ('7-forge.png',   'Make things together',         'Turn embers and spare curios into keepsakes.'),
  (None,            'Kind by design',               'A habit journal that is gentle with you.')],
 'ja': [
  ('1-choose.png',  '一日ひとつ、小さなこと',         '3枚のカードをめくって、今日やることを選びます。'),
  ('2-card.png',    'どの子も、あなたのために',       'やりとげると、二つとない生きものが日記に。'),
  ('8-evening.png', 'ひとりでに書かれていく日記',     '小さな質問に答えるだけで、その日がページに。'),
  ('3-hearth.png',  '火のそばで、いつも一緒',         '炉ばたで遊んだり、旅に出したり。'),
  ('5-binder.png',  '少しずつ埋まっていくバインダー', '来た日のことが、ずっと残ります。'),
  ('6-map.png',     'ひとりでに描かれていく地図',     '旅をするほど、地方が描きこまれていきます。'),
  ('7-forge.png',   '一緒にものづくり',               '残り火と予備の珍品で、宝物を作ろう。'),
  (None,            'やさしさを大切に',               'あなたにやさしい習慣日記。')]}[LANG]
KIND = {
 'en': [('Miss a day? Nothing is lost.', 'No streaks to break. Rest days are always fine.'),
        ('Nothing is ever for sale.', 'Every Forgeling and every pack is earned by showing up.'),
        ('No accounts. No ads. No tracking.', 'Everything stays on your phone.')],
 'ja': [('休んでも、何も失いません。', '途切れる連続記録はありません。休みの日はいつでも大丈夫。'),
        ('売り物はありません。', 'フォージリングもパックも、毎日来ることで手に入ります。'),
        ('アカウント・広告・追跡なし。', 'すべてあなたのスマホの中に。')]}[LANG]
STAMP = {'en': ('<b>KEPT</b><span>ON YOUR<br>PHONE</span>'), 'ja': ('<b class="j">保管</b><span class="j">あなたの<br>スマホに</span>')}[LANG]
CSS = fonts + '''
*{margin:0;box-sizing:border-box}
body{width:1320px;height:2868px;overflow:hidden;font-family:'Nunito Sans',sans-serif;color:#FBF1D6;position:relative;
  background:repeating-linear-gradient(90deg,rgba(0,0,0,0) 0 38px,rgba(0,0,0,.06) 38px 40px,rgba(255,255,255,.025) 40px 90px,rgba(0,0,0,.05) 90px 92px),
  radial-gradient(ellipse at 50% 0%,rgba(255,186,96,.22),transparent 60%),#3B2A22}
h1{font:700 128px/1 'Caveat',cursive;text-align:center;margin:150px 40px 0;white-space:nowrap;color:#FBF1D6}
p.sub{font:400 50px/1.3 'Nunito Sans',sans-serif;text-align:center;margin:30px 110px 0;color:#E9DCC0}
.phone{position:absolute;left:150px;top:590px;width:1020px;border-radius:84px;overflow:hidden;border:14px solid #1A120E;box-shadow:0 40px 110px rgba(0,0,0,.5);transform:rotate(-1deg)}
.phone img{display:block;width:100%}
.tape{position:absolute;width:250px;height:76px;background:rgba(255,211,107,.58);z-index:2}
.page{position:absolute;left:110px;right:110px;top:560px;bottom:220px;background:repeating-linear-gradient(transparent 0 79px,rgba(91,74,158,.14) 79px 82px),#FBF5E6;box-shadow:14px 14px 0 #E3D3AE,28px 28px 0 #D9C69C;padding:110px 90px 0 120px;color:#2E2A47;transform:rotate(-.6deg)}
.page::before{content:'';position:absolute;left:70px;top:0;bottom:0;width:5px;background:rgba(168,50,63,.35)}
.page ul{list-style:none;padding:0;margin:0}
.page li{margin:0 0 70px;font:700 84px/1.05 'Caveat',cursive;position:relative;padding-left:100px}
.page li::before{content:'';position:absolute;left:0;top:14px;width:58px;height:58px;border:6px solid #2F6B45;border-radius:50%}
.page li::after{content:'';position:absolute;left:16px;top:24px;width:22px;height:34px;border:solid #2F6B45;border-width:0 9px 9px 0;transform:rotate(40deg)}
.page li span{display:block;font:400 44px/1.4 'Nunito Sans',sans-serif;color:#4B3C8C;font-style:italic;margin-top:14px}
.stamp{position:absolute;right:90px;bottom:110px;width:300px;height:300px;border-radius:50%;border:10px solid #A8323F;color:#A8323F;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-12deg);box-shadow:inset 0 0 0 10px #FBF5E6,inset 0 0 0 18px #A8323F}
.stamp b{font:400 76px/.9 'VT323',monospace}
.stamp span{font:700 24px/1.25 'Nunito Sans',sans-serif;letter-spacing:.1em;text-align:center;max-width:200px;margin-top:8px}
body.ja h1{font:700 96px/1.1 'Noto Sans CJK JP',sans-serif;letter-spacing:.02em}
body.ja p.sub{font:500 46px/1.4 'Noto Sans CJK JP',sans-serif;margin:34px 100px 0}
body.ja .page li{font:700 56px/1.25 'Noto Sans CJK JP',sans-serif}
body.ja .page li span{font:400 40px/1.45 'Noto Sans CJK JP',sans-serif;font-style:normal}
.stamp .j{font-family:'Noto Sans CJK JP',sans-serif}
.stamp b.j{font-size:72px;font-weight:900}
.stamp span.j{font-size:30px;letter-spacing:.05em}
'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1320,'height':2868})
    for i, (img, title, sub) in enumerate(SLIDES, 1):
        if img:
            data = base64.b64encode(open(os.path.join(raw, img), 'rb').read()).decode()
            body = (f'<h1>{title}</h1><p class="sub">{sub}</p>'
                    f'<i class="tape" style="left:90px;top:600px;transform:rotate(-32deg)"></i><i class="tape" style="right:90px;top:585px;transform:rotate(30deg)"></i>'
                    f'<div class="phone"><img src="data:image/png;base64,{data}"></div>')
        else:
            items = ''.join(f'<li>{a}<span>{b}</span></li>' for a, b in KIND)
            body = f'<h1>{title}</h1><p class="sub">{sub}</p><div class="page"><ul>{items}</ul><div class="stamp">{STAMP}</div></div>'
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{LANG}">{body}</body></html>')
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{const h=document.querySelector('h1');let f=parseFloat(getComputedStyle(h).fontSize);while(h.scrollWidth>h.clientWidth&&f>40){f-=2;h.style.fontSize=f+'px';}}")
        pg.screenshot(path=os.path.join(out, f'forgelings-{i}.png'))
    b.close()
print('composed', len(SLIDES))
