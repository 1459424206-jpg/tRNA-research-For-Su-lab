from __future__ import annotations

import html
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "trna_structure_matched_20260604"
PDB_FILE = OUT_DIR / "1EHZ.pdb"
CLOVER_DY = 86

FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


PALETTE = {
    "acceptor": "#2F80ED",
    "d_arm": "#F2994A",
    "anticodon": "#27AE60",
    "variable": "#9B51E0",
    "t_arm": "#EB5757",
    "core": "#6B7280",
    "pair": "#9CA3AF",
    "mod": "#FFD166",
    "ink": "#111827",
    "muted": "#4B5563",
    "bg": "#FFFFFF",
}

DOMAIN_CN = {
    "acceptor": "受体臂 / 3′ CCA端",
    "d_arm": "D臂 / D环",
    "anticodon": "反密码子臂 / 环",
    "variable": "可变环",
    "t_arm": "TΨC臂 / TΨC环",
    "core": "连接区",
}

MODS = {
    10: ("m²G10", "N2-甲基鸟苷"),
    16: ("D16", "二氢尿苷"),
    17: ("D17", "二氢尿苷"),
    26: ("m²²G26", "N2,N2-二甲基鸟苷"),
    32: ("Cm32", "2′-O-甲基胞苷"),
    34: ("Gm34", "2′-O-甲基鸟苷；反密码子摆动位点"),
    37: ("yW37", "wybutosine；反密码子3′侧"),
    39: ("Ψ39", "假尿苷"),
    40: ("m⁵C40", "5-甲基胞苷"),
    46: ("m⁷G46", "7-甲基鸟苷"),
    49: ("m⁵C49", "5-甲基胞苷"),
    54: ("T54", "核糖胸苷 / 5-甲基尿苷"),
    55: ("Ψ55", "假尿苷"),
    58: ("m¹A58", "1-甲基腺苷"),
}

RES_CODE = {
    "2MG": "m²G",
    "H2U": "D",
    "M2G": "m²²G",
    "OMC": "Cm",
    "OMG": "Gm",
    "YYG": "yW",
    "PSU": "Ψ",
    "5MC": "m⁵C",
    "7MG": "m⁷G",
    "5MU": "T",
    "1MA": "m¹A",
}


def domain(pos: int) -> str:
    if 1 <= pos <= 7 or 66 <= pos <= 76:
        return "acceptor"
    if 10 <= pos <= 25:
        return "d_arm"
    if 27 <= pos <= 43:
        return "anticodon"
    if 44 <= pos <= 48:
        return "variable"
    if 49 <= pos <= 65:
        return "t_arm"
    return "core"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def lighten(hex_color: str, factor: float) -> tuple[int, int, int]:
    r, g, b = hex_to_rgb(hex_color)
    return tuple(int(c + (255 - c) * factor) for c in (r, g, b))


class Svg:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.items: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f"<title>{html.escape(title)}</title>",
            '<rect width="100%" height="100%" fill="#FFFFFF"/>',
            "<defs>",
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">',
            '<path d="M0,0 L0,6 L9,3 z" fill="#374151"/>',
            "</marker>",
            "</defs>",
        ]

    def line(self, x1, y1, x2, y2, stroke, width=2, opacity=1.0, dash=None, arrow=False):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        self.items.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" opacity="{opacity}"{dash_attr}{marker}/>'
        )

    def polyline(self, pts, stroke, width=3, fill="none", opacity=1.0):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.items.append(
            f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'
        )

    def circle(self, x, y, r, fill, stroke="#FFFFFF", width=1.5, opacity=1.0):
        self.items.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{width}" opacity="{opacity}"/>'
        )

    def rect(self, x, y, w, h, fill, stroke="none", width=1, rx=8, opacity=1.0):
        self.items.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"/>'
        )

    def text(self, x, y, txt, size=24, fill="#111827", weight="400", anchor="middle"):
        escaped = html.escape(txt)
        self.items.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="Microsoft YaHei, SimHei, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'dominant-baseline="middle">{escaped}</text>'
        )

    def save(self, path: Path):
        path.write_text("\n".join(self.items + ["</svg>"]), encoding="utf-8")


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill="#111827",
    anchor="mm",
    box=False,
):
    x, y = xy
    if box:
        bbox = draw.textbbox((x, y), text, font=fnt, anchor=anchor)
        pad = 7
        draw.rounded_rectangle(
            (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad),
            radius=8,
            fill=(255, 255, 255, 230),
            outline=(229, 231, 235, 240),
            width=1,
        )
    draw.text((x, y), text, font=fnt, fill=fill, anchor=anchor)


