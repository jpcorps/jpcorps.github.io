# VORTEXEL (1) 글의 그림을 만드는 스크립트 (2D 로 단순화한 설명용 그림)
# 실행: python3 make_figures.py  → 같은 폴더에 png 4장
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import font_manager as fm

for f in fm.findSystemFonts():
    if "NotoSansCJK-Regular" in f:
        fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))

VOX = 0.5                 # 블록 한 칸 0.5m
W, H = 24.0, 12.0         # 2D 장면 크기 (m)
NX, NY = int(W / VOX), int(H / VOX)

# ---- 장면: 언덕 지면 + 바위 + 지붕(얇은 판) -------------------------
ground = [(0, 2.0), (4, 2.3), (7, 4.2), (9.5, 4.6), (12, 3.0), (24, 2.6)]
rock = [(15.2, 2.8), (15.2, 6.1), (17.8, 6.1), (17.8, 2.7)]
roof = [(18.6, 6.4), (21.0, 8.6), (23.4, 6.4)]
segments = []
for poly in (ground, rock, roof):
    segments += list(zip(poly[:-1], poly[1:]))
segments.append((rock[-1], rock[0]))

def seg_dist(px, py, a, b):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = np.clip(t, 0, 1)
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy))

def udist(px, py, segs):
    return np.min([seg_dist(px, py, a, b) for a, b in segs], axis=0)

def ground_height(x):
    xs, ys = zip(*ground)
    return np.interp(x, xs, ys)

def inside(px, py):
    """지면 아래 또는 바위 안이면 True (부호 정하기용)"""
    below = py < ground_height(px)
    in_rock = (px > 15.2) & (px < 17.8) & (py < 6.1) & (py > 2.6)
    return below | in_rock

# 블록 중심 좌표
cx = (np.arange(NX) + 0.5) * VOX
cy = (np.arange(NY) + 0.5) * VOX
CX, CY = np.meshgrid(cx, cy)

def draw_scene(ax, lw=2.2, color="k"):
    for a, b in segments:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, solid_capstyle="round")

def grid_lines(ax, alpha=0.18):
    for x in np.arange(0, W + 1e-6, VOX):
        ax.axvline(x, color="k", lw=0.4, alpha=alpha)
    for y in np.arange(0, H + 1e-6, VOX):
        ax.axhline(y, color="k", lw=0.4, alpha=alpha)

def finish(ax, title):
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=13)

# ---- 그림 1: 지형을 0.5m 블록으로 -----------------------------------
ud = udist(CX, CY, segments)
touched = ud <= VOX * np.sqrt(2) / 2          # 선이 지나가는 칸
solid = inside(CX, CY)
fig, axs = plt.subplots(1, 2, figsize=(13, 3.9))
draw_scene(axs[0]); finish(axs[0], "① 원래 지형 (선 = 충돌용 삼각형의 단면)")
img = np.zeros((NY, NX)); img[solid] = 1; img[touched] = 2
cmap = ListedColormap(["#ffffff", "#c9d6e8", "#e07b39"])
axs[1].imshow(img, origin="lower", extent=[0, W, 0, H], cmap=cmap, vmin=0, vmax=2)
grid_lines(axs[1]); draw_scene(axs[1], lw=1.0, color="#333")
finish(axs[1], "② 0.5m 블록으로 나눠 본 모습 (주황 = 벽이 지나가는 칸)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig1-voxelize.png"), dpi=110); plt.close(fig)

# ---- 그림 2: 완전한 SDF vs 가까운 거리만 기록한 SDF -------------------
sdf = np.where(solid, -ud, ud)
fig, axs = plt.subplots(1, 2, figsize=(13, 3.9))
im = axs[0].imshow(sdf, origin="lower", extent=[0, W, 0, H], cmap="RdBu", vmin=-6, vmax=6)
draw_scene(axs[0], lw=1.2); finish(axs[0], "① 완전한 SDF: 모든 칸에 '가장 가까운 벽까지 거리'")
fig.colorbar(im, ax=axs[0], fraction=0.025, pad=0.01, label="거리(m)  파랑 = 바깥, 빨강 = 안쪽")
band = np.where(ud <= 2 * VOX, sdf, np.nan)
cm2 = plt.get_cmap("RdBu").copy(); cm2.set_bad("#d9d9d9")
axs[1].imshow(band, origin="lower", extent=[0, W, 0, H], cmap=cm2, vmin=-1, vmax=1)
draw_scene(axs[1], lw=1.2); finish(axs[1], "② 벽에서 2칸(1m) 안쪽만 기록. 회색 = 기록 없음")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig2-sdf-full-vs-short.png"), dpi=110); plt.close(fig)
recorded = np.isfinite(band).mean()

