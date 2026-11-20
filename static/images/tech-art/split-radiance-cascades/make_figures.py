"""
'스플릿 래디언스 캐스케이드' 글(2026-11-21) 그림 3장. python3 make_figures.py 로 실행 (수 초).
모두 원리를 보여 주는 2D 장난감 계산이며, 원문(jacktollenaar.top)이나 논문의 실제 코드가 아니다.

장면(2D 옆모습): 폭 20, 높이 8 인 방 두 칸. x=9.3 에 천장까지 닿는 벽
(프로브 칸 경계와 일부러 안 맞춤).
  - 오른쪽 방 천장 x=13~17 에 밝은 조명(1.0), 왼쪽 방 천장 x=2~4 에 어두운 조명(0.25).
  - 빛은 한 번만 계산(조명에 직접 닿은 광선만 밝음). 튕긴 빛은 없음.
바닥(y=0) 위 점들에서 위쪽 반원 방향으로 광선을 쏴서
  - 정답: 점마다 광선 평균(코사인 가중)
  - 캐스케이드: 광선을 '맞은 거리'로 0~3번 칸에 나눠 담고(경계 0.5, 2, 8: 4배씩),
    칸마다 프로브 간격을 2배씩 넓혀 이웃 점들의 광선을 함께 모은 뒤 위에서부터 합친다.
    (a) 투과율 없이 그냥 더함   (b) 원문처럼 '안 막히고 지나간 비율'(투과율)을 곱해 합침
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "Noto Sans CJK JP", "font.size": 11,
                     "axes.unicode_minus": False})
OUT = __file__.rsplit("/", 1)[0] + "/"
rng = np.random.default_rng(7)

W, H, WALL = 20.0, 8.0, 9.3
LIGHTS = [(13.0, 17.0, 1.0), (2.0, 4.0, 0.25)]      # 천장 조명 (x0, x1, 밝기)
L0, NC = 0.5, 4                                      # 0번 칸 길이, 칸 개수
EDGES = [0.0] + [L0 * 4 ** k for k in range(NC - 1)] + [np.inf]   # 0,1,4,16,inf


def trace(ox, oy, dx, dy):
    """2D 광선 하나: 맞은 거리 t 와 그 점의 밝기를 돌려준다."""
    best_t, rad = np.inf, 0.0
    # 천장 y=H
    if dy > 1e-9:
        t = (H - oy) / dy
        x = ox + t * dx
        if 0 <= x <= W and t < best_t:
            best_t, rad = t, 0.0
            for x0, x1, e in LIGHTS:
                if x0 <= x <= x1:
                    rad = e
    # 세로 벽들 x=0, x=WALL, x=W
    if abs(dx) > 1e-9:
        for wx in (0.0, WALL, W):
            t = (wx - ox) / dx
            if t > 1e-6 and t < best_t:
                y = oy + t * dy
                if 0 <= y <= H:
                    best_t, rad = t, 0.0
    return best_t, rad


def cascade_of(t):
    """원문 식과 같은 꼴: ceil(max(0.5*log2(t/L0), 0)) → 칸 길이가 4배씩."""
    c = int(np.ceil(max(0.5 * np.log2(max(t, 1e-9) / L0), 0.0)))
    return min(c, NC - 1)


# ── 그림 1: 한 점에서 쏜 광선을 맞은 거리로 칸에 나누기 ─────────────────
def fig1():
    fig, ax = plt.subplots(figsize=(9, 4.2))
    cols = ["#e8a33d", "#3d8be8", "#3dbf6e", "#b05ce0"]
    ox, oy = 7.5, 0.05
    for a in np.linspace(0.08, np.pi - 0.08, 15):
        dx, dy = np.cos(a), np.sin(a)
        t, r = trace(ox, oy, dx, dy)
        c = cascade_of(t)
        ax.plot([ox, ox + t * dx], [oy, oy + t * dy], color=cols[c], lw=2)
        ax.plot(ox + t * dx, oy + t * dy, "o", color=cols[c], ms=5)
    for k, e in enumerate(EDGES[1:-1]):
        th = np.linspace(0, np.pi, 100)
        ax.plot(ox + e * np.cos(th), oy + e * np.sin(th), "--", color="gray", lw=0.8)
    ax.fill_between([0, W], -0.4, 0, color="#555")
    ax.fill_between([WALL - 0.12, WALL + 0.12], 0, H, color="#555")
    ax.plot([0, W], [H, H], color="#555", lw=4)
    for x0, x1, e in LIGHTS:
        ax.plot([x0, x1], [H, H], color="#ffd84a" if e > 0.5 else "#c9b46a", lw=7)
    for k in range(NC):
        hi = f"{EDGES[k+1]:g}" if k < NC - 1 else ""
        ax.plot([], [], color=cols[k], lw=3, label=f"{k}번 칸 ({EDGES[k]:g}~{hi})")
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_xlim(-0.5, W + 0.5); ax.set_ylim(-0.5, H + 0.6); ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("광선 하나를 끝까지 쏘고, 맞은 거리에 따라 칸(캐스케이드)에 넣기")
    fig.tight_layout(); fig.savefig(OUT + "fig1_split_rays.png", dpi=130); plt.close(fig)


# ── 그림 2·3: 투과율 있는/없는 합치기 비교 ─────────────────────────────
NBIN = 8                                             # 방향 칸 (2D 반원을 8등분, 단순화)
xs = np.linspace(0.25, W - 0.25, 160)                # 바닥 위 화소들
RAYS = 1024


def bin_of(a):
    return min(int(a / np.pi * NBIN), NBIN - 1)


def run():
    # 정답과 광선 기록
    ref = np.zeros(len(xs))
    recs = []
    for i, x in enumerate(xs):
        a = rng.random(RAYS) * np.pi
        s = 0.0; ws = 0.0
        for ang in a:
            dx, dy = np.cos(ang), np.sin(ang)
            t, r = trace(x, 0.05, dx, dy)
            w = dy                                             # 코사인 가중
            s += r * w; ws += w
            recs.append((i, x, ang, t, r))
        ref[i] = s / ws
    # 칸 c 의 프로브 간격 = 0.5 * 2^c. 프로브마다 방향 칸별로 (밝기합, 지나간 수, 들어온 수)
    probes = [dict() for _ in range(NC)]
    for i, x, ang, t, r in recs:
        hc = cascade_of(t)
        b = bin_of(ang)
        for c in range(hc + 1):                       # 맞은 칸까지 들르고
            key = (int(x // (0.5 * 2 ** c)), b)
            acc = probes[c].setdefault(key, np.zeros(3))
            acc[2] += 1                                # 들어온 광선 수(Weight)
            if c == hc:
                acc[0] += r                            # 맞은 칸에만 밝기
            else:
                acc[1] += 1                            # 아래 칸엔 '지나감' 표시(투과)
    res = {}
    for mode in ("naive", "trans"):
        out = np.zeros(len(xs))
        for i, x in enumerate(xs):
            s = 0.0; ws = 0.0
            for b in range(NBIN):
                merged = 0.0
                for c in range(NC - 1, -1, -1):         # 위 칸부터 내려오며 합치기
                    acc = probes[c].get((int(x // (0.5 * 2 ** c)), b))
                    if acc is None or acc[2] == 0:
                        continue
                    R = acc[0] / acc[2]; T = acc[1] / acc[2]
                    merged = R + (T * merged if mode == "trans" else merged)
                ang = (b + 0.5) / NBIN * np.pi
                w = np.sin(ang)
                s += merged * w; ws += w
            out[i] = s / ws
        res[mode] = out
    return ref, res


def fig23(ref, res):
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.axvspan(WALL - 0.08, WALL + 0.08, color="#555")
    ax.plot(xs, ref, color="black", lw=2.2, label="정답 (화소마다 광선 평균)")
    ax.plot(xs, res["naive"], color="#e0573d", lw=1.6, label="(a) 그냥 더하기")
    ax.plot(xs, res["trans"], color="#3d8be8", lw=1.6, ls="--", label="(b) 투과율 곱해 합치기")
    ax.set_xlabel("바닥 위치 (가운데 회색이 벽)"); ax.set_ylabel("바닥에 닿는 빛")
    ax.set_xlim(0, W); ax.legend(fontsize=9, loc="upper left")
    ax.set_title("벽 너머 빛이 새는가: 투과율을 안 쓰면 왼쪽 방까지 밝아진다")
    fig.tight_layout(); fig.savefig(OUT + "fig2_leak_compare.png", dpi=130); plt.close(fig)

    left = xs < WALL - 0.5
    for k in ("naive", "trans"):
        err = np.abs(res[k] - ref)
        print(f"{k}: 왼쪽 방 평균 {res[k][left].mean():.3f} (정답 {ref[left].mean():.3f}), "
              f"전체 평균 오차 {err.mean():.3f}")
    near = (xs > 8.0) & (xs < WALL)
    print("벽 바로 왼쪽(8~9.3) 평균:", {k: round(float(res[k][near].mean()), 3) for k in res},
          "정답", round(float(ref[near].mean()), 3))


def fig3():
    """칸이 올라갈수록: 길이 4배, 프로브 간격 2배, 방향 수 늘어남을 표로 그림."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.axis("off")
    cols = ["#e8a33d", "#3d8be8", "#3dbf6e", "#b05ce0"]
    for c in range(NC):
        y = 3 - c
        n = 4 * 2 ** c
        sp = 0.5 * 2 ** c
        xs_ = np.arange(0, 16 + 1e-9, sp)
        ax.plot(xs_, [y] * len(xs_), "o", color=cols[c], ms=max(3, 9 - 2 * c))
        for x in xs_[:: max(1, int(4 / sp))][:1]:
            for a in np.linspace(0, 2 * np.pi, n, endpoint=False):
                ax.plot([x, x + 0.35 * np.cos(a)], [y, y + 0.35 * np.sin(a)], color=cols[c], lw=0.8)
        ax.text(17, y, f"{c}번 칸: 광선 구간 {EDGES[c]:g}~{'' if c == NC - 1 else format(EDGES[c+1], 'g')}, 프로브 간격 {sp:g}, 방향 {n}개",
                va="center", fontsize=9.5)
    ax.set_xlim(-0.7, 34); ax.set_ylim(-0.7, 3.7)
    ax.set_title("위 칸으로 갈수록: 멀리 보고, 듬성듬성 놓고, 방향은 촘촘하게 (2D 장난감 값)")
    fig.tight_layout(); fig.savefig(OUT + "fig3_cascades.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    fig1()
    ref, res = run()
    fig23(ref, res)
    fig3()
