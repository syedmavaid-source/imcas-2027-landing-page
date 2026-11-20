# Build img/fx_<name>.png (400px circle portraits) from Doha's escalator source cut-outs (Drive: Symposium - Escalator Window - IMCAS - Final_Folder/Links).
# CROP = (centre x, hair top y, chin y) in source pixels; framing: hair top at 12%, chin at 68% of the circle.
from PIL import Image, ImageDraw
import pathlib
D = pathlib.Path(__file__).parent
CROP = {'frank': (877, 203, 1038), 'casabona': (445, 45, 395), 'ruiz': (918, 32, 605), 'sundaram': (931, 139, 968),
        'chacur': (545, 60, 545), 'kaye': (861, 289, 1150), 'brambilla': (640, 30, 535), 'techapichetvanich': (848, 106, 742)}
S = 400
for n, (cx, top, chin) in CROP.items():
    im = Image.open(D / f'{n}.png').convert('RGBA')
    side = (chin - top) / 0.56
    x0, y0 = cx - side / 2, top - 0.12 * side
    crop = im.crop((round(x0), round(y0), round(x0 + side), round(y0 + side))).resize((S, S), Image.LANCZOS)
    bg = Image.new('RGBA', (S, S), (233, 237, 237, 255)); bg.alpha_composite(crop)
    m = Image.new('L', (S * 4, S * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, S * 4 - 1, S * 4 - 1), fill=255)
    bg.putalpha(m.resize((S, S), Image.LANCZOS))
    bg.save(D.parent / 'img' / f'fx_{n}.png', optimize=True)
    print(n, 'ok')
