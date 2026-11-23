# GPU 글자 렌더링 비교 장난감 (jpcorps.com 2026-11-24 글)
# 비트맵 아틀라스 / SDF / 외곽선 직접 계산(광선 교차 세기)을 파이썬으로 흉내 낸다.
# 실행: python3 make_figures.py   (numpy, scipy, matplotlib, fontTools 필요)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from scipy.ndimage import map_coordinates

KO = font_manager.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = KO.get_name()
font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def glyph_curves(ch):
    """글자 외곽선을 2차 베지어 (p0, p1, p2) 목록으로. 직선은 p1 = 중점."""
    f = TTFont(FONT)
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord(ch)]
    pen = RecordingPen()
    gs[name].draw(pen)
    curves, start, cur = [], None, None
    for op, args in pen.value:
        if op == "moveTo":
            start = cur = np.array(args[0], float)
        elif op == "lineTo":
            p = np.array(args[0], float)
            curves.append((cur, (cur + p) / 2, p)); cur = p
        elif op == "qCurveTo":
            pts = [np.array(a, float) for a in args]
            if args[-1] is None:
                raise ValueError("implied on-curve contour not handled")
            offs, end = pts[:-1], pts[-1]
            for i, c in enumerate(offs):
                nxt = end if i == len(offs) - 1 else (c + offs[i + 1]) / 2
                curves.append((cur, c, nxt)); cur = nxt
        elif op in ("closePath", "endPath"):
            if np.linalg.norm(cur - start) > 1e-9:
                curves.append((cur, (cur + start) / 2, start))
            cur = start
    return np.array(curves), f["head"].unitsPerEm

def winding(curves, x, y):
    """점 (x, y) 에서 +x 방향 광선을 쏴서 외곽선 교차를 방향 붙여 센다 (Slug 의 핵심 생각을 단순하게)."""
    w = np.zeros_like(x)
    for p0, p1, p2 in curves:
        # y(t) = a t^2 + b t + c = y
        a = p0[1] - 2 * p1[1] + p2[1]
        b = 2 * (p1[1] - p0[1])
        c = p0[1] - y
        ts = []
        if abs(a) < 1e-9:
            if abs(b) > 1e-9:
                ts.append(-c / b + 0 * y)
        else:
            disc = b * b - 4 * a * c
            ok = disc >= 0
            sq = np.sqrt(np.where(ok, disc, 0))
            ts.append(np.where(ok, (-b - sq) / (2 * a), -1))
            ts.append(np.where(ok, (-b + sq) / (2 * a), -1))
        for t in ts:
            valid = (t >= 0) & (t < 1)   # 끝점은 한쪽만 세서 이음매가 두 번 세지지 않게
            xt = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
            hit = valid & (xt > x) & (dy != 0)
            w += np.where(hit, np.sign(dy), 0)
    return w

def flatten(curves, n=24):
    t = np.linspace(0, 1, n + 1)[:, None]
    segs = []
    for p0, p1, p2 in curves:
        pts = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
        segs += [(pts[i], pts[i + 1]) for i in range(n)]
    return np.array(segs)

def dist_to_outline(segs, x, y):
    d = np.full(x.shape, np.inf)
    P = np.stack([x, y], -1)
    for a, b in segs:
        ab = b - a
        t = np.clip(((P - a) @ ab) / (ab @ ab + 1e-12), 0, 1)
        q = a + t[..., None] * ab
        d = np.minimum(d, np.linalg.norm(P - q, axis=-1))
    return d

curves, upem = glyph_curves("A")
segs = flatten(curves)
# 글자 주변 사각형 (폰트 단위)
x0, x1 = curves[..., 0].min(), curves[..., 0].max()
y0, y1 = curves[..., 1].min(), curves[..., 1].max()
pad = 0.08 * upem
X0, X1, Y0, Y1 = x0 - pad, x1 + pad, y0 - pad, y1 + pad

SMALL = 24      # 작은 텍스처 해상도 (가로 픽셀)