def arrow(draw: ImageDraw.ImageDraw, p1, p2, fill="#374151", width=2):
    draw.line([p1, p2], fill=fill, width=width)
    x1, y1 = p1
    x2, y2 = p2
    ang = math.atan2(y2 - y1, x2 - x1)
    l = 12
    pts = [
        (x2, y2),
        (x2 - l * math.cos(ang - math.pi / 6), y2 - l * math.sin(ang - math.pi / 6)),
        (x2 - l * math.cos(ang + math.pi / 6), y2 - l * math.sin(ang + math.pi / 6)),
    ]
    draw.polygon(pts, fill=fill)


def cloverleaf_coords() -> dict[int, tuple[float, float]]:
    coords: dict[int, tuple[float, float]] = {}
    for i in range(1, 8):
        coords[i] = (760, 120 + (i - 1) * 35)
    for i in range(66, 73):
        coords[i] = (950, 120 + (72 - i) * 35)

    coords.update(
        {
            8: (720, 365),
            9: (650, 385),
            10: (590, 410),
            11: (560, 438),
            12: (535, 470),
            13: (520, 505),
            14: (500, 560),
            15: (450, 600),
            16: (395, 585),
            17: (365, 535),
            18: (385, 480),
            19: (435, 455),
            20: (500, 462),
            21: (555, 485),
            22: (625, 505),
            23: (642, 470),
            24: (668, 438),
            25: (695, 410),
            26: (735, 380),
        }
    )

    for idx, pos in enumerate(range(27, 32)):
        coords[pos] = (790 - idx * 5, 410 + idx * 40)
    coords.update(
        {
            32: (720, 602),
            33: (695, 652),
            34: (725, 705),
            35: (780, 727),
            36: (835, 705),
            37: (865, 652),
            38: (840, 602),
        }
    )
    for idx, pos in enumerate(range(39, 44)):
        coords[pos] = (850 - idx * 5, 570 - idx * 40)

    coords.update(
        {
            44: (890, 385),
            45: (940, 365),
            46: (990, 380),
            47: (1030, 410),
            48: (1060, 440),
            49: (1110, 410),
            50: (1135, 438),
            51: (1160, 470),
            52: (1175, 505),
            53: (1185, 540),
            54: (1235, 570),
            55: (1290, 570),
            56: (1325, 535),
            57: (1320, 485),
            58: (1285, 450),
            59: (1235, 450),
            60: (1195, 480),
            61: (1285, 540),
            62: (1275, 505),
            63: (1260, 470),
            64: (1235, 438),
            65: (1210, 410),
            73: (1010, 95),
            74: (1065, 72),
            75: (1120, 58),
            76: (1175, 58),
        }
    )
    return {pos: (x, y + CLOVER_DY) for pos, (x, y) in coords.items()}


PAIRINGS = [
    (1, 72),
    (2, 71),
    (3, 70),
    (4, 69),
    (5, 68),
    (6, 67),
    (7, 66),
    (10, 25),
    (11, 24),
    (12, 23),
    (13, 22),
    (27, 43),
    (28, 42),
    (29, 41),
    (30, 40),
    (31, 39),
    (49, 65),
    (50, 64),
    (51, 63),
    (52, 62),
    (53, 61),
]


def get_residue_names() -> dict[int, str]:
    names: dict[int, str] = {}
    with PDB_FILE.open() as fh:
        for line in fh:
            if not line.startswith(("ATOM", "HETATM")):
                continue
            if line[21].strip() != "A":
                continue
            try:
                pos = int(line[22:26])
            except ValueError:
                continue
            if 1 <= pos <= 76 and pos not in names:
                names[pos] = line[17:20].strip()
    return names


def base_label(pos: int, names: dict[int, str]) -> str:
    name = names.get(pos, "")
    return RES_CODE.get(name, name if name in {"A", "C", "G", "U"} else str(pos))


