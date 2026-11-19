"""Build the Webflow version of the landing page (Event trials template, embeds inside a CMS-conditional wrapper).
Outputs webflow/e1_style.html, e2_markup.html, e3_script.html. Asset URLs come from webflow/urls.json."""
import re, json, pathlib
H = pathlib.Path(__file__).parent
s = (H / 'src.html').read_text()
U = json.loads((H / 'webflow' / 'urls.json').read_text())
CDN = 'https://cdn.prod.website-files.com/63a16b39edec0d0cb726136e/'
FONTS = [(300, '6afeb0d2e58532aaa3c57234_imcas27-DIN-Light.ttf', 'truetype'), (400, '6afeb09fff5d927a1913e9fa_imcas27-DIN-Regular.ttf', 'truetype'),
         (500, '6afeb0d2dc78e1e5d4bf766f_imcas27-DIN-Medium.otf', 'opentype'), (700, '6afeb0d3955073727f5777e7_imcas27-DIN-Bold.otf', 'opentype')]
fontcss = ''.join(f"@font-face{{font-family:'DIN';font-weight:{w};font-display:swap;src:url({CDN}{f}) format('{t}')}}" for w, f, t in FONTS)
ALIAS = {'dx_sphere.webp': 'dx_sphere_v2.webp', 'kv_model.webp': 'd_seated.jpg'}
def url(n):
    n = ALIAS.get(n, n)
    if n not in U: return ''
    return U[n]
css = re.search(r'<style>(.*?)</style>', s, re.S).group(1).replace('/*FONTS*/', fontcss)
css = re.sub(r'url\(img/([\w\-.]+)\)', lambda m: f'url({url(m.group(1))})' if url(m.group(1)) else 'none', css)
# scope page-level rules to this page only (body gets .imcas27-on from the script)
css = re.sub(r'(^|\})body\{', r'\1body.imcas27-on{', css)
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css = re.sub(r'\s*\n\s*', '', css); css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
body = re.search(r'<body>(.*?)<script src=', s, re.S).group(1)
body = re.sub(r'(src|poster)="img/([\w\-.]+)"', lambda m: f'{m.group(1)}="{url(m.group(2))}"', body)
body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
body = re.sub(r'\n\s*', '\n', body).strip()
js = re.search(r'<script>\n(const T=.*?)</script>', s, re.S).group(1)
imgmap = 'const IMG=' + json.dumps({k: v for k, v in U.items()}) + ';const im=n=>IMG[n]||"";'
js = re.sub(r'img/(fx|su)_\$\{([^}]+)\}\.png', lambda m: '${im("' + m.group(1) + '_"+' + m.group(2) + '+".png")}', js)
js = re.sub(r'img/([\w\-]+\.(?:png|jpg|mp4|webp|svg))', lambda m: url(m.group(1)), js)
leftover = re.findall(r'img/[\w\-.$]+', js + body + css)
js = '(function(){"use strict";document.body.classList.add("imcas27-on");' + imgmap + js + '})();'
out = H / 'webflow'
(out / 'e1_style.html').write_text('<style>' + css + '</style>')
(out / 'e2_markup.html').write_text(body)
(out / 'e3_script.html').write_text('<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n<script>' + js + '</script>')
for f in ['e1_style.html', 'e2_markup.html', 'e3_script.html']: print(f, len((out / f).read_text()))
print('leftover img refs:', leftover)
