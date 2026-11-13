# Makes a lived-in save by playing the current build through real taps, day by day (for store screenshots and demos).
# Usage: python3 tools/lived_save.py OUT.json [START=2026-08-27] [DAYS=110] [SEED=11]
#   Run from the dev root after `python3 pwa.py`-style setup (qa/lib.py, Playwright). Plays work.html over local http.
#   Each day: choose one of three cards, do it (sometimes all in, sometimes rest), answer the day's question, sometimes
#   add your own words or a photo postcard (made-up landscape pictures), open packs, visit the Hearth, wander, collect.
import sys, os, json, random, datetime, io, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'qa')); os.environ.setdefault('FORGE_HTML', 'file://' + os.path.join(ROOT, 'work.html'))
from lib import *
import http.server, threading, functools
from PIL import Image, ImageDraw
out = sys.argv[1]; START = datetime.date.fromisoformat(sys.argv[2] if len(sys.argv) > 2 else '2026-08-27')
DAYS = int(sys.argv[3]) if len(sys.argv) > 3 else 110; rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 11)
_d, _f = os.path.split(P[len('file://'):]) if P.startswith('file://') else (None, None)
if _d:
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=_d, **k)
        def log_message(s, *a): pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start(); URL = f'http://127.0.0.1:{srv.server_address[1]}/{_f}'
else: URL = P
FAKE = """(()=>{const R=Date;let off=+(localStorage.getItem('__off')||0);window.__setOff=v=>{off=v;localStorage.setItem('__off',String(v));};window.__real=()=>R.now();
class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"""
LINES = ["Walked the long way home and noticed the maples turning.", "Called Mom back. We talked for an hour.",
  "Finally fixed the squeaky cabinet door.", "Read twenty pages before bed instead of scrolling.",
  "Cooked a real dinner. Leftovers for tomorrow.", "Quiet morning with coffee on the porch.",
  "Cleared out the junk drawer. Found my old harmonica.", "Studied for an hour without my phone in the room.",
  "Sent a thank-you note I'd been putting off.", "Stretched for ten minutes. Felt good.",
  "Took the dog to the beach at sunset.", "Wrote down three things that went right today.",
  "Tired, but I showed up.", "Helped a neighbor carry groceries up the stairs.", "First cold morning of the year."]
def photo(seed):
    r = random.Random(seed); w, h = 640, 480; im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
    top = [(r.randint(60, 140), r.randint(110, 180), r.randint(190, 240)), (240, 150, 90), (90, 80, 150)][seed % 3]
    for y in range(h):
        t = y / h; d.line([(0, y), (w, y)], fill=tuple(int(top[i] * (1 - t) + (250, 220, 180)[i] * t) for i in range(3)))
    sx = r.randint(80, 520); d.ellipse([sx - 40, 90, sx + 40, 170], fill=(255, 240, 200))
    for k in range(3):
        base = 260 + k * 60; pts = [(0, h)] + [(x, base + int(30 * __import__('math').sin(x / (60 + k * 20) + seed + k))) for x in range(0, w + 20, 20)] + [(w, h)]
        g = 120 - k * 30; d.polygon(pts, fill=(40 + k * 10, g, 60 + k * 15))
    for _ in range(r.randint(2, 6)):
        x = r.randint(20, 600); y = r.randint(300, 420); d.polygon([(x, y - 70), (x - 25, y), (x + 25, y)], fill=(20, 60, 40))
    f = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False); im.save(f, 'JPEG', quality=88); return f.name
def vis(pg, sel): return pg.evaluate("s=>{const e=document.querySelector(s);return !!(e&&!e.hidden&&e.offsetParent!==null)}", sel)
def click(pg, sel): pg.evaluate("s=>document.querySelector(s).click()", sel); pg.wait_for_timeout(260)
def settle(pg, limit=24):
    for _ in range(limit):
        if pg.evaluate("document.getElementById('modal').hidden"): return
        for sel in ["#cover", "#rvSkip", "#skipNames", "[data-mood]", "#packTear", "#packNext", "#packDone", "#nudgeOk", "#keptBack", "#vBack", "#vOk", "[data-close]", "#ovClose"]:
            if vis(pg, sel):
                click(pg, sel)
                if sel in ("#cover", "#packTear"): pg.wait_for_timeout(900)
                break
        else: pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
