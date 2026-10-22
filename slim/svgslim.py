# Rewrites pixel-art SVG data URIs made of many <rect> elements into one <path> per run of same-fill rects.
# Painting order is kept exactly (only consecutive rects with the same fill are merged), so the picture is identical.
import re, sys

def conv_svg(svg, q):
    # q is the attribute quote as it appears in the URI: "'" or '%22'
    A = lambda name: rf"{name}={re.escape(q)}([^%'\"]*?){re.escape(q)}"
    rect_re = re.compile(r"<rect\b([^>]*?)/>")
    def attrs(a):
        d = {}
        for k in ('x', 'y', 'width', 'height', 'fill', 'fill-opacity', 'opacity'):
            m = re.search(r"(?<![\w-])" + A(k), a)
            if m: d[k] = m.group(1)
        rest = re.sub(r"(?<![\w-])(x|y|width|height|fill|fill-opacity|opacity)=" + re.escape(q) + r"[^%'\"]*?" + re.escape(q), '', a).strip()
        return d, rest
    out = []; pos = 0; run = None  # run = [style_key, [(x,y,w,h)], start_index]
    def flush():
        nonlocal run
        if not run: return
        key, rs = run
        if len(rs) == 1 and False: pass
        d = ''; px = py = None
        for (x, y, w, h) in rs:
            if px is None: d += f"M{fmt(x)} {fmt(y)}"
            else: d += f"m{fmt(x-px)} {fmt(y-py)}"
            d += f"h{fmt(w)}v{fmt(h)}h{fmt(-w)}z"; px, py = x, y
        fill, fo, op = key
        extra = (f" fill={q}{fill}{q}" if fill is not None else '') + (f" fill-opacity={q}{fo}{q}" if fo is not None else '') + (f" opacity={q}{op}{q}" if op is not None else '')
        out.append(f"<path{extra} d={q}{d}{q}/>")
        run = None
    def fmt(v):
        v = round(v, 4); return str(int(v)) if v == int(v) else str(v)
    for m in rect_re.finditer(svg):
        between = svg[pos:m.start()]
        a, rest = attrs(m.group(1))
        mergeable = not rest and 'width' in a and 'height' in a
        if between:
            flush(); out.append(between)
        if not mergeable:
            flush(); out.append(m.group(0)); pos = m.end(); continue
        key = (a.get('fill'), a.get('fill-opacity'), a.get('opacity'))
        r = (float(a.get('x', 0)), float(a.get('y', 0)), float(a['width']), float(a['height']))
        if run and run[0] == key: run[1].append(r)
        else: flush(); run = [key, [r]]
        pos = m.end()
    flush(); out.append(svg[pos:])
    return ''.join(out)

def slim(src, min_len=1200):
    saved = 0; n = 0
    def sub(m):
        nonlocal saved, n
        u = m.group(0)
        if len(u) < min_len or u.count('<rect') < 8: return u
        q = '%22' if 'xmlns=%22' in u else "'"
        new = conv_svg(u, q); saved += len(u) - len(new); n += 1
        return new
    out = re.sub(r"url\(\"data:image/svg\+xml,<svg.*?</svg>\"\)", sub, src, flags=re.S)
    return out, saved, n

if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf8').read()
    o, saved, n = slim(s)
    print('converted', n, 'saved', saved)
