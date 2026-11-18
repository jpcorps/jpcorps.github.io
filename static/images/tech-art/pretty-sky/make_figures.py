"""
'예쁜 하늘' 글(2026-11-19) 그림 3장. python3 make_figures.py 로 실행 (수 초).
모두 원리를 보여 주는 장난감 계산이며, 원문 게임/Godot 의 실제 코드가 아니다.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "Noto Sans CJK JP", "font.size": 11,
                     "axes.unicode_minus": False})
BG, W = "#1a1a2e", "white"

def to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)

# ── 그림 1: 노멀을 위로 꺾으면 구름 밑면이 하늘색을 받는다 ──────────────
SKY = np.array([0.30, 0.50, 0.95])     # 위쪽 반구(하늘)에서 오는 간접광
SEA = np.array([0.04, 0.07, 0.10])     # 아래쪽 반구(바다)에서 오는 간접광
SUN = np.array([1.00, 0.95, 0.85])
SUN_DIR = np.array([-0.5, 0.8, 0.35]); SUN_DIR /= np.linalg.norm(SUN_DIR)

def shade(nx, ny, nz, bend):
    # 간접광: 노멀을 위로 bend 만큼 꺾은 뒤 반구 조명(하늘/바다 섞기)
    bx, by, bz = nx, ny + bend, nz
    l = np.sqrt(bx ** 2 + by ** 2 + bz ** 2); by = by / l
    t = 0.5 + 0.5 * by
    amb = SKY * t[..., None] + SEA * (1 - t)[..., None]
    # 직사광: 원래 노멀 그대로 (구름이라 살짝 감싸는 wrap 조명)
    ndl = np.clip((nx * SUN_DIR[0] + ny * SUN_DIR[1] + nz * SUN_DIR[2] + 0.3) / 1.3, 0, 1)
    return 0.55 * amb + 0.9 * SUN * ndl[..., None]

H, Wd = 260, 420
ys, xs = np.mgrid[1:-1:H * 1j, -1.6:1.6:Wd * 1j]
sky_bg = np.zeros((H, Wd, 3))
g = (ys[..., None] + 1) / 2
sky_bg = SKY * 0.9 * g + np.array([0.75, 0.82, 0.95]) * (1 - g) * 0.9
# 납작한 구름 덩어리(타원) — 단면을 옆에서 본 그림
ex, ey = xs / 1.25, (ys + 0.05) / 0.62
r = np.sqrt(ex ** 2 + ey ** 2)
inside = r < 1
ez = np.sqrt(np.clip(1 - r ** 2, 0, 1))
# 타원체(가로 1.25, 세로 0.62, 깊이 1.0) 표면의 법선
nx, ny, nz = ex / 1.25, ey / 0.62, ez / 1.0
nl = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2) + 1e-6
nx, ny, nz = nx / nl, ny / nl, nz / nl

fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
fig.patch.set_facecolor(BG)
for ax, bend, title in [(axes[0], 0.0, "노멀 그대로: 밑면은 바다(어두운 아래쪽)를 본다"),
                        (axes[1], 0.8, "노멀을 위로 꺾음: 밑면도 하늘빛을 받는다")]:
    img = sky_bg.copy()
    c = shade(nx, ny, nz, bend)
    img[inside] = c[inside]
    ax.imshow(to_srgb(img), extent=(-1.6, 1.6, -1, 1))
    # 밑면 한 점의 노멀 화살표
    ax.annotate("", xy=(0.25, -0.67 - 0.32), xytext=(0.25, -0.67),
                arrowprops=dict(color="#ffcc66" if bend == 0 else "#666666",
                                width=2, headwidth=9, alpha=0.9 if bend == 0 else 0.5))
    if bend > 0:
        ax.annotate("", xy=(0.25 + 0.12, -0.67 + 0.30), xytext=(0.25, -0.67),
                    arrowprops=dict(color="#ffcc66", width=2, headwidth=9))
    ax.set_title(title, color=W, fontsize=11)
    ax.axis("off")
fig.text(0.5, 0.02, "노란 화살표: 간접광을 읽어 올 방향(노멀).  직사광 계산에는 원래 노멀을 그대로 쓴다.  (장난감 계산)",
         color="#bbbbcc", ha="center", fontsize=9.5)
plt.tight_layout(rect=(0, 0.05, 1, 0.96))
plt.savefig("fig1_normal_bending.png", dpi=110, facecolor=BG)
plt.close()

# ── 그림 2: 레이마칭 한 걸음 안에서 '깎기'와 '더하기' 순서 ─────────────
beta = np.array([0.20, 0.45, 1.05])      # 빨강·초록·파랑 산란 세기 (파랑이 제일 잘 흩어짐)
sun_here = np.exp(-beta * 0.35)          # 위에서 내려온 햇빛 (살짝 걸러진 흰빛)
D = 4.0                                  # 지평선 쪽으로 바라본 공기 두께

def march(N, order):
    ds = D / N
    T = np.exp(-beta * ds)               # 한 칸을 지나며 남는 빛
    S = beta * sun_here * ds             # 한 칸에서 새로 들어오는 빛(인스캐터링)
    L = np.zeros(3)
    for _ in range(N):                   # 먼 곳부터 카메라 쪽으로
        if order == "add_first":
            L = (L + S) * T              # 더하고 → 깎기 (원래 순서)
        else:
            L = L * T + S                # 깎고 → 더하기 (바꾼 순서)
    return L

exact = sun_here * (1 - np.exp(-beta * D))
Ns = [2, 4, 8, 16, 64, 256]
expo = 1.15
fig, ax = plt.subplots(figsize=(10, 3.9))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
rows = [("더하고 → 깎기", "add_first"), ("깎고 → 더하기", "att_first")]
for ri, (name, od) in enumerate(rows):
    for ci, N in enumerate(Ns):
        c = to_srgb(march(N, od) * expo)
        ax.add_patch(plt.Rectangle((ci, 1 - ri), 0.92, 0.85, color=c))
    ax.text(-0.1, 1 - ri + 0.42, name, color=W, ha="right", va="center")
ax.add_patch(plt.Rectangle((len(Ns) + 0.35, 0.5), 0.92, 0.85, color=to_srgb(exact * expo)))
ax.text(len(Ns) + 0.81, 0.3, "정답\n(걸음 무한대)", color=W, ha="center", va="top", fontsize=10)
for ci, N in enumerate(Ns):
    ax.text(ci + 0.46, -0.12, f"{N}걸음", color=W, ha="center", va="top")
ax.set_xlim(-2.4, len(Ns) + 1.4); ax.set_ylim(-0.6, 2.0); ax.axis("off")
ax.set_title("지평선 쪽 하늘색: 걸음 수와 순서에 따라 (장난감 계산)", color=W)
plt.tight_layout()
plt.savefig("fig2_march_order.png", dpi=110, facecolor=BG)
plt.close()
for N in Ns:
    print(N, "add_first", np.round(march(N, "add_first"), 3), "att_first", np.round(march(N, "att_first"), 3))
print("exact", np.round(exact, 3))

# ── 그림 3: 톤 매핑 — 1.0 넘는 하늘을 모니터에 담기 ──────────────────
def hable(x):
    A, B, C, Dd, E, F = 0.22, 0.30, 0.10, 0.20, 0.01, 0.30
    return ((x * (A * x + C * B) + Dd * E) / (x * (A * x + B) + Dd * F)) - E / F

def filmic(x, white, bias=2.0):
    return hable(x * bias) / hable(white * bias)

maps = [("선형 (1.0 넘으면 잘림)", lambda x: np.clip(x, 0, 1)),
        ("Reinhard  x/(1+x)", lambda x: x / (1 + x)),
        ("필믹, 흰색 기준 6.0", lambda x: np.clip(filmic(x, 6.0), 0, 1)),
        ("필믹, 흰색 기준 2.0", lambda x: np.clip(filmic(x, 2.0), 0, 1))]

# 해 쪽으로 갈수록 밝아지고 노래지는 HDR 하늘 (값이 1을 훌쩍 넘는다)
t = np.linspace(0, 1, 500)
base = np.array([0.35, 0.55, 0.95]); glow = np.array([1.0, 0.85, 0.55])
mixw = t[:, None] ** 1.5
sky = (base * (1 - mixw) + glow * mixw) * (0.5 + 1.9 * t[:, None] ** 2)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.3), gridspec_kw={"width_ratios": [1, 1.6]})
fig.patch.set_facecolor(BG)
x = np.linspace(0, 6, 400)
cols = ["#ff7766", "#aaaaaa", "#66bbff", "#ffcc44"]
for (name, f), c in zip(maps, cols):
    a1.plot(x, f(x), color=c, lw=2, label=name)
a1.set_facecolor("#16213e"); a1.set_xlabel("계산된 밝기 (HDR)", color=W); a1.set_ylabel("모니터에 나갈 밝기", color=W)
a1.tick_params(colors=W)
for s in a1.spines.values(): s.set_color("#555577")
a1.legend(facecolor="#0d0d22", labelcolor=W, fontsize=9, loc="lower right")
a1.set_title("톤 매핑 곡선", color=W)
strip = np.stack([to_srgb(f(sky)) for _, f in maps])
a2.imshow(np.repeat(strip, 30, axis=0), aspect="auto", extent=(0, 1, 4, 0))
for i, (name, _) in enumerate(maps):
    a2.text(0.01, i + 0.5, name, color="black", va="center", fontsize=9.5,
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=1.5))
a2.set_xticks([0, 1]); a2.set_xticklabels(["해에서 먼 하늘", "해 근처"], color=W)
a2.set_yticks([]); a2.set_title("같은 하늘, 다른 톤 매핑", color=W)
plt.tight_layout()
plt.savefig("fig3_tone_mapping.png", dpi=110, facecolor=BG)
plt.close()
print("sky max", sky.max().round(2), "linear clipped fraction", (sky.max(axis=1) > 1).mean().round(2))
