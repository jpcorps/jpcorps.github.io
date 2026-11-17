# VORTEXEL (4) 글의 그림을 만드는 스크립트 (설명용으로 아주 단순화한 2D 흉내)
# 실행: python3 make_figures.py  → 같은 폴더에 png 4장
#
# 슬라이드에서 가져온 생각:
#  - 땅은 0.5m 칸(복셀)마다 거리값(SDF)을 가진다.
#  - 칸마다 '대표 법선' 하나: 칸 모서리의 거리값으로 모서리 방향에 가중치를 줘서 더하고 정규화.
#  - 파편이 든 칸의 거리값으로 '평면' 하나를 만들고, 파편의 꼭짓점 전부를 그 평면과 비교.
#  - 파편끼리는 '내접원'(3D 에서는 내접구) 끼리만 부딪친다. 모양은 안 본다.
# 반발 계수, 마찰, 충돌 응답 공식, 시간 간격 등은 제가 임의로 정한 값이며
# 카프콤 VORTEXEL 의 실제 구현과는 다릅니다 (슬라이드에 세부 공식이 나오지 않습니다).
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon, Circle, Rectangle

for f in fm.findSystemFonts():
    if "NotoSansCJK-Regular" in f:
        fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))

H = 0.5                      # 칸 크기 0.5m (슬라이드의 근거리 SDF 1칸)
W_, HT = 12.0, 6.0           # 2D 세계 크기 (m)
NX, NY = int(W_ / H), int(HT / H)

# ---------------------------------------------------------------- 땅과 거리값
def ground_y(x):
    return 1.6 + 0.9 * np.exp(-((x - 2.5) / 1.6) ** 2) * 1.6 - 0.12 * x \
        + 0.25 * np.sin(2.2 * x)

GX = np.linspace(-1, W_ + 1, 3000)
GPTS = np.stack([GX, ground_y(GX)], 1)

def sdf_exact(p):
    """땅 곡선까지의 거리 (땅 위 +, 땅 속 -)."""
    d = np.sqrt(((GPTS[None] - p[:, None]) ** 2).sum(-1)).min(1)
    below = p[:, 1] < ground_y(p[:, 0])
    return np.where(below, -d, d)

# 칸 모서리(격자점)에 거리값을 미리 구워 둔다
CX, CY = np.meshgrid(np.arange(NX + 1) * H, np.arange(NY + 1) * H, indexing="ij")
CORNER = sdf_exact(np.stack([CX.ravel(), CY.ravel()], 1)).reshape(NX + 1, NY + 1)

def rep_normal_from(c00, c10, c01, c11):
    """칸 모서리 4개의 거리값으로 대표 법선 하나 (3D 에서는 8개)."""
    s = 1 / np.sqrt(2)
    dirs = np.array([[-s, -s], [s, -s], [-s, s], [s, s]])
    vals = np.array([c00, c10, c01, c11])
    n = (vals[:, None] * dirs).sum(0)
    L = np.linalg.norm(n)
    return n / L if L > 1e-6 else np.zeros(2), L

REPN = np.zeros((NX, NY, 2))
for i in range(NX):
    for j in range(NY):
        REPN[i, j], _ = rep_normal_from(CORNER[i, j], CORNER[i + 1, j],
                                        CORNER[i, j + 1], CORNER[i + 1, j + 1])

def sdf_at(p):
    """모서리 값 이중선형 보간 = 게임이 읽는 거리값."""
    fx, fy = p[0] / H, p[1] / H
    i, j = int(np.clip(fx, 0, NX - 1)), int(np.clip(fy, 0, NY - 1))
    u, v = fx - i, fy - j
    return ((1 - u) * (1 - v) * CORNER[i, j] + u * (1 - v) * CORNER[i + 1, j]
            + (1 - u) * v * CORNER[i, j + 1] + u * v * CORNER[i + 1, j + 1]), (i, j)

# ---------------------------------------------------------------- 파편 (2D 강체)
def shape(kind, s):
    if kind == "box":
        return np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]]) * s
    if kind == "tri":
        a = np.radians([90, 210, 330])
        return np.stack([np.cos(a), np.sin(a)], 1) * s * 1.3
    if kind == "card":       # 납작한 판
        return np.array([[-1, -0.25], [1, -0.25], [1, 0.25], [-1, 0.25]]) * s * 1.4