def draw_legend(draw, x, y, scale=1.0):
    title_font = font(int(27 * scale), True)
    body_font = font(int(22 * scale))
    draw_text(draw, (x, y), "统一颜色标注", title_font, anchor="la")
    yy = y + 42 * scale
    for key in ["acceptor", "d_arm", "anticodon", "variable", "t_arm", "core"]:
        c = hex_to_rgb(PALETTE[key])
        draw.rounded_rectangle((x, yy - 14, x + 32 * scale, yy + 14), radius=6, fill=c)
        draw_text(draw, (x + 44 * scale, yy), DOMAIN_CN[key], body_font, anchor="lm", fill=PALETTE["ink"])
        yy += 36 * scale


def draw_mod_table(draw, x, y, scale=1.0, cols=2):
    title_font = font(int(25 * scale), True)
    small = font(int(17 * scale))
    draw_text(draw, (x, y), "1EHZ 中标出的修饰核苷", title_font, anchor="la")
    items = list(MODS.items())
    row_h = 30 * scale
    col_w = 355 * scale
    for idx, (pos, (abbr, name)) in enumerate(items):
        col = idx // 7 if cols == 2 else 0
        row = idx % 7 if cols == 2 else idx
        xx = x + col * col_w
        yy = y + 37 * scale + row * row_h
        draw.ellipse((xx, yy - 9, xx + 18 * scale, yy + 9), fill=hex_to_rgb(PALETTE["mod"]), outline=(120, 76, 0), width=1)
        draw_text(draw, (xx + 28 * scale, yy), f"{abbr}: {name}", small, anchor="lm", fill=PALETTE["ink"])


def draw_2d_png(names: dict[int, str], path: Path):
    s = 2
    W, H = 1800, 1280
    im = Image.new("RGB", (W * s, H * s), "white")
    draw = ImageDraw.Draw(im, "RGBA")
    coords = {k: (v[0] * s, v[1] * s) for k, v in cloverleaf_coords().items()}

    title_f = font(38 * s, True)
    subtitle_f = font(22 * s)
    label_f = font(25 * s, True)
    small_f = font(17 * s)
    tiny_f = font(13 * s)

    draw_text(draw, (90 * s, 50 * s), "tRNA 二级结构：三叶草模型（酵母 tRNA^Phe，PDB 1EHZ 对照）", title_f, anchor="la")
    draw_text(draw, (90 * s, 88 * s), "颜色与右侧 3D 结构一致；黄色圆点为该结构中解析到的重要修饰核苷。", subtitle_f, anchor="la", fill=PALETTE["muted"])

    for a, b in PAIRINGS:
        draw.line([coords[a], coords[b]], fill=hex_to_rgb(PALETTE["pair"]) + (170,), width=3 * s)

    for i in range(1, 76):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        draw.line([(x1, y1), (x2, y2)], fill=hex_to_rgb(PALETTE[domain(i)]) + (220,), width=7 * s)

    for pos in range(1, 77):
        x, y = coords[pos]
        fill = hex_to_rgb(PALETTE[domain(pos)])
        r = 15 * s
        if pos in MODS:
            draw.ellipse((x - (r + 7), y - (r + 7), x + (r + 7), y + (r + 7)), fill=hex_to_rgb(PALETTE["mod"]) + (255,), outline=(120, 76, 0, 255), width=2 * s)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill + (255,), outline=(255, 255, 255, 255), width=3 * s)
        label = base_label(pos, names)
        draw_text(draw, (x, y), label, tiny_f, fill="white")
        if pos in {1, 7, 10, 16, 17, 26, 32, 34, 37, 39, 40, 46, 49, 54, 55, 58, 66, 72, 73, 76}:
            draw_text(draw, (x, y + 26 * s), str(pos), tiny_f, fill=PALETTE["ink"])

    annotations = [
        ("5′端", (690, 96 + CLOVER_DY), (758, 120 + CLOVER_DY)),
        ("3′ CCA氨基酸接受端", (1210, 104 + CLOVER_DY), (1118, 60 + CLOVER_DY)),
        ("受体臂", (850, 308 + CLOVER_DY), (855, 225 + CLOVER_DY)),
        ("D环", (250, 760), (396, 585 + CLOVER_DY)),
        ("反密码子 GmAA (34-36)", (640, 780 + CLOVER_DY), (780, 725 + CLOVER_DY)),
        ("可变环", (1090, 365), (990, 380 + CLOVER_DY)),
        ("TΨC环", (1375, 590 + CLOVER_DY), (1290, 570 + CLOVER_DY)),
    ]
    for txt, txy, pxy in annotations:
        arrow(draw, (txy[0] * s, txy[1] * s), (pxy[0] * s, pxy[1] * s), width=2 * s)
        draw_text(draw, (txy[0] * s, txy[1] * s), txt, label_f, anchor="mm", box=True)

    mod_offsets = {
        10: (-55, -38),
        16: (-64, 18),
        17: (-68, 38),
        26: (12, -48),
        32: (-70, -10),
        34: (-45, 38),
        37: (52, 38),
        39: (64, 0),
        40: (68, 0),
        46: (0, -52),
        49: (10, -52),
        54: (0, 50),
        55: (34, 50),
        58: (38, -48),
    }
    for pos, (abbr, _) in MODS.items():
        x, y = coords[pos]
        dx, dy = mod_offsets[pos]
        tx, ty = x + dx * s, y + dy * s
        draw.line([(x, y), (tx, ty)], fill=(120, 76, 0, 180), width=1 * s)
        draw_text(draw, (tx, ty), abbr, small_f, fill="#5B3A00")

    draw_legend(draw, 1325 * s, 255 * s, scale=s)
    draw_mod_table(draw, 108 * s, 965 * s, scale=s, cols=2)

    im = im.resize((W, H), Image.Resampling.LANCZOS)
    im.save(path, dpi=(300, 300))