stats = dict(done=0, rest=0, lines=0, posts=0, asks=0, packs=0, wanders=0)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx, pg = newpage(b, timezone_id='America/New_York', locale='en-US'); pg.add_init_script(FAKE); pg.set_default_timeout(8000)
    def go(day):
        ms = pg.evaluate("(s)=>new Date(s).getTime()-window.__real()", day + 'T' + rng.choice(['08:10', '12:30', '19:45']) + ':00')
        pg.evaluate("(v)=>window.__setOff(v)", ms); pg.reload(); pg.wait_for_timeout(700)
    pg.goto(URL); pg.wait_for_selector('#ageGo, #titleGo'); go(START.isoformat()); first_card(pg); settle(pg)
    day = START; end = START + datetime.timedelta(days=DAYS)
    while day < end:
        r = rng.random(); day += datetime.timedelta(days=rng.choice([2, 3]) if r < 0.10 else 1)
        if day > end: day = end
        go(day.isoformat()); settle(pg); tabto(pg, 'today')
        if vis(pg, '#btnTurn'):
            click(pg, '#btnTurn')
            if pg.evaluate("!!document.querySelector('[data-chup]')"):
                for i in rng.sample(range(3), rng.choice([1, 2, 3])): click(pg, f'[data-chup="{i}"]'); pg.wait_for_timeout(500)
                g = pg.evaluate("[...document.querySelectorAll('[data-chgo]')].map(b=>b.dataset.chgo)")
                if g: click(pg, f'[data-chgo="{rng.choice(g)}"]'); pg.wait_for_timeout(900)
            elif vis(pg, '#vBack'): click(pg, '#vBack')
            pg.wait_for_timeout(500); settle(pg)
            a = rng.random()
            if a < 0.08 and vis(pg, '#btnRest'): click(pg, '#btnRest'); stats['rest'] += 1
            elif vis(pg, '#btnDone'): click(pg, '#btnAll' if a > 0.85 else '#btnDone'); pg.wait_for_timeout(500); settle(pg); stats['done'] += 1
        tabto(pg, 'today')
        btns = pg.evaluate("[...document.querySelectorAll('#view-today [data-ask]')].map(b=>b.dataset.ask)")
        if btns: click(pg, f'#view-today [data-ask="{rng.choice(btns)}"]'); stats['asks'] += 1; pg.wait_for_timeout(400); settle(pg)
        if rng.random() < 0.4 and vis(pg, '#btnMargin'):
            click(pg, '#btnMargin'); pg.wait_for_timeout(300)
            if vis(pg, '#jIn'): pg.fill('#jIn', rng.choice(LINES)); click(pg, '#jSave'); stats['lines'] += 1
            settle(pg)
        if rng.random() < 0.3 and vis(pg, '#pcAdd'):
            try:
                with pg.expect_file_chooser(timeout=3000) as fc: click(pg, '#pcAdd')
                fc.value.set_files(photo(day.toordinal())); pg.wait_for_timeout(900); stats['posts'] += 1
            except Exception as e: print('postcard', day, e)
            settle(pg)
        while vis(pg, '#btnPack'): click(pg, '#btnPack'); settle(pg, 40); stats['packs'] += 1; tabto(pg, 'today')
        if rng.random() < 0.7:
            tabto(pg, 'hearth')
            if vis(pg, '#hRelight'): click(pg, '#hRelight'); pg.wait_for_timeout(2500); settle(pg)
            if vis(pg, '#hSnack') and pg.evaluate("!document.getElementById('hSnack').disabled"):
                click(pg, '#hSnack')
                if vis(pg, '[data-snack]'): click(pg, '[data-snack]')
                settle(pg)
            if vis(pg, '#hCollect'): click(pg, '#hCollect'); settle(pg)
            if vis(pg, '#hWander') and rng.random() < 0.7:
                click(pg, '#hWander'); opts = pg.evaluate("[...document.querySelectorAll('#modal [data-wgo]')].map(b=>b.dataset.wgo)")
                if opts: pg.evaluate("v=>document.querySelector('#modal [data-wgo=\"'+v+'\"]').click()", rng.choice(opts)); pg.wait_for_timeout(250); stats['wanders'] += 1
                settle(pg)
            tabto(pg, 'today')
        if pg._errs: print('page error', day, pg._errs[-1]); pg._errs.clear()
        if (day - START).days % 10 == 0: print(day, stats, flush=True)
    s = st(pg); json.dump(s, open(out, 'w'))
    print('saved', out, 'date', s['date'], 'cards', len(s['cards']), 'pages', stats)
    b.close()
