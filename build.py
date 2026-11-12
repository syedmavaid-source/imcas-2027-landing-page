"""Inline the DIN brand fonts (data URIs) into src.html -> index.html. Usage: python3 build.py"""
import base64, pathlib
F = pathlib.Path(__file__).resolve().parents[2] / 'sponsorship' / 'src' / 'fonts'
faces = [(300, 'DIN Light.ttf', 'truetype'), (400, 'DIN Regular.ttf', 'truetype'), (500, 'DIN Medium.otf', 'opentype'), (700, 'DIN Bold.otf', 'opentype')]
css = ''.join(f"@font-face{{font-family:'DIN';font-weight:{w};font-display:swap;src:url(data:font/{'ttf' if t=='truetype' else 'otf'};base64,{base64.b64encode((F/f).read_bytes()).decode()}) format('{t}')}}\n" for w, f, t in faces)
src = pathlib.Path(__file__).with_name('src.html').read_text()
pathlib.Path(__file__).with_name('index.html').write_text(src.replace('/*FONTS*/', css))
print('ok', len(css) // 1024, 'KB fonts')