def draw_2d_svg(names: dict[int, str], path: Path):
    W, H = 1800, 1280
    svg = Svg(W, H, "tRNA 2D cloverleaf with Chinese annotations")
    coords = cloverleaf_coords()
    svg.text(90, 50, "tRNA 二级结构：三叶草模型（酵母 tRNA^Phe，PDB 1EHZ 对照）", 38, weight="700", anchor="start")
    svg.text(90, 88, "颜色与右侧 3D 结构一致；黄色圆点为该结构中解析到的重要修饰核苷。", 22, fill=PALETTE["muted"], anchor="start")
    for a, b in PAIRINGS:
        svg.line(*coords[a], *coords[b], PALETTE["pair"], width=2.5, opacity=0.7)
    for i in range(1, 76):
        svg.line(*coords[i], *coords[i + 1], PALETTE[domain(i)], width=7, opacity=0.9)
    for pos in range(1, 77):
        x, y = coords[pos]
        if pos in MODS:
            svg.circle(x, y, 22, PALETTE["mod"], stroke="#784C00", width=1.8)
        svg.circle(x, y, 15, PALETTE[domain(pos)], stroke="#FFFFFF", width=2.4)
        svg.text(x, y + 1, base_label(pos, names), 13, fill="#FFFFFF")
        if pos in {1, 7, 10, 16, 17, 26, 32, 34, 37, 39, 40, 46, 49, 54, 55, 58, 66, 72, 73, 76}:
            svg.text(x, y + 27, str(pos), 13, fill=PALETTE["ink"])

    annotations = [
        ("5′端", (690, 96 + CLOVER_DY), (758, 120 + CLOVER_DY)),
        ("3′ CCA氨基酸接受端", (1210, 104 + CLOVER_DY), (1118, 60 + CLOVER_DY)),
        ("受体臂", (850, 308 + CLOVER_DY), (855, 225 + CLOVER_DY)),
        ("D环", (250, 760), (396, 585 + CLOVER_DY)),
        ("反密码子 GmAA (34-36)", (640, 780 + CLOVER_DY), (780, 725 + CLOVER_DY)),
        ("可变环", (1090, 365), (990, 380 + CLOVER_DY)),
        ("TΨC环", (1375, 590 + CLOVER_DY), (1290, 570 + CLOVER_DY)),
    ]
    for txt, txy, pxy in annotations:
        svg.line(txy[0], txy[1], pxy[0], pxy[1], "#374151", width=2, arrow=True)
        svg.rect(txy[0] - 90, txy[1] - 19, 180, 38, "#FFFFFF", "#E5E7EB", rx=8, opacity=0.94)
        svg.text(txy[0], txy[1], txt, 25, weight="700")

    mod_offsets = {
        10: (-55, -38),
        16: (-64, 18),
        17: (-68, 38),
        26: (12, -48),
        32: (-70, -10),
        34: (-45, 38),
        37: (52, 38),
        39: (64, 0),
        40: (68, 0),
        46: (0, -52),
        49: (10, -52),
        54: (0, 50),
        55: (34, 50),
        58: (38, -48),
    }
    for pos, (abbr, _) in MODS.items():
        x, y = coords[pos]
        dx, dy = mod_offsets[pos]
        tx, ty = x + dx, y + dy
        svg.line(x, y, tx, ty, "#784C00", width=1, opacity=0.7)
        svg.text(tx, ty, abbr, 17, fill="#5B3A00")

    svg.text(1325, 255, "统一颜色标注", 27, weight="700", anchor="start")
    yy = 297
    for key in ["acceptor", "d_arm", "anticodon", "variable", "t_arm", "core"]:
        svg.rect(1325, yy - 14, 32, 28, PALETTE[key], rx=6)
        svg.text(1369, yy, DOMAIN_CN[key], 22, anchor="start")
        yy += 36

    svg.text(108, 965, "1EHZ 中标出的修饰核苷", 25, weight="700", anchor="start")
    for idx, (pos, (abbr, name)) in enumerate(MODS.items()):
        col = idx // 7
        row = idx % 7
        xx = 108 + col * 355
        yy = 1002 + row * 30
        svg.circle(xx + 9, yy, 9, PALETTE["mod"], stroke="#784C00", width=1)
        svg.text(xx + 28, yy, f"{abbr}: {name}", 17, anchor="start")
    svg.save(path)


