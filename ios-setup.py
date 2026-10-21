# Applies Forgelings' iOS settings and art to the generated Xcode project (safe to run more than once).
import os, re, json
from PIL import Image, ImageDraw, ImageChops
here = os.path.dirname(os.path.abspath(__file__)); app = os.path.join(here, 'ios', 'App')

# ---- Info.plist: portrait iPhone, modern CPUs, no custom encryption ----
p = os.path.join(app, 'App', 'Info.plist'); s = open(p, encoding='utf8').read()
s = re.sub(r'<key>UIRequiredDeviceCapabilities</key>\s*<array>.*?</array>', '<key>UIRequiredDeviceCapabilities</key>\n\t<array>\n\t\t<string>arm64</string>\n\t</array>', s, flags=re.S)
s = re.sub(r'<key>UISupportedInterfaceOrientations</key>\s*<array>.*?</array>', '<key>UISupportedInterfaceOrientations</key>\n\t<array>\n\t\t<string>UIInterfaceOrientationPortrait</string>\n\t</array>', s, flags=re.S)
s = re.sub(r'\s*<key>UISupportedInterfaceOrientations~ipad</key>\s*<array>.*?</array>', '', s, flags=re.S)
if 'ITSAppUsesNonExemptEncryption' not in s:
    s = s.replace('</dict>\n</plist>', '\t<key>ITSAppUsesNonExemptEncryption</key>\n\t<false/>\n</dict>\n</plist>')
open(p, 'w', encoding='utf8').write(s)

# ---- project: iPhone only, version 1.0.0 ----
p = os.path.join(app, 'App.xcodeproj', 'project.pbxproj'); s = open(p, encoding='utf8').read()
s = s.replace('TARGETED_DEVICE_FAMILY = "1,2";', 'TARGETED_DEVICE_FAMILY = 1;').replace('MARKETING_VERSION = 1.0;', 'MARKETING_VERSION = 1.0.0;')
open(p, 'w', encoding='utf8').write(s)

# ---- art: the pixel campfire icon (same drawing as the web icons) and a dark launch screen ----
G=[".........#........","........#Y#.......","........#Y#.......",".......#YY#.......","...#...#YYY#..#...","..#O#.#YYWY#.#O#..","..#O#.#YWWY#.#O#..",
   "..#OO#YYWWYY#OO#..","..#ROOYYWWYYOOR#..","..#ROOYYYYYYOOR#..","...#ROOOYYOOOR#...","...#RROOOOOORR#...","....#RRROORRR#....",".....##RRRR##.....",
   "...BBBBBBBBBBBB...","..BbbbbbbbbbbbbB..","...BBBBBBBBBBBB..."]
C={'#':(110,34,40),'Y':(255,214,90),'W':(255,246,207),'O':(255,138,46),'R':(229,68,30),'B':(70,46,30),'b':(122,84,52)}
def art(S, frac, sparks=True, glow=True):
    img=Image.new('RGB',(S,S)); d=ImageDraw.Draw(img)
    for y in range(S):
        t=y/S; d.line([(0,y),(S,y)],fill=(int(0x3A+(0x17-0x3A)*t),int(0x2C+(0x13-0x2C)*t),int(0x78+(0x36-0x78)*t)))
    px=max(1,int(S*frac/18)); w=18*px; h=len(G)*px; ox=(S-w)//2; oy=(S-h)//2
    if glow:
        gl=Image.new('RGB',(S,S)); gd=ImageDraw.Draw(gl); R=int(S*frac*.43)
        for r in range(R,0,-max(1,S//90)):
            k=int(100*(1-r/R)**1.5); gd.ellipse([S/2-r,S/2+S*frac*.1-r,S/2+r,S/2+S*frac*.1+r],fill=(k,int(k*.55),int(k*.2)))
        img=ImageChops.add(img,gl); d=ImageDraw.Draw(img)
    for j,row in enumerate(G):
        for i,ch in enumerate(row):
            if ch!='.': d.rectangle([ox+i*px,oy+j*px,ox+i*px+px-1,oy+j*px+px-1],fill=C[ch])
    if sparks:
        q=max(2,px//2)
        for (fx,fy,c) in [(.17,.12,(255,200,90)),(.78,.19,(255,150,70)),(.13,.39,(255,170,80)),(.83,.44,(255,200,90)),(.67,.08,(255,246,207))]:
            x=int(S/2+(fx-.5)*S*frac); y=int(S/2+(fy-.5)*S*frac); d.rectangle([x,y,x+q,y+q],fill=c)
    return img
art(1024,.86).save(os.path.join(app,'App','Assets.xcassets','AppIcon.appiconset','AppIcon-512@2x.png'))
sp=os.path.join(app,'App','Assets.xcassets','Splash.imageset')
for f in os.listdir(sp):
    if f.endswith('.png'): art(2732,.16,sparks=False).save(os.path.join(sp,f))
print('iOS settings and art applied')
