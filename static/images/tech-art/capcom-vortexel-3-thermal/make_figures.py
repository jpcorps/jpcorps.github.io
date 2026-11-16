# VORTEXEL (3) 글의 그림을 만드는 스크립트 (설명용으로 아주 단순화한 2D 흉내)
# 실행: python3 make_figures.py  → 같은 폴더에 png 4장
# 규칙: 불붙은 이웃과 링크로 이어진 점은 '데워진 시간'이 쌓이고,
#       IGNITE 초가 쌓이면 불이 붙어 BURN 초 동안 타고 꺼진다.
# 링크 거리, 바람 효과의 크기 등은 제가 임의로 정한 값이며
# 카프콤 VORTEXEL 의 실제 구현과는 다릅니다 (슬라이드에 세부 공식이 나오지 않습니다).
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

for f in fm.findSystemFonts():
    if "NotoSansCJK-Regular" in f:
        fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))

IGNITE = 1.0   # 불에 1초 닿으면 불붙고 (슬라이드 예시 숫자)
BURN = 2.0     # 2초 동안 탄다
DT = 0.05
LINK_R = 2.6   # 이웃으로 이을 거리 (임의)

# ---------------------------------------------------------------- 풀밭 점 만들기
rng = np.random.default_rng(7)
W, H = 30.0, 16.0

def in_grass(x, y):
    # 풀밭 두 덩어리 + 가는 풀길 (나머지는 맨땅)
    a = ((x - 9) / 8) ** 2 + ((y - 8) / 6) ** 2 < 1
    b = ((x - 22) / 6.5) ** 2 + ((y - 7.5) / 5.5) ** 2 < 1
    c = (x > 15) & (x < 17.5) & (np.abs(y - 8.5) < 1.2)
    return a | b | c

def poisson_points(n_try=6000, rmin=1.55):
    pts = []
    for _ in range(n_try):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if not in_grass(x, y):
            continue
        if all((x - px) ** 2 + (y - py) ** 2 > rmin ** 2 for px, py in pts):
            pts.append((x, y))
    return np.array(pts)

P = poisson_points()
N = len(P)
D = np.linalg.norm(P[:, None] - P[None], axis=2)
LINK = (D < LINK_R) & (D > 0)
N_LINKS = int(LINK.sum() // 2)

def simulate(t_end, start, wind=None, wind_gain=0.0):
    """시간 규칙 불 번짐. wind=(wx,wy) 단위벡터면, 바람 방향으로 가는 링크는
    더 빨리 데워진다고 (제 마음대로) 가정."""
    heat = np.zeros(N)            # 데워진 시간 누적
    t_on = np.full(N, np.inf)     # 불붙은 시각
    from_dir = np.zeros((N, 2))   # 불이 온 방향
    t_on[start] = 0.0
    # 링크마다 데워지는 빠르기
    rate = LINK.astype(float)
    if wind is not None:
        d = P[None] - P[:, None]                       # i -> j 방향
        d /= np.maximum(np.linalg.norm(d, axis=2, keepdims=True), 1e-9)
        cos = d[..., 0] * wind[0] + d[..., 1] * wind[1]
        rate = LINK * np.clip(1.0 + wind_gain * cos, 0.15, None)
    t = 0.0
    while t < t_end - 1e-9:
        burning = (t_on <= t) & (t < t_on + BURN)
        unlit = ~np.isfinite(t_on)
        inc = (rate[burning] ).max(axis=0) if burning.any() else np.zeros(N)
        heat[unlit] += inc[unlit] * DT
        newly = unlit & (heat >= IGNITE - 1e-9)
        for j in np.where(newly)[0]:
            src = np.where(burning & LINK[:, j])[0]
            v = P[j] - P[src].mean(axis=0)
            from_dir[j] = v / max(np.linalg.norm(v), 1e-9)
        t += DT
        t_on[newly] = t
    return t_on, heat, from_dir

def state_at(t_on, heat, t):
    burned = np.clip((t - t_on) / BURN, 0, 1)        # 연소도(탄 정도) 0~1
    burned[~np.isfinite(t_on)] = 0
    burning = (t_on <= t) & (t < t_on + BURN)
    out = (t >= t_on + BURN)
    return burned, burning, out

C_GRASS = "#6aa84f"; C_FIRE = "#ff7b1c"; C_OUT = "#3b3b3b"; C_HEAT = "#f1c232"

def draw_field(ax, title):
    gx, gy = np.meshgrid(np.linspace(0, W, 300), np.linspace(0, H, 160))
    ax.imshow(in_grass(gx, gy), extent=(0, W, 0, H), origin="lower",
              cmap=matplotlib.colors.ListedColormap(["#efe6d2", "#dcebd0"]), zorder=0)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title, fontsize=11)