class Body:
    def __init__(self, kind, s, pos, vel, w):
        self.kind, self.v_local = kind, shape(kind, s)
        self.pos, self.vel = np.array(pos, float), np.array(vel, float)
        self.ang, self.w = 0.0, w
        self.r_out = np.linalg.norm(self.v_local, axis=1).max()       # 외접원
        # 내접원: 중심에서 각 변까지 거리 중 최소
        v, r_in = self.v_local, 1e9
        for k in range(len(v)):
            a, b = v[k], v[(k + 1) % len(v)]
            e = b - a
            r_in = min(r_in, abs(e[0] * a[1] - e[1] * a[0]) / np.linalg.norm(e))
        self.r_in = r_in
        self.m = 1.0
        self.I = self.m * (self.r_out ** 2) / 3
        self.trail = []

    def verts(self):
        c, s = np.cos(self.ang), np.sin(self.ang)
        R = np.array([[c, -s], [s, c]])
        return self.v_local @ R.T + self.pos

E, MU, G, DT = 0.35, 0.5, -9.8, 1 / 120   # 반발, 마찰, 중력, 시간 간격 (임의)

def cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]

def step_ground(b):
    d, (i, j) = sdf_at(b.pos)
    if d - b.r_out > 0:                 # 거리 - 외접원 반지름 > 0 이면 안 닿음
        return
    n = REPN[i, j]
    if not n.any():                     # 법선 0 이면 포기 (대충!)
        return
    p0 = b.pos - n * d                  # 이 칸의 '평면'
    V = b.verts()
    pen = (V - p0) @ n
    k = np.argmin(pen)
    if pen[k] >= 0:
        return
    r = V[k] - b.pos
    vp = b.vel + b.w * np.array([-r[1], r[0]])
    vn = vp @ n
    if vn < 0:
        rn = cross2(r, n)
        jn = -(1 + E) * vn / (1 / b.m + rn * rn / b.I)
        t = np.array([-n[1], n[0]])
        vt = vp @ t
        rt = cross2(r, t)
        jt = np.clip(-vt / (1 / b.m + rt * rt / b.I), -MU * jn, MU * jn)
        imp = jn * n + jt * t
        b.vel += imp / b.m
        b.w += cross2(r, imp) / b.I
    b.pos += n * (-pen[k]) * 0.8

def step_pairs(bodies):
    """파편끼리: 내접원만 본다."""
    for a in range(len(bodies)):
        for c in range(a + 1, len(bodies)):
            A, B = bodies[a], bodies[c]
            d = B.pos - A.pos
            L = np.linalg.norm(d)
            if L < 1e-9 or L > A.r_in + B.r_in:
                continue
            n = d / L
            over = A.r_in + B.r_in - L
            A.pos -= n * over / 2
            B.pos += n * over / 2
            rv = (B.vel - A.vel) @ n
            if rv < 0:
                j = -(1 + E) * rv / 2
                A.vel -= j * n
                B.vel += j * n

def simulate(bodies, t_end, pairs=True):
    for s in range(int(t_end / DT)):
        for b in bodies:
            b.vel[1] += G * DT
            b.vel *= 0.999
            b.pos += b.vel * DT
            b.ang += b.w * DT
            step_ground(b)
            if s % 6 == 0:
                b.trail.append(b.pos.copy())
        if pairs:
            step_pairs(bodies)

# ================================================================ 그림 1: 대표 법선
fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [2.1, 1]})
ax = axs[0]
gx = np.linspace(0, W_, 400)
ax.fill_between(gx, 0, ground_y(gx), color="#c9b38f")
ax.plot(gx, ground_y(gx), color="#6b4f2a", lw=2)
for i in range(NX + 1):
    ax.plot([i * H] * 2, [0, HT], color="#999", lw=0.4)
for j in range(NY + 1):
    ax.plot([0, W_], [j * H] * 2, color="#999", lw=0.4)
