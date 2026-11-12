# Applies Forgelings' Android settings and art to the generated Android project (safe to run more than once).
# Run after `npx cap add android` or `npx cap sync android`. Mirrors ios-setup.py.
import os, re
from PIL import Image, ImageDraw
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, 'android', 'app', 'src', 'main', 'res')
ICON = Image.open(os.path.join(here, 'art', 'AppIcon-1024.png')).convert('RGBA')
SPLASH = Image.open(os.path.join(here, 'art', 'splash-2732.png')).convert('RGBA')
NIGHT = '#16132E'
DENS = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

def wr(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w', encoding='utf8').write(text)

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), r, fill=255)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def circle(im):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, im.size[0] - 1, im.size[1] - 1), fill=255)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

# ---- launcher icons: the wax seal. Adaptive icon = the whole icon (its own warm gradient) at 90% of the 108dp
#      canvas, so the full seal sits inside the 72dp area every launcher mask keeps; a matching gradient behind it. ----
for d, k in DENS.items():
    leg = round(48 * k); fg = round(108 * k)
    small = ICON.resize((leg, leg), Image.LANCZOS)
    rounded(small, round(leg * .18)).save(os.path.join(res, f'mipmap-{d}', 'ic_launcher.png'))
    circle(small).save(os.path.join(res, f'mipmap-{d}', 'ic_launcher_round.png'))
    canvas = Image.new('RGBA', (fg, fg), (0, 0, 0, 0)); s = round(fg * .9); o = (fg - s) // 2
    canvas.paste(ICON.resize((s, s), Image.LANCZOS), (o, o)); canvas.save(os.path.join(res, f'mipmap-{d}', 'ic_launcher_foreground.png'))
wr(os.path.join(res, 'drawable', 'ic_launcher_background.xml'), '''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="270" android:startColor="#FFD57A" android:endColor="#FF9F5A" />
</shape>
''')
for f in ('ic_launcher.xml', 'ic_launcher_round.xml'):
    wr(os.path.join(res, 'mipmap-anydpi-v26', f), '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
''')
v24 = os.path.join(res, 'drawable-v24', 'ic_launcher_foreground.xml')
if os.path.exists(v24): os.remove(v24)  # Capacitor's placeholder vector would win over our PNG on Android 7+
wr(os.path.join(res, 'values', 'ic_launcher_background.xml'), '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FFBA6A</color>\n</resources>\n')

# ---- notification icon: Android draws it as a single-colour silhouette, so a white flame-and-book cut from the seal ----
src = ICON.resize((512, 512), Image.LANCZOS)
sil = Image.new('RGBA', src.size, (0, 0, 0, 0)); px = src.load(); sp = sil.load()
for y in range(512):
    for x in range(512):
        r, g, b, a = px[x, y]
        if r > 225 and g > 200 and b > 180 and (x - 256) ** 2 + (y - 256) ** 2 < 190 ** 2: sp[x, y] = (255, 255, 255, 255)
bb = sil.getbbox(); sil = sil.crop(bb); side = max(sil.size); sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
sq.paste(sil, ((side - sil.size[0]) // 2, (side - sil.size[1]) // 2))
for d, k in DENS.items():
    n = round(24 * k); pad = round(2 * k); im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    im.paste(sq.resize((n - 2 * pad, n - 2 * pad), Image.LANCZOS), (pad, pad))
    os.makedirs(os.path.join(res, f'drawable-{d}'), exist_ok=True); im.save(os.path.join(res, f'drawable-{d}', 'ic_stat_forgelings.png'))

# ---- launch screen: the night campfire art (Android 11 and older), night colour + seal on Android 12+ ----
def cover(im, w, h):
    s = max(w / im.size[0], h / im.size[1]); r = im.resize((round(im.size[0] * s), round(im.size[1] * s)), Image.LANCZOS)
    l = (r.size[0] - w) // 2; t = (r.size[1] - h) // 2; return r.crop((l, t, l + w, t + h))
for d, k in DENS.items():
    for o, (w, h) in (('port', (320, 480)), ('land', (480, 320))):
        cover(SPLASH, round(w * k), round(h * k)).convert('RGB').save(os.path.join(res, f'drawable-{o}-{d}', 'splash.png'))
cover(SPLASH, 480, 480).convert('RGB').save(os.path.join(res, 'drawable', 'splash.png'))
p = os.path.join(res, 'values', 'styles.xml'); s = open(p, encoding='utf8').read()
if 'windowSplashScreenBackground' not in s:
    s = s.replace('<item name="android:background">@drawable/splash</item>\n    </style>',
                  '<item name="android:background">@drawable/splash</item>\n'
                  f'        <item name="windowSplashScreenBackground">{NIGHT}</item>\n'
                  '        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher_foreground</item>\n'
                  '        <item name="postSplashScreenTheme">@style/AppTheme.NoActionBar</item>\n    </style>')
open(p, 'w', encoding='utf8').write(s)

# ---- manifest: portrait phone layout like the iPhone app ----
p = os.path.join(here, 'android', 'app', 'src', 'main', 'AndroidManifest.xml'); s = open(p, encoding='utf8').read()
if 'screenOrientation' not in s:
    s = s.replace('android:name=".MainActivity"', 'android:name=".MainActivity"\n            android:screenOrientation="portrait"')
open(p, 'w', encoding='utf8').write(s)
print('android setup applied')