def grid(n):
    """n×n 픽셀 중심 좌표 (위가 y 큰 쪽)"""
    s = (X1 - X0) / n
    hs = int(round((Y1 - Y0) / ((X1 - X0) / SMALL)))
    h = hs * (n // SMALL)   # 작은 격자와 큰 격자의 위아래가 딱 맞게
    xs = X0 + (np.arange(n) + 0.5) * s
    ys = Y1 - (np.arange(h) + 0.5) * s
    return np.meshgrid(xs, ys), s

def coverage(n, ss=4):
    (gx, gy), s = grid(n)
    acc = np.zeros_like(gx)
    for i in range(ss):
        for j in range(ss):
            ox = (i + 0.5) / ss - 0.5; oy = (j + 0.5) / ss - 0.5
            acc += winding(curves, gx + ox * s, gy + oy * s) != 0
    return acc / (ss * ss)

SPREAD = 3

def sdf(n):
    (gx, gy), s = grid(n)
    d = dist_to_outline(segs, gx, gy)
    inside = winding(curves, gx, gy) != 0
    sd = np.where(inside, d, -d) / s     # 단위: 작은 텍스처의 텍셀
    return np.clip(sd, -SPREAD, SPREAD)  # 실제 SDF 폰트처럼 경계 근처 몇 텍셀만 담는다

BIG = 480       # 크게 확대해서 그릴 해상도
ratio = BIG / SMALL

def upsample(img, n_big):
    h, w = img.shape
    H = int(round(h * n_big / w))
    yy, xx = np.mgrid[0:H, 0:n_big]
    sx = (xx + 0.5) / (n_big / w) - 0.5
    sy = (yy + 0.5) / (n_big / w) - 0.5
    return map_coordinates(img, [sy, sx], order=1, mode="nearest")

def nearest_up(img, n_big):
    k = n_big // img.shape[1]
    return np.kron(img, np.ones((k, k)))

atlas = coverage(SMALL)
field = sdf(SMALL)
field_big = upsample(field, BIG)
# 텍셀 단위 거리 → 화면 픽셀 단위로 바꿔 1픽셀 폭 부드러운 경계
sdf_img = np.clip(field_big * ratio + 0.5, 0, 1)
exact = coverage(BIG, ss=3)

out = "./"
# 그림 1: 같은 글자를 20배 키웠을 때
fig, axs = plt.subplots(1, 4, figsize=(13, 4.2))
for ax, img, t in zip(axs,
    [nearest_up(atlas, BIG), upsample(atlas, BIG), sdf_img, exact],
    [f"① 비트맵 {SMALL}px\n그냥 확대(가장 가까운 점)", f"② 비트맵 {SMALL}px\n부드럽게 확대(쌍선형)",
     f"③ SDF {SMALL}px\n확대 후 0에서 자르기", "④ 외곽선에서 바로 계산\n(광선 교차 세기)"]):
    ax.imshow(img, cmap="gray_r", vmin=0, vmax=1, interpolation="nearest")
    ax.set_title(t, fontsize=11); ax.axis("off")
fig.suptitle(f"같은 'A' 를 {SMALL}픽셀짜리 텍스처에서 {BIG}픽셀로 키우면", fontsize=13)
fig.tight_layout(); fig.savefig(out + "fig1_magnify.png", dpi=110); plt.close(fig)

# 그림 2: SDF 텍스처가 담고 있는 것
fig, axs = plt.subplots(1, 3, figsize=(12, 4.4))
v = SPREAD
im = axs[0].imshow(field, cmap="RdBu", vmin=-v, vmax=v, interpolation="nearest")
axs[0].set_title(f"{SMALL}×{field.shape[0]} SDF 텍스처 (실제 저장되는 것)\n파랑=글자 안(+), 빨강=밖(−), ±3텍셀까지만", fontsize=10.5)
axs[0].axis("off")
axs[1].imshow(field_big, cmap="RdBu", vmin=-v, vmax=v)
axs[1].contour(field_big, levels=[0], colors="k", linewidths=1.5)
axs[1].set_title("쌍선형으로 확대한 값 + 0 이 되는 선", fontsize=10.5); axs[1].axis("off")
axs[2].imshow(sdf_img, cmap="gray_r", vmin=0, vmax=1)
axs[2].set_title("0 보다 크면 칠하기 → 매끈한 글자", fontsize=10.5); axs[2].axis("off")
fig.tight_layout(); fig.savefig(out + "fig2_sdf_field.png", dpi=110); plt.close(fig)

# 그림 3: 꼭짓점 확대 (A 의 꼭대기)
H = exact.shape[0]
top = slice(int(H * 0.22), int(H * 0.58)); mid = slice(int(BIG * 0.32), int(BIG * 0.68))
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
axs[0].imshow(sdf_img[top, mid], cmap="gray_r", vmin=0, vmax=1)
axs[0].set_title("SDF: 꼭짓점이 동글동글", fontsize=12); axs[0].axis("off")
axs[1].imshow(exact[top, mid], cmap="gray_r", vmin=0, vmax=1)
axs[1].set_title("외곽선 직접 계산: 꼭짓점이 뾰족", fontsize=12); axs[1].axis("off")
fig.suptitle("'A' 가운데 구멍(삼각형)만 크게 보면", fontsize=13)
fig.tight_layout(); fig.savefig(out + "fig3_corner.png", dpi=110); plt.close(fig)

# 그림 4: 광선 교차 세기
fig, ax = plt.subplots(figsize=(7, 6.5))
t = np.linspace(0, 1, 30)[:, None]
for p0, p1, p2 in curves:
    pts = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
    ax.plot(pts[:, 0], pts[:, 1], "k-", lw=2)
    mid_ = pts[15]; d = pts[16] - pts[14]
    ax.annotate("", xy=mid_ + d * 0.8, xytext=mid_, arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
yline = y0 + 0.62 * (y1 - y0)
probe = [(x0 + 0.06 * (x1 - x0), "밖"), (x0 + 0.27 * (x1 - x0), "안"), (x0 + 0.50 * (x1 - x0), "밖 (구멍)")]
colors = ["tab:red", "tab:blue", "tab:green"]
for (px, lab), col in zip(probe, colors):
    yy = yline + (probe.index((px, lab)) - 1) * 0.035 * upem
    w = winding(curves, np.array([px]), np.array([yy]))[0]
    ax.plot([px, X1], [yy, yy], "-", color=col, lw=1.5, alpha=0.8)
    ax.plot(X1, yy, ">", color=col, ms=8)
    ax.plot(px, yy, "o", color=col, ms=9)
    ax.text(px, yy + 0.02 * upem, f"합계 {int(w):+d} → {lab}", color=col, fontsize=11, ha="left")
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("픽셀에서 오른쪽으로 광선을 쏴서\n외곽선을 위로 넘으면 +1, 아래로 넘으면 −1 → 합이 0 이 아니면 안", fontsize=12)
fig.tight_layout(); fig.savefig(out + "fig4_winding.png", dpi=110); plt.close(fig)

# 확인용 숫자
print("curves", len(curves), "sdf shape", field.shape, "atlas shape", atlas.shape)
print("exact vs sdf mean abs diff", np.abs(exact - sdf_img[:exact.shape[0], :exact.shape[1]]).mean())
print("exact vs bilinear atlas mean abs diff", np.abs(exact - upsample(atlas, BIG)[:exact.shape[0], :exact.shape[1]]).mean())