# ---- 그림 3: 얇은 지붕에 비가 샌다 ------------------------------------
# 두께 5cm 판자 지붕. 블록 꼭짓점(0.5m 간격)에만 거리를 저장하고,
# 빗방울(반지름 3cm)은 저장된 값을 보간해서 "거리 - 반지름 <= 0" 이면 부딪힌 것으로 본다.
RAD, THICK = 0.03, 0.05
roof_segs = list(zip(roof[:-1], roof[1:]))
gx = np.arange(int(18 / VOX), int(24 / VOX) + 1) * VOX
gy = np.arange(int(5.5 / VOX), int(9.5 / VOX) + 1) * VOX
GX, GY = np.meshgrid(gx, gy)
corner_d = udist(GX, GY, roof_segs) - THICK / 2     # 꼭짓점에 저장되는 값

def sample(x, y):
    """꼭짓점 값 4개를 선형 보간 (3D 에서는 8개)"""
    i = np.clip(((x - gx[0]) / VOX).astype(int), 0, len(gx) - 2)
    j = np.clip(((y - gy[0]) / VOX).astype(int), 0, len(gy) - 2)
    fx = (x - gx[i]) / VOX; fy = (y - gy[j]) / VOX
    d00 = corner_d[j, i]; d10 = corner_d[j, i + 1]
    d01 = corner_d[j + 1, i]; d11 = corner_d[j + 1, i + 1]
    return (d00 * (1 - fx) * (1 - fy) + d10 * fx * (1 - fy)
            + d01 * (1 - fx) * fy + d11 * fx * fy)

drops_x = np.linspace(18.75, 23.25, 37)
ys = np.linspace(9.4, 5.6, 800)

def roof_hit_direct(x, y):
    """구멍 메우기: 판자를 원래 모양(얇은 상자)으로 직접 검사"""
    return udist(x, y, roof_segs) - THICK / 2 - RAD

fig, axs = plt.subplots(1, 2, figsize=(13, 5.2))
results = []
for ax, test, title in ((axs[0], lambda x, y: sample(x, y) - RAD, "① 블록 꼭짓점에 저장한 거리만으로 검사"),
                        (axs[1], roof_hit_direct, "② 판자 모양(상자)으로 직접 검사")):
    leaks = 0
    for x in drops_x:
        d = test(np.full_like(ys, x), ys)
        if np.any(d <= 0):
            hit = np.argmax(d <= 0)
            ax.plot([x, x], [ys[0], ys[hit]], color="#999", lw=1.0)
            ax.plot(x, ys[hit], "o", color="#555", ms=3)
        else:
            leaks += 1
            ax.plot([x, x], [ys[0], ys[-1]], color="#2f7fd6", lw=1.3)
            ax.plot(x, ys[-1], "v", color="#2f7fd6", ms=5)
    results.append(leaks)
    for gxv in gx: ax.axvline(gxv, color="k", lw=0.4, alpha=0.2)
    for gyv in gy: ax.axhline(gyv, color="k", lw=0.4, alpha=0.2)
    ax.plot(GX, GY, ".", color="#bbb", ms=3)
    for a, b in roof_segs:
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#a0522d", lw=2.5)
    ax.set_xlim(18, 24); ax.set_ylim(5.5, 9.5); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{title}\n빗방울 {len(drops_x)}개 중 {leaks}개가 샘 (파랑)", fontsize=12)
leaks = results[0]
fig.tight_layout(); fig.subplots_adjust(top=0.86); fig.savefig(os.path.join(OUT, "fig3-thin-roof-leak.png"), dpi=110); plt.close(fig)
print("min corner value near roof:", corner_d.min())

# ---- 그림 4: 큰 바둑판으로 나눠 빈 곳은 저장하지 않기 -------------------
NODE = 8                                   # 한 덩어리 = 8x8 블록 (3D 에서는 8x8x8)
nnx, nny = NX // NODE, NY // NODE
keep = np.zeros((nny, nnx), bool)
near = ud <= 2 * VOX
for j in range(nny):
    for i in range(nnx):
        keep[j, i] = near[j*NODE:(j+1)*NODE, i*NODE:(i+1)*NODE].any()
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.imshow(np.where(near, 1.0, np.nan), origin="lower", extent=[0, W, 0, H], cmap="Oranges", vmin=0, vmax=1.6)
for j in range(nny):
    for i in range(nnx):
        x0, y0 = i * NODE * VOX, j * NODE * VOX
        ax.add_patch(plt.Rectangle((x0, y0), NODE * VOX, NODE * VOX, fill=keep[j, i],
                                   facecolor="#e07b3922", edgecolor="#e07b39" if keep[j, i] else "#bbb",
                                   lw=1.6 if keep[j, i] else 0.8, ls="-" if keep[j, i] else "--"))
draw_scene(ax, lw=1.0, color="#333")
finish(ax, f"큰 칸 {nnx*nny}개 중 벽 근처가 있는 {keep.sum()}개만 저장 (점선 칸은 저장 안 함)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig4-sparse-nodes.png"), dpi=110); plt.close(fig)

print(f"grid {NX}x{NY}, recorded band {recorded:.1%}, leaks {leaks}/{len(drops_x)}, nodes kept {keep.sum()}/{nnx*nny}")
