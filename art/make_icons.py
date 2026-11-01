# Renders every Forgelings icon from art/forgelings-icon.svg (the seal mark, chosen by Hunter on November 1, 2026).
# Run from the forge folder: python3 art/make_icons.py  -> art/out/*.png. pwa.py and the iPhone app's ios-setup.py copy these.
# The drawing is full-bleed and square: iOS and Android round the corners themselves.
import os, re, base64
from playwright.sync_api import sync_playwright
from PIL import Image
here=os.path.dirname(os.path.abspath(__file__)); out=os.path.join(here,'out'); os.makedirs(out,exist_ok=True)
svg=open(os.path.join(here,'forgelings-icon.svg'),encoding='utf8').read()
inner=re.search(r'<svg[^>]*>([\s\S]*)</svg>',svg).group(1)
def page(S,scale=1.0,bg=None):
    # scale < 1 shrinks the seal inside a full amber square (maskable icons need a safe zone)
    grad=re.search(r'<linearGradient[\s\S]*?</linearGradient>',inner).group(0)
    if scale==1.0 and not bg: art=inner
    else:
        body=re.sub(r'<title>[\s\S]*?</title>','',inner)
        body=re.sub(r'<defs>[\s\S]*?</defs>','',body)
        rect=re.search(r'<rect width="180" height="180"[^>]*></rect>',body).group(0)
        rest=body.replace(rect,'')
        fill=f'fill="{bg}"' if bg else 'fill="url(#g-amb)"'
        art=f'<defs>{grad}</defs><rect width="180" height="180" {fill}></rect><g transform="translate({90-90*scale} {90-90*scale}) scale({scale})">{rest}</g>'
    return f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="{S}" height="{S}" style="display:block">{art}</svg></body></html>'
JOBS=[('icon-192.png',192,1.0,None),('icon-512.png',512,1.0,None),('apple-touch-icon.png',180,1.0,None),
      ('icon-maskable-512.png',512,.8,None),('favicon-64.png',64,1.0,None),('AppIcon-1024.png',1024,1.0,None),
      ('splash-mark-600.png',600,1.0,None)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,S,sc,bg in JOBS:
        pg=b.new_page(viewport={'width':S,'height':S}); pg.set_content(page(S,sc,bg)); pg.wait_for_timeout(100)
        f=os.path.join(out,name); pg.screenshot(path=f,clip={'x':0,'y':0,'width':S,'height':S}); pg.close()
        Image.open(f).convert('RGB').save(f)   # no alpha: Apple rejects app icons with transparency
    b.close()
# the launch screen: the seal small and centred on the app's dark launch colour
sp=Image.new('RGB',(2732,2732),(0x16,0x13,0x2E)); m=Image.open(os.path.join(out,'splash-mark-600.png')).resize((440,440),Image.LANCZOS)
mask=Image.new('L',(440,440),0); from PIL import ImageDraw; ImageDraw.Draw(mask).rounded_rectangle([0,0,439,439],radius=98,fill=255)
sp.paste(m,((2732-440)//2,(2732-440)//2),mask); sp.save(os.path.join(out,'splash-2732.png'))
print('icons:',sorted(os.listdir(out)))
