from lib import *
# 0.30.1: room to grow. Slimmer pixel SVGs and one unused font face dropped; nothing visible changes.
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    html=pg.evaluate("document.documentElement.outerHTML")
    faces=pg.evaluate("[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules]}catch(e){return []}}).filter(r=>r.cssText&&r.cssText.startsWith('@font-face')).map(r=>r.style.fontFamily.replace(/\"/g,'')+' '+r.style.fontWeight).sort()")
    rec("Fonts","the bundled faces are exactly the ones in use",faces==["Fredoka 500","Fredoka 600","Nunito Sans 400","Nunito Sans 700","Press Start 2P 400","VT323 400"],faces)
    rec("Fonts","every bundled face loads",pg.evaluate("Promise.all(['500 16px Fredoka','600 16px Fredoka','400 16px \"Nunito Sans\"','700 16px \"Nunito Sans\"','16px \"Press Start 2P\"','16px VT323'].map(f=>document.fonts.load(f))).then(r=>r.every(x=>x.length>0))"))
    big=[len(u) for u in re.findall(r"data:image/svg\+xml,<svg.*?</svg>",html,re.S) if len(u)>9000]
    rec("SVG","no pixel-art background is stored one rectangle per pixel any more",not big,big)
    rec("SVG","the card back and frames still draw",pg.evaluate("(()=>{const v=getComputedStyle(document.documentElement).getPropertyValue('--cbT');return v.includes('<path')})()"))
    if P.startswith("file://"): rec("Size","the app keeps room under the 640 KB budget (below 630 KB)",len(open(P[7:]).read().encode())<630000)
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_301"); print(sum(r["ok"] for r in RES),"/",len(RES))
