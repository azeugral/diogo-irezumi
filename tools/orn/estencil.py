# Estêncil do desenho: preto chapado + sombra em pontilhismo, vetorizado com potrace.
# Uso: python estencil.py entrada.png saida.svg [periodo] [limiar_tinta]
import sys, time, cv2, numpy as np, potrace
src, dst = sys.argv[1], sys.argv[2]
P = float(sys.argv[3]) if len(sys.argv) > 3 else 15
LT = float(sys.argv[4]) if len(sys.argv) > 4 else .36
im = cv2.imread(src); im = cv2.copyMakeBorder(im, 80, 80, 80, 80, cv2.BORDER_CONSTANT, value=(235, 235, 235))
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
k = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
fundo = cv2.GaussianBlur(cv2.morphologyEx(g, cv2.MORPH_CLOSE, k(71)), (0, 0), 25)
L = np.clip(g / np.maximum(fundo, 1), 0, 1)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32); S = hsv[..., 1] / 255; Hh = hsv[..., 0]
cor = S > .38
Ls = cv2.GaussianBlur(L, (0, 0), 1.6)
tinta = (Ls < LT) & ~cor
tinta = cv2.morphologyEx(tinta.astype(np.uint8), cv2.MORPH_CLOSE, k(5)).astype(bool)
# silhueta do desenho: fecha o traço e preenche o miolo
sil = cv2.morphologyEx(tinta.astype(np.uint8), cv2.MORPH_CLOSE, k(45))
cs, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
sil = np.zeros_like(sil); cv2.drawContours(sil, [c for c in cs if cv2.contourArea(c) > 5000], -1, 1, -1)
sil = cv2.erode(sil, k(9)).astype(bool)
perto = cv2.dilate(tinta.astype(np.uint8), k(7)).astype(bool)
# tom da sombra (0 papel .. 1 preto); cor: vermelho escuro mais denso, amarelo leve
tom = np.clip((.93 - L) / .55, 0, 1) ** 1.15
tom = np.where(cor, np.where((Hh > 18) & (Hh < 40), .22, .55), tom)
yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]].astype(np.float32)
a = np.deg2rad(45); u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / P; v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / P
tela = .5 + .25 * (np.cos(u) + np.cos(v))
pontos = (tom * .8 > tela) & ~perto & sil & (tom > .14)
out = (tinta | pontos).astype(np.uint8)
out &= cv2.dilate(sil.astype(np.uint8), k(41))
out = cv2.morphologyEx(out, cv2.MORPH_OPEN, k(3))
n, lab, st, _ = cv2.connectedComponentsWithStats(out)
out[np.isin(lab, np.where(st[:, cv2.CC_STAT_AREA] < 12)[0])] = 0
ys, xs = np.where(out); pad = 10
out = out[ys.min() - pad:ys.max() + pad, xs.min() - pad:xs.max() + pad]
pv = np.full(out.shape + (3,), 235, np.uint8); pv[out > 0] = 20
cv2.imwrite(dst.replace('.svg', '-prev.png'), cv2.resize(pv, None, fx=.5, fy=.5, interpolation=cv2.INTER_AREA))
sm = cv2.GaussianBlur(out.astype(np.float32), (0, 0), 1.3) > .5
t = time.time()
pl = potrace.Bitmap(sm).trace(turdsize=8, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.1, opticurve=True, opttolerance=.3)
fm = lambda p: f"{p[0]:.1f} {p[1]:.1f}" if isinstance(p, tuple) else f"{p.x:.1f} {p.y:.1f}"
d = []
h, w = out.shape
borda = lambda q: (q[0] if isinstance(q, tuple) else q.x) in (0, w) or (q[1] if isinstance(q, tuple) else q.y) in (0, h)
for c in pl:
    if all(borda(sg.end_point) for sg in c.segments): continue  # moldura do fundo invertia a máscara
    d.append("M" + fm(c.start_point))
    for sg in c.segments:
        d.append(("L" + fm(sg.c) + "L" + fm(sg.end_point)) if sg.is_corner else ("C" + fm(sg.c1) + " " + fm(sg.c2) + " " + fm(sg.end_point)))
    d.append("Z")
h, w = out.shape
open(dst, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path fill-rule="evenodd" d="{"".join(d)}"/></svg>')
print(dst, w, h, len(pl), 'curvas', round(time.time() - t, 1), 's')
