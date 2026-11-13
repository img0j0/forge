# Raw App Store captures (440 x 956 at 3x = 1320 x 2868) of the store edition, from a lived-in save.
# Usage: python3 shots.py URL_OF_www/index.html SAVE.json OUT_DIR QA_DIR [LANG]
#   URL: serve www/ over http (file:// storage is unreliable in some Chromium builds).
#   SAVE.json: a lived-in save; make one with the dev branch's tools/lived_save.py. QA_DIR: the dev branch's qa/ (lib.py).
#   LANG: en (default) or ja. The save's last day should be a done day with an answer, your words and a postcard.
import sys, os, json, datetime as dt
url, save, out, qa = sys.argv[1:5]; LANG = sys.argv[5] if len(sys.argv) > 5 else 'en'
sys.path.insert(0, qa); os.environ["FORGE_HTML"] = url
from lib import *
os.makedirs(out, exist_ok=True)
LIVED = json.load(open(save))
def clock(day, hh):
    ms = int(dt.datetime.fromisoformat(day + f"T{hh}:00-05:00").timestamp() * 1000)
    return "(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()" % ms
def session(b, hh, nextday=False):
    day = LIVED["date"]
    if nextday: day = (dt.date.fromisoformat(day) + dt.timedelta(days=1)).isoformat()
    ctx, pg = newpage(b, 440, 956, device_scale_factor=3, timezone_id="America/New_York", reduced_motion="reduce",
                      locale="ja-JP" if LANG == "ja" else "en-US")
    pg.add_init_script(clock(day, hh)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s = json.loads(json.dumps(LIVED)); s["seen"] = 999
    s["forge"]["made"] = sorted(set(s["forge"].get("made", []) + ["xlantern", "relic0", "charm1", "kettle"]))
    s["explore"] = {str(i): 4 for i in range(10)}
    setst(pg, s); pg.evaluate("l=>localStorage.setItem('forge-lang',l)", LANG); pg.reload(); pg.wait_for_timeout(1500); closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    return ctx, pg
def snap(pg, name, wait=800):
    pg.evaluate("document.activeElement&&document.activeElement.blur&&document.activeElement.blur()"); pg.wait_for_timeout(wait)
    pg.screenshot(path=os.path.join(out, name + ".png"))
def click(pg, sel): pg.evaluate("s=>{const e=document.querySelector(s);e&&e.click()}", sel); pg.wait_for_timeout(500)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=swiftshader'])
    # A fresh morning: three face-down cards, all turned over
    ctx, pg = session(b, "09:30", nextday=True)
    tabto(pg, "today"); pg.evaluate("scrollTo(0,0)"); click(pg, "#btnTurn"); pg.wait_for_timeout(800)
    for i in range(3): click(pg, f'[data-chup="{i}"]')
    snap(pg, "1-choose", 1200); print("choose", pg._errs[:3]); ctx.close()
    # The day's page: the find, the question answered, your words and a postcard
    ctx, pg = session(b, "16:30")
    tabto(pg, "today"); pg.evaluate("scrollTo(0,0)"); snap(pg, "4-today")
    pg.evaluate("()=>{const e=document.querySelector('#view-today .pcwrap,#view-today .ask,#view-today [data-ask]');e&&e.scrollIntoView({block:'center'})}"); snap(pg, "4-today-lower")
    tabto(pg, "binder"); pg.evaluate("scrollTo(0,0)"); snap(pg, "5-binder")
    pg.evaluate("()=>{const c=[...document.querySelectorAll('#view-binder [data-insp]')].find(x=>x.querySelector('.r-legendary,.r-epic,.r-rare'))||document.querySelector('#view-binder [data-insp]');c.click()}"); snap(pg, "2-card", 1200)
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    openmap(pg); pg.evaluate("scrollTo(0,0)"); snap(pg, "6-map", 1200)
    tabto(pg, "hearth"); click(pg, "#hForge"); pg.evaluate("()=>{for(const e of document.querySelectorAll('#modal, #modal *'))if(e.scrollTop)e.scrollTop=0}"); snap(pg, "7-forge")
    print("day", pg._errs[:3]); ctx.close()
    # Night by the fire (the season's weather), and closing the day
    ctx, pg = session(b, "21:30")
    tabto(pg, "hearth"); pg.evaluate("scrollTo(0,0)"); snap(pg, "3-hearth", 1500)
    tabto(pg, "today"); pg.evaluate("scrollTo(0,0)"); click(pg, "#btnClose"); pg.wait_for_timeout(800); snap(pg, "8-evening")
    print("night", pg._errs[:3]); ctx.close()
    b.close()
print("raw captures in", out)