def draw_links(ax, alpha=0.35):
    for i in range(N):
        for j in range(i + 1, N):
            if LINK[i, j]:
                ax.plot(*zip(P[i], P[j]), color="#7a7a7a", lw=0.7, alpha=alpha, zorder=1)

def draw_points(ax, t_on, heat, t, arrows=False, from_dir=None):
    burned, burning, out = state_at(t_on, heat, t)
    unlit = ~np.isfinite(t_on) | (t_on > t)
    col = []
    for i in range(N):
        if out[i]:
            col.append(C_OUT)
        elif burning[i]:
            col.append(C_FIRE)
        else:
            col.append(C_GRASS)
    ax.scatter(P[:, 0], P[:, 1], s=70, c=col, edgecolors="white", linewidths=0.8, zorder=3)
    if arrows and from_dir is not None:
        m = burning
        ax.quiver(P[m, 0], P[m, 1], from_dir[m, 0], from_dir[m, 1], color="#b03a00",
                  scale=18, width=0.006, zorder=4)

legend_pts = [Line2D([0], [0], marker="o", ls="", markerfacecolor=c, markeredgecolor="white",
                     markersize=9, label=l)
              for c, l in [(C_GRASS, "아직 안 탐"), (C_FIRE, "타는 중"), (C_OUT, "다 타서 꺼짐")]]

# ---------------------------------------------------------------- fig1 격자 vs 점+링크
def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(12, 3.9))
    ax = axs[0]
    cell = 1.0
    n_cells = int((W / cell) * (H / cell))
    draw_field(ax, f"① 2D 히트맵: 넓이만큼 칸이 필요 ({n_cells}칸)")
    for x in np.arange(0, W + 0.01, cell):
        ax.axvline(x, color="#999", lw=0.4, zorder=1)
    for y in np.arange(0, H + 0.01, cell):
        ax.axhline(y, color="#999", lw=0.4, zorder=1)
    ax = axs[1]
    draw_field(ax, f"② 발화점 + 이웃 링크: 점 개수만큼 ({N}점, 링크 {N_LINKS}개)")
    draw_links(ax, 0.6)
    ax.scatter(P[:, 0], P[:, 1], s=55, c=C_GRASS, edgecolors="white", linewidths=0.8, zorder=3)
    fig.text(0.5, 0.01, "같은 30m × 16m 땅. 연한 초록이 풀밭, 베이지가 맨땅. 점 간격과 링크 거리는 제가 임의로 정했습니다.",
             ha="center", fontsize=9, color="#555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(OUT, "fig1-grid-vs-points.png"), dpi=130)
    plt.close(fig)

# ---------------------------------------------------------------- fig2 단계별 번짐
START = int(np.argmin(np.linalg.norm(P - np.array([3.0, 8.0]), axis=1)))

def fig2():
    t_on, heat, fd = simulate(20.0, START)
    times = [0.0, 2.0, 4.0, 6.0, 9.0, 13.0]
    fig, axs = plt.subplots(2, 3, figsize=(12, 5.6))
    for ax, t in zip(axs.flat, times):
        draw_field(ax, f"{t:.0f}초")
        draw_links(ax, 0.25)
        draw_points(ax, t_on, heat, t, arrows=True, from_dir=fd)
    axs[0, 0].annotate("불씨", P[START], xytext=(P[START][0] + 2, P[START][1] + 5),
                       arrowprops=dict(arrowstyle="->", color="#b03a00"), color="#b03a00", fontsize=10)
    fig.legend(handles=legend_pts, loc="lower center", ncol=3, frameon=False, fontsize=10)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(OUT, "fig2-spread-steps.png"), dpi=130)
    plt.close(fig)
    return t_on