def parse_backbone_coords() -> tuple[np.ndarray, dict[int, str]]:
    res_atoms: dict[int, dict[str, object]] = {}
    with PDB_FILE.open() as fh:
        for line in fh:
            if not line.startswith(("ATOM", "HETATM")) or line[21].strip() != "A":
                continue
            try:
                pos = int(line[22:26])
            except ValueError:
                continue
            if not (1 <= pos <= 76):
                continue
            atom = line[12:16].strip()
            resn = line[17:20].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            entry = res_atoms.setdefault(pos, {"name": resn, "atoms": [], "c4": None})
            entry["atoms"].append((x, y, z))
            if atom == "C4'":
                entry["c4"] = (x, y, z)

    coords = []
    names = {}
    for pos in range(1, 77):
        entry = res_atoms[pos]
        names[pos] = str(entry["name"])
        coords.append(entry["c4"] or tuple(np.mean(np.array(entry["atoms"]), axis=0)))
    return np.array(coords, dtype=float), names


def project_3d(coords: np.ndarray, width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    coords = coords - coords.mean(axis=0)
    cov = np.cov(coords.T)
    vals, vecs = np.linalg.eigh(cov)
    vecs = vecs[:, vals.argsort()[::-1]]
    q = coords @ vecs
    theta = math.radians(24)
    phi = math.radians(-12)
    ry = np.array([[math.cos(theta), 0, math.sin(theta)], [0, 1, 0], [-math.sin(theta), 0, math.cos(theta)]])
    rx = np.array([[1, 0, 0], [0, math.cos(phi), -math.sin(phi)], [0, math.sin(phi), math.cos(phi)]])
    q = q @ ry.T @ rx.T
    xy = q[:, :2]
    z = q[:, 2]
    min_xy = xy.min(axis=0)
    max_xy = xy.max(axis=0)
    scale = min((width - 530) / (max_xy[0] - min_xy[0]), (height - 300) / (max_xy[1] - min_xy[1]))
    screen = np.empty_like(xy)
    screen[:, 0] = (xy[:, 0] - min_xy[0]) * scale + 150
    screen[:, 1] = (max_xy[1] - xy[:, 1]) * scale + 185
    return screen, z


def draw_3d_png(path: Path):
    s = 2
    W, H = 1800, 1280
    coords, names = parse_backbone_coords()
    pts, depth = project_3d(coords, W, H)
    pts_s = pts * s
    im = Image.new("RGB", (W * s, H * s), "white")
    draw = ImageDraw.Draw(im, "RGBA")

    title_f = font(38 * s, True)
    subtitle_f = font(22 * s)
    label_f = font(25 * s, True)
    small_f = font(17 * s)
    tiny_f = font(13 * s)

    draw_text(draw, (90 * s, 50 * s), "tRNA 三级结构：L 型折叠（PDB 1EHZ 坐标投影）", title_f, anchor="la")
    draw_text(draw, (90 * s, 88 * s), "骨架按残基顺序连接；颜色与 2D 图相同，黄色编号为相同修饰位点。", subtitle_f, anchor="la", fill=PALETTE["muted"])

    order_segments = sorted(range(1, 76), key=lambda i: (depth[i - 1] + depth[i]) / 2)
    z_min, z_max = float(depth.min()), float(depth.max())
    for i in order_segments:
        p1 = tuple(pts_s[i - 1])
        p2 = tuple(pts_s[i])
        dz = ((depth[i - 1] + depth[i]) / 2 - z_min) / (z_max - z_min + 1e-9)
        color = lighten(PALETTE[domain(i)], 0.38 - 0.25 * dz)
        draw.line([p1, p2], fill=color + (230,), width=int((10 + 4 * dz) * s))

    for pos in sorted(range(1, 77), key=lambda p: depth[p - 1]):
        x, y = pts_s[pos - 1]
        dz = (depth[pos - 1] - z_min) / (z_max - z_min + 1e-9)
        fill = lighten(PALETTE[domain(pos)], 0.32 - 0.18 * dz)
        r = (8 + 3 * dz) * s
        if pos in MODS:
            draw.ellipse((x - r - 7 * s, y - r - 7 * s, x + r + 7 * s, y + r + 7 * s), fill=hex_to_rgb(PALETTE["mod"]) + (245,), outline=(120, 76, 0, 255), width=2 * s)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill + (255,), outline=(255, 255, 255, 230), width=2 * s)
        if pos in MODS:
            draw_text(draw, (x, y), str(pos), tiny_f, fill="#111827")

    domain_targets = {
        "受体臂 / CCA端": (72, (1130, 1035)),
        "D臂": (16, (1015, 370)),
        "反密码子环": (35, (380, 990)),
        "可变环": (46, (720, 520)),
        "TΨC环": (55, (1190, 245)),
    }
    for txt, (pos, txy) in domain_targets.items():
        x, y = pts_s[pos - 1]
        arrow(draw, (txy[0] * s, txy[1] * s), (x, y), width=2 * s)
        draw_text(draw, (txy[0] * s, txy[1] * s), txt, label_f, box=True)

    draw_text(draw, (1295 * s, 110 * s), "3D 中的黄色数字 = 2D 中相同修饰编号", font(22 * s, True), anchor="la", fill=PALETTE["ink"])
    draw_mod_table(draw, 1295 * s, 160 * s, scale=s, cols=1)
    draw_legend(draw, 1295 * s, 690 * s, scale=s)

    footer = "坐标来源：RCSB PDB 1EHZ；显示为正交投影，非空间填充模型。"
    draw_text(draw, (90 * s, 1225 * s), footer, subtitle_f, anchor="la", fill=PALETTE["muted"])

    im = im.resize((W, H), Image.Resampling.LANCZOS)
    im.save(path, dpi=(300, 300))