for i in range(NX):
    for j in range(NY):
        c = np.array([(i + 0.5) * H, (j + 0.5) * H])
        if abs(sdf_exact(c[None])[0]) < 0.9:
            n = REPN[i, j]
            ax.arrow(c[0], c[1], n[0] * 0.33, n[1] * 0.33, head_width=0.08,
                     color="#1f5fbf", lw=1.2, length_includes_head=True)
ax.set_xlim(0, W_); ax.set_ylim(0, HT); ax.set_aspect("equal")
ax.set_title("땅 근처 칸마다 대표 법선(파란 화살표) 딱 하나", fontsize=13)
ax.set_xlabel("m")

ax = axs[1]
# 좁은 틈: 왼쪽 벽 x<0.15, 오른쪽 벽 x>0.85, 그 사이 0.5m 칸 하나
ax.add_patch(Rectangle((-0.3, -0.2), 0.45, 1.0, color="#c9b38f"))
ax.add_patch(Rectangle((0.85, -0.2), 0.45, 1.0, color="#c9b38f"))
ax.add_patch(Rectangle((0.25, 0.05), 0.5, 0.5, fill=False, ec="k", lw=1.5))
def gap_sdf(x):
    return min(x - 0.15, 0.85 - x)
cs = [(0.25, 0.05), (0.75, 0.05), (0.25, 0.55), (0.75, 0.55)]
vals = [gap_sdf(x) for x, _ in cs]
n, L = rep_normal_from(*vals)
for (x, y), v in zip(cs, vals):
    ax.plot(x, y, "o", color="#d0453b")
    ax.text(x, y + 0.06, f"{v:.2f}", ha="center", fontsize=11, color="#d0453b")
ax.text(0.5, 0.3, f"대표 법선 길이\n{L:.2f} → 0 법선", ha="center", va="center", fontsize=11)
ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.2, 0.8); ax.set_aspect("equal")
ax.set_title("두 벽이 마주 보는 틈: 법선이 사라진다", fontsize=13)
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig1-representative-normal.png"), dpi=110)
plt.close(fig)
print("gap normal length:", L)

# ================================================================ 그림 2: 꼭짓점 vs 평면
fig, ax = plt.subplots(figsize=(7.5, 5))
gx = np.linspace(3.0, 6.0, 200)
ax.fill_between(gx, 0.5, ground_y(gx), color="#c9b38f")
ax.plot(gx, ground_y(gx), color="#6b4f2a", lw=2)
b = Body("box", 0.18, (4.3, 0), (0, 0), 0)
b.ang = 0.5
b.pos[1] = ground_y(4.3) + 0.12
d, (i, j) = sdf_at(b.pos)
n = REPN[i, j]
p0 = b.pos - n * d
t = np.array([-n[1], n[0]])
ax.plot(*np.stack([p0 - t * 1.2, p0 + t * 1.2]).T, "--", color="#1f5fbf", lw=1.5,
        label="이 칸의 거리값으로 만든 평면")
ax.add_patch(Rectangle((i * H, j * H), H, H, fill=False, ec="#777", lw=1, ls=":"))
V = b.verts()
ax.add_patch(Polygon(V, closed=True, fc="#888", ec="k", alpha=0.85))
pen = (V - p0) @ n
for v, p in zip(V, pen):
    ax.plot(*v, "o", color="#d0453b" if p < 0 else "#2a9d4b", ms=8)
