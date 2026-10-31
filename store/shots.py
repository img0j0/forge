# Raw App Store captures (440 x 956 at 3x = 1320 x 2868) of the store edition, from a lived-in save.
# Usage: python3 shots.py URL_OF_www/index.html SAVE.json OUT_DIR QA_DIR
#   URL: serve www/ over http (file:// storage is unreliable in some Chromium builds).
#   SAVE.json: a lived-in save (the 110-day simulated save from the qa tools). QA_DIR: forge dev branch's qa/ (for lib.py).
import sys, os, json, datetime as dt
url, save, out, qa = sys.argv[1:5]
sys.path.insert(0, qa); os.environ["FORGE_HTML"] = url
from lib import *
os.makedirs(out, exist_ok=True)
LIVED = json.load(open(save))
def clock(hh):
    ms = int(dt.datetime.fromisoformat(LIVED["date"] + f"T{hh}:00-05:00").timestamp() * 1000)
    return "(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()" % ms
def session(b, hh):
    ctx, pg = newpage(b, 440, 956, device_scale_factor=3, timezone_id="America/New_York", reduced_motion="reduce")
    pg.add_init_script(clock(hh)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s = json.loads(json.dumps(LIVED)); s["seen"] = 999
    s["forge"]["made"] = sorted(set(s["forge"].get("made", []) + ["xlantern", "relic0", "charm1", "kettle"]))
    s["explore"] = {str(i): 4 for i in range(10)}
    setst(pg, s); pg.reload(); pg.wait_for_timeout(1200); closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    return ctx, pg
def snap(pg, name, wait=800):
    pg.evaluate("document.activeElement&&document.activeElement.blur&&document.activeElement.blur()"); pg.wait_for_timeout(wait)
    pg.screenshot(path=os.path.join(out, name + ".png"))
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=swiftshader'])
    ctx, pg = session(b, "11:30")
    tabto(pg, "today"); pg.evaluate("scrollTo(0,0)"); snap(pg, "1-today")
    tabto(pg, "binder"); pg.evaluate("scrollTo(0,0)"); snap(pg, "4-binder")
    pg.evaluate("()=>{const c=[...document.querySelectorAll('#view-binder [data-insp]')].find(x=>x.querySelector('.r-epic,.r-legendary,.r-rare'))||document.querySelector('#view-binder [data-insp]');c.click()}"); snap(pg, "2-card", 1200)
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    openmap(pg); pg.evaluate("scrollTo(0,0)"); snap(pg, "5-map", 1200)
    tabto(pg, "hearth"); pg.evaluate("document.getElementById('hForge').click()"); snap(pg, "6-forge")
    print("day", pg._errs[:3]); ctx.close()
    ctx, pg = session(b, "21:30")
    tabto(pg, "hearth"); pg.evaluate("scrollTo(0,0)"); snap(pg, "3-hearth", 1500)
    print("night", pg._errs[:3]); ctx.close()
    b.close()
print("raw captures in", out)
