"""Motor de desenho dos esqueletos do Bestiário (32×32, de frente).

Cada sprite é montado em camadas: itens das costas → corpo → roupa → crânio →
chapéu → itens nas mãos. Cada camada recebe sombreamento automático (luz de
cima/esquerda) e contorno próprio, o que separa as peças a 32 px.

O corpo muda por estágio (seção C do AGENTS.md):
  1 = bebê (cabeça grande, corpo curto, olhos grandes)
  2 = adolescente (proporção intermediária, postura solta)
  3 = adulto (ombros largos, crânio menor em relação ao corpo, postura firme)
"""
from PIL import Image, ImageDraw

OUTL = (40, 30, 48)
BONE = (240, 236, 222)
BONE_D = (198, 190, 170)
EYE = (40, 30, 48)
W = 32
GROUND = 30


def clamp(v):
    return max(0, min(255, int(v)))


def lighten(c, f):
    return tuple(clamp(c[i] + (255 - c[i]) * f) for i in range(3))


def darken(c, f):
    return tuple(clamp(c[i] * (1 - f)) for i in range(3))


class Layer:
    """Camada de desenho com cores base; sombreada e contornada ao compor."""

    def __init__(self, shade=True, outline=True):
        self.img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self.shade = shade
        self.outline = outline

    # primitivas (coordenadas inteiras, sem antialias)
    def px(self, x, y, c):
        if 0 <= x < W and 0 <= y < W:
            self.img.putpixel((int(x), int(y)), c + (255,))

    def rect(self, x, y, w, h, c):
        if w > 0 and h > 0:
            self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=c + (255,))

    def ell(self, cx, cy, rx, ry, c):
        for yy in range(int(cy - ry - 1), int(cy + ry + 2)):
            for xx in range(int(cx - rx - 1), int(cx + rx + 2)):
                dx = (xx + 0.5 - cx) / max(rx, 0.01)
                dy = (yy + 0.5 - cy) / max(ry, 0.01)
                if dx * dx + dy * dy <= 1.0:
                    self.px(xx, yy, c)

    def poly(self, pts, c):
        self.d.polygon([(int(round(x)), int(round(y))) for x, y in pts], fill=c + (255,))

    def line(self, x0, y0, x1, y1, c, w=1):
        if w == 1:
            self.d.line([(x0, y0), (x1, y1)], fill=c + (255,))
        else:
            self.d.line([(x0, y0), (x1, y1)], fill=c + (255,), width=w)


def _shade(img):
    src = img.copy()
    for y in range(W):
        for x in range(W):
            p = src.getpixel((x, y))
            if p[3] == 0:
                continue
            c = p[:3]
            up = src.getpixel((x, y - 1))[3] if y > 0 else 0
            lf = src.getpixel((x - 1, y))[3] if x > 0 else 0
            dn = src.getpixel((x, y + 1))[3] if y < W - 1 else 0
            rt = src.getpixel((x + 1, y))[3] if x < W - 1 else 0
            if not dn or not rt:
                img.putpixel((x, y), darken(c, 0.24) + (255,))
            elif not up or not lf:
                img.putpixel((x, y), lighten(c, 0.22) + (255,))


