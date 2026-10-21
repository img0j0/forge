# Builds www/ for the iPhone app from the Forgelings web build (../forge/work.html by default).
# Marks it as the store edition, so tester-only pieces are hidden even before Capacitor starts.
import os, re, sys, shutil
here = os.path.dirname(os.path.abspath(__file__))
src_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'forgelings.html')
src = open(src_path, encoding='utf8').read()
src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="forge-build" content="store">', 1)
src = re.sub(r'<title>Forgelings \(prototype [0-9.]+\)</title>', '<title>Forgelings</title>', src, count=1)
assert 'content="store"' in src and '<title>Forgelings</title>' in src
out = os.path.join(here, 'www'); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(src)
print('www/index.html', len(src.encode()), 'bytes from', os.path.basename(src_path))