ax.add_patch(Circle(b.pos, b.r_out, fill=False, ec="#999", ls="--"))
ax.plot(*b.pos, "k+", ms=10)
ax.annotate("", xy=p0 + n * 0.45, xytext=p0, arrowprops=dict(arrowstyle="->", color="#1f5fbf", lw=2))
ax.text(*(p0 + n * 0.5 + np.array([0.03, -0.08])), "대표 법선", color="#1f5fbf", fontsize=11)
ax.text(b.pos[0] - 0.05, b.pos[1] + 0.55, "점선 원 = 외접원\n(거리 - 반지름 ≤ 0 이면\n닿았는지 자세히 본다)", fontsize=10, color="#555")
ax.plot([], [], "o", color="#d0453b", label="평면 아래로 파고든 꼭짓점")
ax.plot([], [], "o", color="#2a9d4b", label="평면 위 꼭짓점")
ax.legend(loc="lower left", fontsize=10)
ax.set_xlim(3.4, 5.4); ax.set_ylim(1.0, 2.6); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("파편이 든 칸 하나만 보고, 꼭짓점을 평면과 비교", fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig2-corner-vs-plane.png"), dpi=110)
plt.close(fig)

# ================================================================ 그림 3: 몬스터가 내려찍은 자리의 돌 파편
rng = np.random.default_rng(3)
bodies = []
for k in range(40):
    kind = ["box", "tri", "card"][k % 3]
    ang = rng.uniform(np.radians(25), np.radians(155))
    sp = rng.uniform(3.5, 7.0)
    x0 = 6.0 + rng.uniform(-0.2, 0.2)
    bodies.append(Body(kind, rng.uniform(0.06, 0.14),
                       (x0, ground_y(x0) + 0.3), (sp * np.cos(ang), sp * np.sin(ang)),
                       rng.uniform(-12, 12)))
snaps = []
for t_end in [0.25, 0.6, 3.5]:
    simulate(bodies, t_end - (snaps[-1][0] if snaps else 0))
    snaps.append((t_end, [b.verts() for b in bodies]))

fig, axs = plt.subplots(3, 1, figsize=(11, 10.5))
for ax, (t_end, polys) in zip(axs, snaps):
    gx = np.linspace(0, W_, 400)
    ax.fill_between(gx, 0, ground_y(gx), color="#c9b38f")
    ax.plot(gx, ground_y(gx), color="#6b4f2a", lw=2)
    for b, V in zip(bodies, polys):
        tr = np.array([p for p in b.trail[: int(t_end / DT / 6)]])
        if len(tr) > 1:
            ax.plot(tr[:, 0], tr[:, 1], color="#999", lw=0.5, alpha=0.6)
        ax.add_patch(Polygon(V, closed=True, fc="#666", ec="k", lw=0.6))
    ax.set_xlim(0, W_); ax.set_ylim(0.0, 5.0); ax.set_aspect("equal")
    ax.set_yticks([])
    ax.set_title(f"{t_end:.2f}초", loc="left", fontsize=12)
axs[-1].set_xlabel("m")
fig.suptitle("가운데를 내려찍었을 때 튀는 돌 40개: 땅은 '칸마다 평면 하나', 서로는 '내접원'만", fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig3-debris.png"), dpi=110)
plt.close(fig)
moving = sum(np.linalg.norm(b.vel) > 0.3 for b in bodies)
inside = sum(sdf_at(b.pos)[0] < -0.05 for b in bodies)
print("debris: still moving", moving, "/ sunk", inside, "/ total", len(bodies))

# ================================================================ 그림 4: 내접원끼리만 부딪치면
fig, axs = plt.subplots(1, 2, figsize=(11, 4))
for ax, (kind, title) in zip(axs, [("box", "네모: 모서리가 살짝 겹치는 정도"),
                                   ("card", "납작한 판: 서로 파고든다")]):
    A = Body(kind, 0.5, (0, 0), (0, 0), 0)
    B = Body(kind, 0.5, (0, 0), (0, 0), 0)
    B.ang = 0.15 if kind == "box" else 1.2
    B.pos = np.array([A.r_in + B.r_in, 0.0])
    if kind == "card":
        B.pos = np.array([A.r_in + B.r_in, 0.05])
    for body, col in [(A, "#7a8ea8"), (B, "#a8907a")]:
        ax.add_patch(Polygon(body.verts(), closed=True, fc=col, ec="k", alpha=0.75))
        ax.add_patch(Circle(body.pos, body.r_in, fill=False, ec="#d0453b", lw=2))
    ax.set_xlim(-1.0, 1.9); ax.set_ylim(-0.9, 0.9); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=13)
fig.suptitle("빨간 원(내접원)이 막 닿은 순간. 판처럼 길쭉한 건 모양끼리 겹쳐 보인다", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig4-inscribed.png"), dpi=110)
plt.close(fig)
print("saved to", OUT)