def draw_3d_svg(path: Path):
    W, H = 1800, 1280
    coords, _names = parse_backbone_coords()
    pts, depth = project_3d(coords, W, H)
    z_min, z_max = float(depth.min()), float(depth.max())
    svg = Svg(W, H, "tRNA 3D structure projection with Chinese annotations")
    svg.text(90, 50, "tRNA 三级结构：L 型折叠（PDB 1EHZ 坐标投影）", 38, weight="700", anchor="start")
    svg.text(90, 88, "骨架按残基顺序连接；颜色与 2D 图相同，黄色编号为相同修饰位点。", 22, fill=PALETTE["muted"], anchor="start")

    order_segments = sorted(range(1, 76), key=lambda i: (depth[i - 1] + depth[i]) / 2)
    for i in order_segments:
        dz = ((depth[i - 1] + depth[i]) / 2 - z_min) / (z_max - z_min + 1e-9)
        c = lighten(PALETTE[domain(i)], 0.38 - 0.25 * dz)
        stroke = "#%02x%02x%02x" % c
        svg.line(*pts[i - 1], *pts[i], stroke, width=10 + 4 * dz, opacity=0.9)

    for pos in sorted(range(1, 77), key=lambda p: depth[p - 1]):
        x, y = pts[pos - 1]
        dz = (depth[pos - 1] - z_min) / (z_max - z_min + 1e-9)
        c = lighten(PALETTE[domain(pos)], 0.32 - 0.18 * dz)
        fill = "#%02x%02x%02x" % c
        r = 8 + 3 * dz
        if pos in MODS:
            svg.circle(x, y, r + 7, PALETTE["mod"], stroke="#784C00", width=1.8)
        svg.circle(x, y, r, fill, stroke="#FFFFFF", width=1.8)
        if pos in MODS:
            svg.text(x, y + 1, str(pos), 13, fill="#111827")

    domain_targets = {
        "受体臂 / CCA端": (72, (1130, 1035)),
        "D臂": (16, (1015, 370)),
        "反密码子环": (35, (380, 990)),
        "可变环": (46, (720, 520)),
        "TΨC环": (55, (1190, 245)),
    }
    for txt, (pos, txy) in domain_targets.items():
        x, y = pts[pos - 1]
        svg.line(txy[0], txy[1], x, y, "#374151", width=2, arrow=True)
        svg.rect(txy[0] - 85, txy[1] - 19, 170, 38, "#FFFFFF", "#E5E7EB", rx=8, opacity=0.94)
        svg.text(txy[0], txy[1], txt, 25, weight="700")

    svg.text(1295, 110, "3D 中的黄色数字 = 2D 中相同修饰编号", 22, weight="700", anchor="start")
    svg.text(1295, 160, "1EHZ 中标出的修饰核苷", 25, weight="700", anchor="start")
    for idx, (pos, (abbr, name)) in enumerate(MODS.items()):
        yy = 197 + idx * 30
        svg.circle(1304, yy, 9, PALETTE["mod"], stroke="#784C00", width=1)
        svg.text(1323, yy, f"{abbr}: {name}", 17, anchor="start")

    svg.text(1295, 690, "统一颜色标注", 27, weight="700", anchor="start")
    yy = 732
    for key in ["acceptor", "d_arm", "anticodon", "variable", "t_arm", "core"]:
        svg.rect(1295, yy - 14, 32, 28, PALETTE[key], rx=6)
        svg.text(1339, yy, DOMAIN_CN[key], 22, anchor="start")
        yy += 36
    svg.text(90, 1225, "坐标来源：RCSB PDB 1EHZ；显示为正交投影，非空间填充模型。", 22, fill=PALETTE["muted"], anchor="start")
    svg.save(path)


