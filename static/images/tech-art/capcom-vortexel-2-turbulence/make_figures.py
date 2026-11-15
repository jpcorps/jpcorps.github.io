# VORTEXEL (2) 글의 그림을 만드는 스크립트 (2D 로 아주 단순화한 설명용 그림)
# 실행: python3 make_figures.py  → 같은 폴더에 png 4장
# 바람 계산은 교과서식 '안정 유체(Stable Fluids)' 를 2D 로 흉내 낸 것이고,
# 카프콤 VORTEXEL 의 실제 계산 방식과는 다릅니다 (슬라이드에 알고리즘이 나오지 않습니다).
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

for f in fm.findSystemFonts():
    if "NotoSansCJK-Regular" in f:
        fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- 장면
NX, NY = 96, 40          # 칸 수 (한 칸 0.5m 라고 치면 48m x 20m)
DX = 0.5
xs = (np.arange(NX) + 0.5) * DX
ys = (np.arange(NY) + 0.5) * DX
X, Y = np.meshgrid(xs, ys)          # [y, x]

def make_solid():
    s = np.zeros((NY, NX), bool)
    ground = 1.5 + 1.2 * np.exp(-((X - 34) / 5.0) ** 2) * 2.0
    s |= Y < ground                                   # 바닥 + 작은 언덕
    s |= (X > 14) & (X < 17) & (Y < 9)                # 바위 벽
    s |= (X > 26) & (X < 27.5) & (Y < 6)              # 낮은 담
    return s

SOLID = make_solid()
FLUID = ~SOLID

def bilerp(f, px, py):
    """칸 중심 기준 값 f 를 (px, py)[m] 에서 섞어 읽기"""
    gx = np.clip(px / DX - 0.5, 0, NX - 1.001)
    gy = np.clip(py / DX - 0.5, 0, NY - 1.001)
    x0 = gx.astype(int); y0 = gy.astype(int)
    tx = gx - x0; ty = gy - y0
    a = f[y0, x0]; b = f[y0, x0 + 1]; c = f[y0 + 1, x0]; d = f[y0 + 1, x0 + 1]
    return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty

def project(u, v, iters=120):
    """압력을 구해서 '공기가 한곳에 몰리거나 비지 않게' 속도를 고친다"""
    div = np.zeros_like(u)
    div[1:-1, 1:-1] = ((u[1:-1, 2:] - u[1:-1, :-2]) + (v[2:, 1:-1] - v[:-2, 1:-1])) / (2 * DX)
    div[SOLID] = 0
    p = np.zeros_like(u)
    for _ in range(iters):
        pn = np.zeros_like(p)
        # 벽 칸은 이웃 압력을 그대로 따라가게 (벽으로는 공기가 못 들어감)
        pp = p.copy()
        pl = np.roll(pp, 1, 1); pr = np.roll(pp, -1, 1)
        pd = np.roll(pp, 1, 0); pu = np.roll(pp, -1, 0)
        sl = np.roll(SOLID, 1, 1); sr = np.roll(SOLID, -1, 1)
        sd = np.roll(SOLID, 1, 0); su = np.roll(SOLID, -1, 0)
        pl = np.where(sl, pp, pl); pr = np.where(sr, pp, pr)
        pd = np.where(sd, pp, pd); pu = np.where(su, pp, pu)
        pn = (pl + pr + pd + pu - div * DX * DX) / 4
        pn[:, -1] = 0           # 오른쪽 끝은 열린 출구
        pn[-1, :] = pn[-2, :]
        pn[SOLID] = 0
        p = pn
    gx = np.zeros_like(u); gy = np.zeros_like(v)
    gx[:, 1:-1] = (p[:, 2:] - p[:, :-2]) / (2 * DX)
    gy[1:-1, :] = (p[2:, :] - p[:-2, :]) / (2 * DX)
    u = u - gx; v = v - gy
    u[SOLID] = 0; v[SOLID] = 0
    return u, v, p

def simulate(steps, inject, dt=0.1, seed=0):
    """inject(u, v, p) -> (u, v) : 매 걸음 바람을 어떻게 넣을지"""
    u = np.zeros((NY, NX)); v = np.zeros((NY, NX)); p = np.zeros((NY, NX))
    for _ in range(steps):
        u, v = inject(u, v, p)
        # 옮기기(이류): 바람이 바람 자신을 실어 나른다
        px = X - u * dt; py = Y - v * dt
        u, v = bilerp(u, px, py), bilerp(v, px, py)
        u[SOLID] = 0; v[SOLID] = 0
        u, v, p = project(u, v)
    return u, v, p

def draw_solid(ax):
    ax.imshow(np.where(SOLID, 1.0, np.nan), origin="lower", extent=[0, NX * DX, 0, NY * DX],
              cmap="Greys", vmin=0, vmax=1.6, interpolation="nearest")

