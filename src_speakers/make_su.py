# Suite-card portraits img/su_<name>.png (160px circle, tight face crop, greyscale) + initial placeholders like su_hannan.png.
# CROP = (centre x, hair top y, chin y) in source px; framing: hair top at 8%, chin at 74%.
from PIL import Image, ImageDraw, ImageOps, ImageFont
import pathlib
D = pathlib.Path(__file__).parent; IMG = D.parent / 'img'; S = 160
CROP = {'techapichetvanich': (848, 106, 742), 'sundaram': (931, 139, 968), 'moukalled': (605, 55, 530), 'crabai': (185, 30, 262)}
def circle(im):
    m = Image.new('L', (S * 4, S * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, S * 4 - 1, S * 4 - 1), fill=255)
    im.putalpha(m.resize((S, S), Image.LANCZOS)); return im
for n, (cx, top, chin) in CROP.items():
    im = Image.open(D / f'{n}.png').convert('RGBA'); side = (chin - top) / 0.66
    x0, y0 = cx - side / 2, top - 0.08 * side
    c = im.crop((round(x0), round(y0), round(x0 + side), round(y0 + side))).resize((S, S), Image.LANCZOS)
    bg = Image.new('RGBA', (S, S), (225, 232, 233, 255)); bg.alpha_composite(c)
    g = ImageOps.grayscale(bg.convert('RGB')).convert('RGBA')
    circle(g).save(IMG / f'su_{n}.png', optimize=True); print(n)
ref = Image.open(IMG / 'su_hannan.png').convert('RGBA'); col = ref.getpixel((30, 80)); fg = ref.getpixel((80, 80))
font = ImageFont.truetype(str(D.parents[2] / 'sponsorship/src/fonts/DIN Medium.otf'), 64)
for n, ch in (('aljerayan', 'A'), ('khorsand', 'K')):
    im = Image.new('RGBA', (S, S), col); d = ImageDraw.Draw(im); d.text((S / 2, S / 2 + 2), ch, font=font, fill=fg, anchor='mm')
    circle(im).save(IMG / f'su_{n}.png'); print(n, col, fg)