def _outline(img, under):
    """Contorno da camada: fora dela, sobre o vazio ou sobre o que já existe."""
    src = img.copy()
    for y in range(W):
        for x in range(W):
            if src.getpixel((x, y))[3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < W and src.getpixel((nx, ny))[3] > 128:
                    img.putpixel((x, y), OUTL + (255,))
                    break


class Sprite:
    def __init__(self):
        self.base = Image.new("RGBA", (W, W), (0, 0, 0, 0))

    def add(self, layer):
        if layer.shade:
            _shade(layer.img)
        if layer.outline:
            _outline(layer.img, self.base)
        self.base.alpha_composite(layer.img)

    def image(self):
        return self.base


# ------------------------------------------------------------------ corpo
def body_frame(stage, lean=0, wide=0):
    """Pontos-chave do corpo por estágio. lean: inclinação do tronco (px);
    wide: alarga ombros/costelas (adultos parrudos)."""
    if stage == 1:
        f = dict(head=(16, 12.5), hr=(7.2, 6.6), ribs=(16, 22.5), rr=(3.6, 2.8), pelvis=25.5,
                 shoulder=(12.5, 20.5), shoulder_r=(19.5, 20.5), arm=5, leg=4.5, eye=2, jaw=3)
    elif stage == 2:
        f = dict(head=(16, 8.5), hr=(6.2, 5.6), ribs=(16, 17.5), rr=(4.4, 3.8), pelvis=22,
                 shoulder=(11, 14.5), shoulder_r=(21, 14.5), arm=8, leg=8, eye=2, jaw=2)
    else:
        f = dict(head=(16, 6.5), hr=(5.4, 5.0), ribs=(16, 15), rr=(5.6 + wide, 4.6), pelvis=21,
                 shoulder=(9.5 - wide, 11.5), shoulder_r=(22.5 + wide, 11.5), arm=10, leg=9, eye=2, jaw=2)
    hx, hy = f["head"]
    f["head"] = (hx + lean, hy)
    f["ribs"] = (f["ribs"][0] + lean / 2, f["ribs"][1])
    sx, sy = f["shoulder"]
    rx, ry = f["shoulder_r"]
    f["shoulder"] = (sx + lean / 2, sy)
    f["shoulder_r"] = (rx + lean / 2, ry)
    # mãos padrão (braços abaixados, levemente abertos)
    f["hand_l"] = (f["shoulder"][0] - 2, f["shoulder"][1] + f["arm"])
    f["hand_r"] = (f["shoulder_r"][0] + 2, f["shoulder_r"][1] + f["arm"])
    f["head_top"] = (f["head"][0], f["head"][1] - f["hr"][1])
    f["stage"] = stage
    return f


def draw_body(sp, f, hands=None, legs="stand", bone=BONE):
    """Esqueleto base: pernas, pelve, coluna, costelas e braços.
    hands: {"l": (x, y), "r": (x, y)} para posar os braços."""
    hands = hands or {}
    hl = hands.get("l", f["hand_l"])
    hr = hands.get("r", f["hand_r"])
    st = f["stage"]
    lay = Layer(shade=False)
    bd = darken(bone, 0.18)
    cx = f["ribs"][0]
    # pernas
    py = f["pelvis"]
    spread = 2 if st == 1 else 3
    if legs == "stand":
        for side in (-1, 1):
            x0 = cx + side * (1.5 if st == 1 else 2)
            lay.line(x0, py + 1, x0 + side * (spread - 1), GROUND - 1, bone, 2 if st == 3 else 1)
            lay.rect(int(x0 + side * (spread - 1)) - (1 if side < 0 else 0) - (1 if st > 1 else 0), GROUND - 1, 3 if st > 1 else 2, 1, bd)
    elif legs == "wide":
        for side in (-1, 1):
            x0 = cx + side * 2
            lay.line(x0, py + 1, x0 + side * (spread + 2), GROUND - 1, bone, 2 if st == 3 else 1)
            lay.rect(int(x0 + side * (spread + 2)) - 1, GROUND - 1, 3, 1, bd)
    # pelve
    lay.ell(cx, py, 3 if st == 1 else 3.6 + (0.6 if st == 3 else 0), 1.6, bone)
    # coluna
    lay.line(cx, f["ribs"][1], cx, py, bd)
    # braços
    for sh, hd in ((f["shoulder"], hl), (f["shoulder_r"], hr)):
        mx = (sh[0] + hd[0]) / 2 + (-1 if hd[0] < cx else 1)
        my = (sh[1] + hd[1]) / 2
        lay.line(sh[0], sh[1], mx, my, bone, 2 if st == 3 else 1)
        lay.line(mx, my, hd[0], hd[1], bone, 1)
        lay.ell(hd[0], hd[1], 1.2, 1.2, bone)
    # costelas
    rx, ry = f["rr"]
    lay.ell(f["ribs"][0], f["ribs"][1], rx, ry, bone)
    for i in range(1, int(ry * 2), 2):
        y = int(f["ribs"][1] - ry + i)
        for x in range(int(f["ribs"][0] - rx + 1), int(f["ribs"][0] + rx)):
            if lay.img.getpixel((x, y))[3] and abs(x + 0.5 - f["ribs"][0]) > 0.6:
                lay.px(x, y, bd)
    # ombros
    lay.line(f["shoulder"][0], f["shoulder"][1], f["shoulder_r"][0], f["shoulder_r"][1], bone, 1)
    sp.add(lay)
    return {"l": hl, "r": hr}


def draw_skull(sp, f, back=False, bone=BONE, mood="calm"):
    """Crânio com olhos (bebês: olhos grandes e brilho), nariz e mandíbula."""
    lay = Layer()
    hx, hy = f["head"]
    rx, ry = f["hr"]
    lay.ell(hx, hy, rx, ry, bone)
    # mandíbula
    jw = rx * 0.62
    lay.rect(int(hx - jw), int(hy + ry * 0.45), int(jw * 2) + 1, f["jaw"] + 1, bone)
    sp.add(lay)
    if back:
        det = Layer(shade=False, outline=False)
        det.line(hx - rx * 0.6, hy - 1, hx + rx * 0.6, hy - 1, BONE_D)
        det.px(hx + 2, hy - ry * 0.6, BONE_D)
        sp.add(det)
        return
    det = Layer(shade=False, outline=False)
    st = f["stage"]
    es = 3 if st == 1 else 2
    ey = int(hy - (0 if st == 1 else 1))
    gap = 2 if st == 1 else 2
    lx = int(hx - gap - es + 0.5)
    rx_ = int(hx + gap)
    if mood == "angry":
        det.rect(lx, ey, es, es, EYE)
        det.rect(rx_, ey, es, es, EYE)
        det.px(lx, ey - 1, EYE)
        det.px(rx_ + es - 1, ey - 1, EYE)
    elif mood == "sleepy":
        det.rect(lx, ey + 1, es, 1, EYE)
        det.rect(rx_, ey + 1, es, 1, EYE)
    else:
        det.rect(lx, ey, es, es, EYE)
        det.rect(rx_, ey, es, es, EYE)
        det.px(lx, ey, (255, 255, 255))
        det.px(rx_, ey, (255, 255, 255))
    # nariz e dentes
    ny = ey + es + (0 if st == 1 else 1)
    det.px(int(hx), ny, EYE)
    ty = int(hy + ry * 0.45) + f["jaw"] - (1 if st == 1 else 0)
    for x in range(int(hx - rx * 0.5) + 1, int(hx + rx * 0.5) + 1, 2):
        det.px(x, ty, EYE)
    sp.add(det)


def finish(sp):
    return sp.image()


def back_view(img):
    """Costas: mesma silhueta espelhada (o jogo usa a frente; a folha guarda as duas)."""
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def map_sprite(img):
    """Reduz o sprite de batalha 32×32 para o mapa (16×16): amostra por maioria
    de cor em blocos 2×2, preservando contorno e cores dominantes."""
    out = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            px = [img.getpixel((x * 2 + dx, y * 2 + dy)) for dy in (0, 1) for dx in (0, 1)]
            opaque = [p for p in px if p[3] > 128]
            if len(opaque) < 2:
                continue
            nonout = [p for p in opaque if p[:3] != OUTL]
            pool = nonout if len(nonout) >= 2 else opaque
            best = max(set(pool), key=pool.count)
            out.putpixel((x, y), best)
    # recontorna
    src = out.copy()
    for y in range(16):
        for x in range(16):
            p = src.getpixel((x, y))
            if p[3] == 0:
                continue
            edge = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < 16 and 0 <= ny < 16) or src.getpixel((nx, ny))[3] == 0:
                    edge = True
            if edge:
                out.putpixel((x, y), OUTL + (255,))
    return out