def draw_flow(ax, u, v, title, vmax=4.0):
    spd = np.hypot(u, v)
    spd_m = np.where(SOLID, np.nan, spd)
    ax.imshow(spd_m, origin="lower", extent=[0, NX * DX, 0, NY * DX], cmap="Blues",
              vmin=0, vmax=vmax, interpolation="bilinear")
    draw_solid(ax)
    uu = np.where(SOLID, np.nan, u); vv = np.where(SOLID, np.nan, v)
    ax.streamplot(xs, ys, uu, vv, color="#e8590c", density=1.1, linewidth=0.8, arrowsize=0.8)
    ax.set_title(title, fontsize=12)
    ax.set_xlim(0, NX * DX); ax.set_ylim(0, NY * DX); ax.set_xticks([]); ax.set_yticks([])

WIND = 3.0  # m/s

# ---------------------------------------------------------------- 그림 1
def fig1():
    # 왼쪽 경계에서 계속 바람을 밀어 넣는 가장 단순한 경우
    def inflow(u, v, p):
        u = u.copy(); u[:, :2] = WIND; u[SOLID] = 0
        return u, v
    u, v, p = simulate(260, inflow)
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.6))
    # 왼쪽: 한 방향 바람 (지형을 모름)
    ax = axs[0]
    ax.imshow(np.full((NY, NX), 0.55), origin="lower", extent=[0, NX * DX, 0, NY * DX],
              cmap="Blues", vmin=0, vmax=1, alpha=0.6)
    draw_solid(ax)
    for yy in np.arange(2, 20, 2.5):
        for xx in np.arange(2, 46, 5):
            ax.annotate("", (xx + 3, yy), (xx, yy),
                        arrowprops=dict(arrowstyle="->", color="#e8590c", lw=1.3))
    ax.set_title("① 한 방향 바람: 어디서나 같은 방향·같은 세기 (벽도 뚫고 지나감)", fontsize=12)
    ax.set_xlim(0, NX * DX); ax.set_ylim(0, NY * DX); ax.set_xticks([]); ax.set_yticks([])
    draw_flow(axs[1], u, v, "② 격자로 계산한 바람: 벽에 막히고, 넘고, 뒤에서 잦아듦")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig1-uniform-vs-grid.png"), dpi=110)
    plt.close(fig)

# ---------------------------------------------------------------- 그림 2
def fig2():
    n = 41
    g = np.linspace(-1.4, 1.4, n)
    LX, LY = np.meshgrid(g, g)
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.9))
    cases = [
        ("상자(Box) + 한 방향", np.maximum(np.abs(LX), np.abs(LY)), "dir"),
        ("원기둥(Cylinder, 위에서 본 모습) + 소용돌이", np.hypot(LX, LY), "swirl"),
        ("구(Sphere) + 사방으로 퍼짐", np.hypot(LX, LY), "radial"),
    ]
    for ax, (title, d, mode) in zip(axs, cases):
        strength = np.clip(1 - d, 0, 1)          # 거리 1 에서 0 이 되도록 줄어듦 (예시)
        ax.imshow(np.where(d <= 1, strength, np.nan), origin="lower", extent=[-1.4, 1.4, -1.4, 1.4],
                  cmap="Blues", vmin=-0.1, vmax=1.0)
        r = np.hypot(LX, LY) + 1e-6
        if mode == "dir":
            U, V = np.ones_like(LX), np.zeros_like(LY)
        elif mode == "swirl":
            U, V = -LY / r, LX / r
        else:
            U, V = LX / r, LY / r
        m = (d <= 1) & (np.arange(n)[None, :] % 4 == 0) & (np.arange(n)[:, None] % 4 == 0)
        ax.quiver(LX[m], LY[m], (U * strength)[m], (V * strength)[m], color="#e8590c",
                  scale=6, width=0.008)
        # 모양의 테두리 (거리 = 1)
        ax.contour(LX, LY, d, levels=[1.0], colors="k", linewidths=1.5)
        ax.set_title(title, fontsize=12)
        ax.set_aspect("equal"); ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
        ax.tick_params(labelsize=8)
    fig.suptitle("발생원 안쪽을 -1 ~ +1 공간으로 바꿔 놓고 '중심에서 얼마나 떨어졌나'(거리) 하나로 세기를 정한다", fontsize=12)
    fig.tight_layout(rect=[0, 0.05, 1, 0.93])
    fig.savefig(os.path.join(OUT, "fig2-emitters.png"), dpi=110)
    plt.close(fig)

