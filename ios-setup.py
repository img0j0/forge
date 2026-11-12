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
if 'NSPhotoLibraryAddUsageDescription' not in s:
    # the share sheet offers "Save Image" for a shared Forgeling picture; iOS needs this sentence or the app crashes there
    s = s.replace('</dict>\n</plist>', '\t<key>NSPhotoLibraryAddUsageDescription</key>\n\t<string>Forgelings saves a picture of your Forgeling to your photos only when you choose Save Image.</string>\n</dict>\n</plist>')
open(p, 'w', encoding='utf8').write(s)

# ---- privacy manifest: no tracking, no data collected; the plugins' UserDefaults (Preferences) and file timestamp
#      (Filesystem) use, declared with Apple's reason codes. Registered as a bundle resource in the project below. ----
PRIV = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>NSPrivacyTracking</key>
\t<false/>
\t<key>NSPrivacyTrackingDomains</key>
\t<array/>
\t<key>NSPrivacyCollectedDataTypes</key>
\t<array/>
\t<key>NSPrivacyAccessedAPITypes</key>
\t<array>
\t\t<dict>
\t\t\t<key>NSPrivacyAccessedAPIType</key>
\t\t\t<string>NSPrivacyAccessedAPICategoryUserDefaults</string>
\t\t\t<key>NSPrivacyAccessedAPITypeReasons</key>
\t\t\t<array>
\t\t\t\t<string>CA92.1</string>
\t\t\t</array>
\t\t</dict>
\t\t<dict>
\t\t\t<key>NSPrivacyAccessedAPIType</key>
\t\t\t<string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
\t\t\t<key>NSPrivacyAccessedAPITypeReasons</key>
\t\t\t<array>
\t\t\t\t<string>C617.1</string>
\t\t\t</array>
\t\t</dict>
\t</array>
</dict>
</plist>
'''
open(os.path.join(app, 'App', 'PrivacyInfo.xcprivacy'), 'w', encoding='utf8').write(PRIV)

# ---- project: iPhone only, version 1.0.0 ----
p = os.path.join(app, 'App.xcodeproj', 'project.pbxproj'); s = open(p, encoding='utf8').read()
s = s.replace('TARGETED_DEVICE_FAMILY = "1,2";', 'TARGETED_DEVICE_FAMILY = 1;').replace('MARKETING_VERSION = 1.0;', 'MARKETING_VERSION = 1.0.0;')
if 'PrivacyInfo.xcprivacy' not in s:
    REF, BLD = 'F0F0A1B2C3D4E5F600000001', 'F0F0A1B2C3D4E5F600000002'
    s = s.replace('/* End PBXBuildFile section */', f'\t\t{BLD} /* PrivacyInfo.xcprivacy in Resources */ = {{isa = PBXBuildFile; fileRef = {REF} /* PrivacyInfo.xcprivacy */; }};\n/* End PBXBuildFile section */', 1)
    s = s.replace('/* End PBXFileReference section */', f'\t\t{REF} /* PrivacyInfo.xcprivacy */ = {{isa = PBXFileReference; lastKnownFileType = text.xml; path = PrivacyInfo.xcprivacy; sourceTree = "<group>"; }};\n/* End PBXFileReference section */', 1)
    s = s.replace('\t\t\t\t504EC30E1FED79650016851F /* Assets.xcassets */,\n', f'\t\t\t\t504EC30E1FED79650016851F /* Assets.xcassets */,\n\t\t\t\t{REF} /* PrivacyInfo.xcprivacy */,\n', 1)
    s = s.replace('\t\t\t\t504EC30F1FED79650016851F /* Assets.xcassets in Resources */,\n', f'\t\t\t\t504EC30F1FED79650016851F /* Assets.xcassets in Resources */,\n\t\t\t\t{BLD} /* PrivacyInfo.xcprivacy in Resources */,\n', 1)
    assert s.count('PrivacyInfo.xcprivacy') == 6, s.count('PrivacyInfo.xcprivacy')
# 0.52: iCloud save (CloudSavePlugin.swift, registered by MainViewController.swift) and its entitlement
for name, ref, bld in (('CloudSavePlugin.swift', 'F0F0A1B2C3D4E5F600000011', 'F0F0A1B2C3D4E5F600000012'),
                       ('MainViewController.swift', 'F0F0A1B2C3D4E5F600000013', 'F0F0A1B2C3D4E5F600000014')):
    if name not in s:
        s = s.replace('/* End PBXBuildFile section */', f'\t\t{bld} /* {name} in Sources */ = {{isa = PBXBuildFile; fileRef = {ref} /* {name} */; }};\n/* End PBXBuildFile section */', 1)
        s = s.replace('/* End PBXFileReference section */', f'\t\t{ref} /* {name} */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {name}; sourceTree = "<group>"; }};\n/* End PBXFileReference section */', 1)
        s = s.replace('\t\t\t\t504EC3071FED79650016851F /* AppDelegate.swift */,\n', f'\t\t\t\t504EC3071FED79650016851F /* AppDelegate.swift */,\n\t\t\t\t{ref} /* {name} */,\n', 1)
        s = s.replace('\t\t\t\t504EC3081FED79650016851F /* AppDelegate.swift in Sources */,\n', f'\t\t\t\t504EC3081FED79650016851F /* AppDelegate.swift in Sources */,\n\t\t\t\t{bld} /* {name} in Sources */,\n', 1)
        assert s.count(name) == 6, (name, s.count(name))
if 'App.entitlements' not in s:
    ref = 'F0F0A1B2C3D4E5F600000015'
    s = s.replace('/* End PBXFileReference section */', f'\t\t{ref} /* App.entitlements */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.entitlements; path = App.entitlements; sourceTree = "<group>"; }};\n/* End PBXFileReference section */', 1)
    s = s.replace('\t\t\t\t504EC3131FED79650016851F /* Info.plist */,\n', f'\t\t\t\t504EC3131FED79650016851F /* Info.plist */,\n\t\t\t\t{ref} /* App.entitlements */,\n', 1)
    s = s.replace('\t\t\t\tCODE_SIGN_STYLE = Automatic;\n', '\t\t\t\tCODE_SIGN_ENTITLEMENTS = App/App.entitlements;\n\t\t\t\tCODE_SIGN_STYLE = Automatic;\n')
    assert s.count('CODE_SIGN_ENTITLEMENTS = App/App.entitlements;') == 2 and s.count('App.entitlements') == 5, s.count('App.entitlements')
open(p, 'w', encoding='utf8').write(s)
# the storyboard's view controller becomes MainViewController, which registers the local plugins
sb = os.path.join(app, 'App', 'Base.lproj', 'Main.storyboard'); t = open(sb, encoding='utf8').read()
t = t.replace('customClass="CAPBridgeViewController" customModule="Capacitor"', 'customClass="MainViewController" customModule="App" customModuleProvider="target"')
open(sb, 'w', encoding='utf8').write(t)

# ---- art: the seal mark icon and the dark launch screen (rendered on the dev branch by art/make_icons.py, copied into art/) ----
import shutil
here=os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(here,'art','AppIcon-1024.png'),os.path.join(app,'App','Assets.xcassets','AppIcon.appiconset','AppIcon-512@2x.png'))
sp=os.path.join(app,'App','Assets.xcassets','Splash.imageset')
for f in os.listdir(sp):
    if f.endswith('.png'): shutil.copy(os.path.join(here,'art','splash-2732.png'),os.path.join(sp,f))
print('iOS settings and art applied')