def make_combined(two_d: Path, three_d: Path, out: Path):
    left = Image.open(two_d).convert("RGB")
    right = Image.open(three_d).convert("RGB")
    scale = 0.58
    left = left.resize((int(left.width * scale), int(left.height * scale)), Image.Resampling.LANCZOS)
    right = right.resize((int(right.width * scale), int(right.height * scale)), Image.Resampling.LANCZOS)
    gap = 26
    pad = 28
    title_h = 0
    W = left.width + right.width + gap + 2 * pad
    H = max(left.height, right.height) + 2 * pad + title_h
    im = Image.new("RGB", (W, H), "white")
    im.paste(left, (pad, pad + title_h))
    im.paste(right, (pad + left.width + gap, pad + title_h))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((pad - 10, pad - 10, pad + left.width + 10, pad + left.height + 10), radius=12, outline=(229, 231, 235), width=2)
    x2 = pad + left.width + gap
    draw.rounded_rectangle((x2 - 10, pad - 10, x2 + right.width + 10, pad + right.height + 10), radius=12, outline=(229, 231, 235), width=2)
    im.save(out, dpi=(300, 300))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not PDB_FILE.exists():
        raise FileNotFoundError(f"Missing {PDB_FILE}. Download 1EHZ.pdb from RCSB first.")
    names = get_residue_names()
    draw_2d_png(names, OUT_DIR / "tRNA_2D_cloverleaf_CN_matched.png")
    draw_2d_svg(names, OUT_DIR / "tRNA_2D_cloverleaf_CN_matched.svg")
    draw_3d_png(OUT_DIR / "tRNA_3D_Lshape_CN_matched.png")
    draw_3d_svg(OUT_DIR / "tRNA_3D_Lshape_CN_matched.svg")
    make_combined(
        OUT_DIR / "tRNA_2D_cloverleaf_CN_matched.png",
        OUT_DIR / "tRNA_3D_Lshape_CN_matched.png",
        OUT_DIR / "tRNA_2D_3D_CN_matched_combined.png",
    )
    print(f"Wrote files to {OUT_DIR}")


if __name__ == "__main__":
    main()