# ---------------------------------------------------------------- fig3 풀 한 다발의 시간표
def fig3():
    # 일렬로 이어진 풀 다발 A-B-C-D 를 따로 계산 (링크 하나에 한 칸씩)
    n = 4
    t_on = np.full(n, np.inf); heat = np.zeros(n); t_on[0] = 0.0
    ts = np.arange(0, 8.0001, DT)
    hist_heat = np.zeros((len(ts), n)); hist_burn = np.zeros((len(ts), n))
    t = 0.0
    for k, t in enumerate(ts):
        burning = (t_on <= t) & (t < t_on + BURN)
        for j in range(n):
            if not np.isfinite(t_on[j]):
                nb = [i for i in (j - 1, j + 1) if 0 <= i < n]
                if any(burning[i] for i in nb):
                    heat[j] += DT
                if heat[j] >= IGNITE - 1e-9:
                    t_on[j] = t + DT
        hist_heat[k] = np.where(t_on <= t, 0.0, np.minimum(heat, IGNITE))  # 불붙은 뒤엔 안 그림
        b = np.clip((t - t_on) / BURN, 0, 1); b[~np.isfinite(t_on)] = 0
        hist_burn[k] = b
    fig, axs = plt.subplots(n, 1, figsize=(10, 5.4), sharex=True)
    for j in range(n):
        ax = axs[j]
        ax.fill_between(ts, 0, hist_heat[:, j] / IGNITE, color=C_HEAT, alpha=0.6, step="post",
                        label="데워진 시간 (1초가 차면 불붙음)")
        ax.plot(ts, hist_burn[:, j], color=C_OUT, lw=2, label="연소도 (탄 정도) 0 → 1")
        if np.isfinite(t_on[j]):
            ax.axvspan(t_on[j], min(t_on[j] + BURN, ts[-1]), color=C_FIRE, alpha=0.25, label="타는 중 (2초)")
        ax.set_ylim(-0.05, 1.15); ax.set_yticks([0, 1])
        ax.set_ylabel(f"풀 {'ABCD'[j]}", rotation=0, labelpad=22, fontsize=11)
        ax.grid(axis="x", color="#ddd")
    axs[-1].set_xlabel("시간(초)")
    h, l = axs[1].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, frameon=False, fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(os.path.join(OUT, "fig3-timeline.png"), dpi=130)
    plt.close(fig)
    return t_on

# ---------------------------------------------------------------- fig4 바람
def fig4():
    T = 6.0
    wind = (1.0, 0.0)
    a, ha, fa = simulate(T, START)
    b, hb, fb = simulate(T, START, wind=wind, wind_gain=0.8)
    c, hc, fc = simulate(T, START, wind=(-1.0, 0.0), wind_gain=0.8)
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, (to, hh, ff), title in zip(axs, [(a, ha, fa), (b, hb, fb), (c, hc, fc)],
                                       ["바람 없음", "바람 → (불 번지는 쪽으로)", "바람 ← (불 오는 쪽으로)"]):
        n_lit = int(np.isfinite(to).sum())
        draw_field(ax, f"{title} · {T:.0f}초 · 불붙은 점 {n_lit}개")
        draw_links(ax, 0.2)
        draw_points(ax, to, hh, T, arrows=True, from_dir=ff)
    for ax, w in zip(axs[1:], [wind, (-1, 0)]):
        ax.annotate("", xy=(15 + 3 * w[0], 14.6), xytext=(15 - 3 * w[0], 14.6),
                    arrowprops=dict(arrowstyle="-|>", color="#3d85c6", lw=2.5))
    fig.legend(handles=legend_pts, loc="lower center", ncol=3, frameon=False, fontsize=10)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(os.path.join(OUT, "fig4-wind.png"), dpi=130)
    plt.close(fig)
    return [int(np.isfinite(x).sum()) for x in (a, b, c)]

if __name__ == "__main__":
    print("points", N, "links", N_LINKS)
    fig1()
    t_on = fig2()
    print("lit by 4s/9s/13s:", [int((t_on <= t).sum()) for t in (4, 9, 13)], "max t_on", np.nanmax(np.where(np.isfinite(t_on), t_on, np.nan)), "unlit", int((~np.isfinite(t_on)).sum()))
    print("chain ignite times", fig3())
    print("lit at 6s (none/down/up):", fig4())
