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

# ---- art: the seal mark icon and the dark launch screen (rendered on the dev branch by art/make_icons.py, copied into art/) ----
import shutil
here=os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(here,'art','AppIcon-1024.png'),os.path.join(app,'App','Assets.xcassets','AppIcon.appiconset','AppIcon-512@2x.png'))
sp=os.path.join(app,'App','Assets.xcassets','Splash.imageset')
for f in os.listdir(sp):
    if f.endswith('.png'): shutil.copy(os.path.join(here,'art','splash-2732.png'),os.path.join(sp,f))
print('iOS settings and art applied')
