"""Native Webflow stylesheet: the GitHub page CSS (src.html), scoped to #ev-native, with class renames for names the site already uses, plus bridge.css.
Usage: python3 native/build_native_css.py <version>  ->  webflow/imcas27-native-v<version>.css"""
import re, json, sys, subprocess, pathlib, hashlib
W = pathlib.Path(__file__).resolve().parent.parent; S = W.parent
U = json.loads((W / 'urls.json').read_text()); CDN = 'https://cdn.prod.website-files.com/63a16b39edec0d0cb726136e/'
FONTS = [(300, '6afeb0d2e58532aaa3c57234_imcas27-DIN-Light.ttf', 'truetype'), (400, '6afeb09fff5d927a1913e9fa_imcas27-DIN-Regular.ttf', 'truetype'),
         (500, '6afeb0d2dc78e1e5d4bf766f_imcas27-DIN-Medium.otf', 'opentype'), (700, '6afeb0d3955073727f5777e7_imcas27-DIN-Bold.otf', 'opentype')]
ALIAS = {'dx_sphere.webp': 'dx_sphere_v2.webp', 'kv_model.webp': 'd_seated.jpg'}
s = (S / 'src.html').read_text()
css = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
css = css.replace('/*FONTS*/', ''.join(f"@font-face{{font-family:'DIN';font-weight:{w};font-display:swap;src:url({CDN}{f}) format('{t}')}}" for w, f, t in FONTS))
css = re.sub(r'url\(img/([\w\-.]+)\)', lambda m: f"url({U.get(ALIAS.get(m.group(1), m.group(1)), '')})" if U.get(ALIAS.get(m.group(1), m.group(1))) else 'none', css)
tmp = W / 'native' / '_src.css'; out = W / 'native' / '_scoped.css'; tmp.write_text(css)
subprocess.run(['node', str(W / 'native' / 'scope.mjs'), str(tmp), str(out)], check=True, cwd=W / 'native')
c = out.read_text()
for a, b in [('top', 'evtop'), ('hero', 'evhero'), ('play', 'rplay')]:
    c = re.sub(r'\.' + a + r'(?![\w-])', '.' + b, c)
c += '\n' + (W / 'native' / 'bridge.css').read_text()
v = sys.argv[1]; f = W / f'imcas27-native-v{v}.css'; f.write_text(c)
print(f.name, len(c), hashlib.md5(c.encode()).hexdigest())