# ---------------------------------------------------------------- 그림 3
def fig3():
    # 지형 복잡도: 주변 9x9 칸 안의 벽 칸 수 (슬라이드는 큰 칸마다 블록 개수를 센다)
    k = 4
    pad = np.pad(SOLID.astype(float), k, mode="edge")
    comp = np.zeros((NY, NX))
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            comp += pad[k + dy:k + dy + NY, k + dx:k + dx + NX]
    comp /= (2 * k + 1) ** 2

    FORCE = 0.6
    def everywhere(u, v, p):
        u = u + FORCE * FLUID * np.clip(WIND - u, 0, None) / WIND
        return u, v
    state = {"mask": np.ones((NY, NX))}
    def filtered(u, v, p):
        pa = np.abs(p)
        pn = pa / (np.percentile(pa[FLUID], 95) + 1e-6)
        mask = ((comp < 0.12) & (pn < 0.35)).astype(float)
        state["mask"] = mask
        u = u + FORCE * FLUID * mask * np.clip(WIND - u, 0, None) / WIND
        return u, v
    def boundary(u, v, p):
        u = u.copy(); u[:, :2] = WIND; u[SOLID] = 0
        return u, v

    ub, vb, _ = simulate(40, boundary)
    ue, ve, _ = simulate(260, everywhere)
    uf, vf, pf = simulate(260, filtered)
    fig, axs = plt.subplots(2, 2, figsize=(13, 7.2))
    draw_flow(axs[0, 0], ub, vb, "① 가장자리에서만 불어 넣기: 안쪽까지 가는 데 한참 걸림 (40걸음 후)")
    draw_flow(axs[0, 1], ue, ve, "② 전체에 똑같이 불어 넣기: 벽 뒤에도 바람이 붙음")
    ax = axs[1, 0]
    ax.imshow(np.where(SOLID, np.nan, state["mask"]), origin="lower",
              extent=[0, NX * DX, 0, NY * DX], cmap="Greens", vmin=-0.3, vmax=1.3,
              interpolation="nearest")
    draw_solid(ax)
    ax.set_title("③ 마스크: 초록 = 바람을 더하는 곳 / 연한 색 = 지형이 복잡하거나 압력이 큰 곳", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([])
    draw_flow(axs[1, 1], uf, vf, "④ 마스크를 씌워 불어 넣은 결과")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig3-global-wind.png"), dpi=110)
    plt.close(fig)
    # 비교용 숫자: 바위 벽 바로 뒤(바람그늘) 평균 풍속
    lee = FLUID & (X > 17.5) & (X < 21) & (Y < 7)
    print("바위 뒤 평균 풍속  전체에 똑같이: %.2f  마스크: %.2f  (m/s)"
          % (np.hypot(ue, ve)[lee].mean(), np.hypot(uf, vf)[lee].mean()))
    print("열린 하늘 평균 풍속 전체에 똑같이: %.2f  마스크: %.2f"
          % (np.hypot(ue, ve)[FLUID & (Y > 15)].mean(), np.hypot(uf, vf)[FLUID & (Y > 15)].mean()))

# ---------------------------------------------------------------- 그림 4
def fig4():
    fig, ax = plt.subplots(figsize=(8.5, 8))
    G, T, B = 224, 128, 12      # Geometry 범위, Turbulence 범위(가로·세로), 섞는 띠(예시)
    ax.add_patch(Rectangle((-G / 2, -G / 2), G, G, fill=False, lw=1.5, ls="--", ec="#868e96"))
    ax.text(-G / 2 + 3, G / 2 - 9, "Geometry 범위 (약 224m)", color="#495057", fontsize=11)
    ax.add_patch(Rectangle((-T / 2, -T / 2), T, T, fc="#d0ebff", ec="#1c7ed6", lw=2))
    ax.add_patch(Rectangle((-T / 2 + B, -T / 2 + B), T - 2 * B, T - 2 * B, fc="#a5d8ff", ec="none"))
    ax.text(-T / 2 + 3, T / 2 - 9, "Turbulence 계산 범위 (128m)", color="#1864ab", fontsize=11)
    ax.text(0, -T / 2 + 4, "가장자리 띠: 안쪽 계산 결과와 바깥 값을 섞음", ha="center", fontsize=9.5,
            color="#1864ab")
    ax.text(0, 8, "3D 유체 계산\n(벽에 막히고 돌아가는 바람)", ha="center", fontsize=12)
    ax.text(0, -88, "범위 밖: 유체 계산 없음\n바람 발생원을 직접 읽어서 바람을 정함", ha="center",
            fontsize=11, color="#495057")
    for (cx, cy, r, lab) in [(78, 70, 13, "폭발 (구)"), (-85, -40, 11, "회오리 (원기둥)"), (30, 40, 9, "")]:
        ax.add_patch(Circle((cx, cy), r, fc="#ffe8cc", ec="#e8590c", lw=1.5))
        if lab:
            ax.text(cx, cy - r - 9, lab, ha="center", fontsize=10, color="#d9480f")
    ax.add_patch(Rectangle((-100, 60), 30, 14, fc="#ffe8cc", ec="#e8590c", lw=1.5))
    ax.text(-85, 51, "골짜기 바람 (상자)", ha="center", fontsize=10, color="#d9480f")
    ax.text(30, 40, "발생원", ha="center", va="center", fontsize=9, color="#d9480f")
    ax.set_xlim(-120, 120); ax.set_ylim(-120, 120); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("위에서 내려다본 범위 개념도 (범위 크기 비율만 맞춤, 발생원은 예시)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig4-ranges.png"), dpi=110)
    plt.close(fig)

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("done")
