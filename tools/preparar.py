# Gera as imagens do site a partir de _ref/ig (posts do Instagram em 1080/1440 px).
import json, os
import numpy as np
from PIL import Image
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IG = os.path.join(RAIZ, '..', '_ref', 'ig')
OUT = os.path.join(RAIZ, 'assets', 'img')

def abre(n): return Image.open(os.path.join(IG, n + '.jpg')).convert('RGB')
def salva(im, pasta, nome, q=86):
    os.makedirs(os.path.join(OUT, pasta), exist_ok=True)
    im.save(os.path.join(OUT, pasta, nome + '.webp'), quality=q, method=6)

def recorta(im, ar, fx=.5, fy=.5, zoom=1.0):
    w, h = im.size
    if w / h > ar: ch = h / zoom; cw = ch * ar
    else: cw = w / zoom; ch = cw / ar
    x = min(max(fx * w - cw / 2, 0), w - cw); y = min(max(fy * h - ch / 2, 0), h - ch)
    return im.crop((round(x), round(y), round(x + cw), round(y + ch)))

# --- portfólio (cat, título)
PORT = [
 ('028_0','braco','Nagasode concluída'),('038_0','braco','Nagasode cicatrizada'),('012_1','braco','Duas nagasode em curso'),('022_1','braco','Nagasode, fundo concluído'),
 ('062_0','braco','Sleeve de koi'),('042_0','braco','Hannya e koi'),('072_0','braco','Ryū, meia manga'),('098_2','braco','Ryū com ramos de sakura'),
 ('100_0','braco','Ryū em curso'),('070_0','braco','Koi a preto e cinza'),('065_2','braco','Sleeve concluída'),('034_2','braco','Sleeve em curso'),
 ('039_0','corpo','Fu dog, costas'),('015_0','corpo','Dois koi na coxa'),('091_1','corpo','Hebi e tora no gémeo'),('040_2','corpo','Ryū freehand na perna'),
 ('044_1','corpo','Ronin e Namazu'),('060_0','corpo','Ryū na cabeça'),('080_1','corpo','Backpiece, primeira sessão de cor'),('078_1','corpo','Legsleeve em linhas'),
 ('007_1','pecas','Namakubi'),('019_1','pecas','Tora'),('004_0','pecas','Ryū, 5 meses cicatrizado'),('023_0','pecas','Tengu'),
 ('055_0','pecas','Hannya freehand'),('054_0','pecas','Ronin tako'),('036_2','pecas','Daruma'),('041_1','pecas','Kaeru'),
 ('052_1','pecas','Bob, o peixe'),('050_2','pecas','Crisântemo freehand'),('079_2','pecas','Oni'),('032_0','pecas','Hebi com crisântemos'),
]
for c, cat, t in PORT:
    im = abre(c)
    salva(recorta(im, .8).resize((720, 900), Image.LANCZOS), 'p', c, 84)
    f = recorta(im, .8); f.thumbnail((1080, 1350), Image.LANCZOS); salva(f, 'full', c, 88)

# --- hero: arte dentro da moldura vermelha, 3:4
def caixa_arte(im):
    a = np.asarray(im).astype(int); h, w, _ = a.shape
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    m = (mn < 150) | ((mx - mn) > 60)
    x0, x1, y0, y1 = int(w*.19), int(w*.81), int(h*.13), int(h*.87)
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    return x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()
HERO = [('077_3','Daruma'),('077_4','Bakeneko'),('083_1','Gama'),('083_2','Dokuro'),('077_2','Koi e Ryū')]
for c, t in HERO:
    im = abre(c); bx0, by0, bx1, by1 = caixa_arte(im)
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
    hh = max((by1 - by0) * 1.22, (bx1 - bx0) * 1.22 / .75); ww = hh * .75
    hh = min(hh, 1560); ww = hh * .75
    cx = min(max(cx, 150 + ww/2), 1290 - ww/2); cy = min(max(cy, 160 + hh/2), 1760 - hh/2)
    cr = im.crop((round(cx-ww/2), round(cy-hh/2), round(cx+ww/2), round(cy+hh/2))).resize((900, 1200), Image.LANCZOS)
    salva(cr, 'hero', c, 90)

# --- disponíveis: cartões com moldura (3:4)
DISP = ['077_3','077_4','083_1','083_2','077_2','083_3','077_1','095_2','095_3','095_4','104_4','107_2']
for c in DISP:
    im = abre(c)
    salva(im.resize((720, 960), Image.LANCZOS), 'disp', c, 86)
    salva(im.resize((1080, 1440), Image.LANCZOS), 'full', c, 88)
PROJ = [('002_0',.5,.5),('105_0',.5,.5),('110_0',.5,.5),('113_0',.5,.5)]
for c, fx, fy in PROJ:
    im = abre(c); salva(recorta(im, .75, fx, fy).resize((720, 960), Image.LANCZOS), 'disp', c, 86)
    f = im.copy(); f.thumbnail((1080, 1440), Image.LANCZOS); salva(f, 'full', c, 88)

# --- sessão a sessão
for c in ['038_5','038_4','038_2','038_0','080_1','059_0','039_0']:
    salva(recorta(abre(c), .8).resize((900, 1125), Image.LANCZOS), 'proc', c, 86)

# --- pinturas e sobre
im = abre('037_1'); f = im.copy(); f.thumbnail((1400, 1400)); salva(f, 'pint', '037_1', 88)
im = abre('008_0'); f = im.copy(); f.thumbnail((1400, 1400)); salva(f, 'pint', '008_0', 88)
salva(recorta(abre('027_4'), .8, .5, .5).resize((900, 1125), Image.LANCZOS), 'sobre', '027_4', 88)

# --- pokédex (quadrado)
POKE = [('117_0','089','Muk',.42,.45,1.6),('116_1','076','Golem',.6,.5,1.5),('102_2','057','Primeape',.45,.42,1.7),('101_1','068','Machamp',.5,.45,1.7),
        ('099_2','094','Gengar',.5,.48,1.5),('097_1','007','Squirtle',.47,.5,1.9),('090_2','059','Arcanine',.55,.42,1.6),('089_2','009','Blastoise',.42,.36,1.25),
        ('088_2','001','Bulbasaur',.5,.38,1.6),('082_2','054','Psyduck',.55,.55,1.5),('069_1','093','Haunter',.55,.52,1.6),('066_1','151','Mew',.5,.48,1.2),('016_1','004','Charmander',.5,.5,1.05)]
for c, n, t, fx, fy, z in POKE:
    salva(recorta(abre(c), 1, fx, fy, z).resize((600, 600), Image.LANCZOS), 'poke', c, 86)

json.dump({'port': PORT, 'hero': HERO, 'disp': DISP, 'proj': [p[0] for p in PROJ], 'poke': [p[:3] for p in POKE]},
          open(os.path.join(RAIZ, 'tools', 'escolhas.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok')
