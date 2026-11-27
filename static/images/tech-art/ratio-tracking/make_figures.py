# 'Ratio tracking, intuitively' 소개글용 장난감 그림.
# 실행: python3 make_figures.py  (numpy, matplotlib. 몇 초)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

KO_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(KO_PATH)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=KO_PATH).get_name()
plt.rcParams["axes.unicode_minus"] = False

L = 10.0   # 광선 길이
M = 1.0    # 밀도의 상한(majorant)


def f(x):
    """광선을 따라가며 만나는 안개 밀도. 0 <= f <= M 인 아무 함수."""
    return 0.55 * np.exp(-((x - 3.0) / 1.0) ** 2) + 0.9 * np.exp(-((x - 7.0) / 0.6) ** 2) + 0.05


# 정답 투과율 exp(-적분 f) — 아주 촘촘한 사다리꼴 적분으로
xs = np.linspace(0, L, 200001)
I_true = np.trapezoid(f(xs), xs)
T_true = np.exp(-I_true)


def ratio_tracking(rng, L=L, M=M, dens=f, log=None):
    x, T = 0.0, 1.0
    while True:
        x += -np.log(1.0 - rng.random()) / M   # 다음 '버스' 도착까지 거리
        if x >= L:
            break
        T *= 1.0 - dens(x) / M                  # 들른 자리에서 '안 막힐 확률' 곱하기
        if log is not None:
            log.append((x, T))
    return T


def ray_march(n, jitter, rng):
    dx = L / n
    off = rng.random() if jitter else 0.5
    x = (np.arange(n) + off) * dx
    return np.exp(-np.sum(f(x)) * dx)


# ---------- 그림 1: 한 번 추적하는 모습 ----------
rng = np.random.default_rng(3)
log = []
T1 = ratio_tracking(rng, log=log)
fig, (a0, a1) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True, gridspec_kw=dict(height_ratios=[1.2, 1]))
a0.fill_between(xs[::200], f(xs[::200]), color="#9bb7d4", alpha=0.7, label="안개 밀도 f(x)")
a0.axhline(M, color="#c0392b", ls="--", lw=1.2, label="상한 M (어디서도 f 보다 큼)")
for x, _ in log:
    a0.plot([x, x], [0, f(x)], color="#2c3e50", lw=1)
    a0.plot(x, f(x), "o", color="#2c3e50", ms=5)
a0.set_ylim(0, 1.15)
a0.set_ylabel("밀도")
a0.legend(loc="upper left", fontsize=9)
a0.set_title("ratio tracking 한 번: 무작위 간격으로 들르면서, 들른 곳마다 (1 - f/M) 를 곱한다", fontsize=10.5, loc="left")
px = [0] + [p[0] for p in log] + [L]
py = [1] + [p[1] for p in log] + [log[-1][1] if log else 1]
a1.step(px, py, where="post", color="#2c3e50", lw=1.6, label=f"이번 한 번의 결과 → {T1:.3f}")
cum = np.exp(-np.cumsum(f(xs)) * (xs[1] - xs[0]))
a1.plot(xs, cum, color="#e67e22", lw=1.4, label=f"정답 투과율 (끝에서 {T_true:.3f})")
a1.set_ylim(0, 1.05)
a1.set_xlabel("광선을 따라 간 거리")
a1.set_ylabel("투과율")
a1.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig("fig1_one_track.png", dpi=150)
plt.close(fig)

# ---------- 그림 2: 여러 번 평균 내기 vs 레이마칭 ----------
rng = np.random.default_rng(7)
N = 4096
rt = np.array([ratio_tracking(rng) for _ in range(N)])
rt_mean = np.cumsum(rt) / np.arange(1, N + 1)
rm4_fixed = ray_march(4, False, rng)
rm4_jit = np.cumsum([ray_march(4, True, rng) for _ in range(N)]) / np.arange(1, N + 1)
fig, ax = plt.subplots(figsize=(8, 4.2))
n = np.arange(1, N + 1)
ax.semilogx(n, rt_mean, color="#2c3e50", lw=1.5, label="ratio tracking 평균")
ax.semilogx(n, rm4_jit, color="#8e44ad", lw=1.2, label="4걸음 레이마칭, 시작점 흔들기 평균")
ax.axhline(rm4_fixed, color="#27ae60", lw=1.2, ls=":", label=f"4걸음 레이마칭, 고정 ({rm4_fixed:.3f})")
ax.axhline(T_true, color="#e67e22", lw=2, ls="--", label=f"정답 ({T_true:.3f})")
ax.set_xlabel("평균 낸 횟수")
ax.set_ylabel("투과율 추정값")
ax.set_ylim(0.0, 0.3)
ax.legend(fontsize=9, loc="upper right")
ax.set_title("ratio tracking 은 평균 낼수록 정답으로, 성긴 레이마칭은 엉뚱한 값으로", fontsize=10.5, loc="left")
fig.tight_layout()
fig.savefig("fig2_converge.png", dpi=150)
plt.close(fig)
print(f"I={I_true:.4f} T={T_true:.4f}")
print(f"ratio tracking mean({N})={rt.mean():.4f}  std(one)={rt.std():.4f}  zero-ratio={np.mean(rt == 0):.3f}")
print(f"ray march 4 fixed={rm4_fixed:.4f}  jitter mean={rm4_jit[-1]:.4f}")
counts = []
rng2 = np.random.default_rng(1)
for _ in range(2000):
    lg = []
    ratio_tracking(rng2, log=lg)
    counts.append(len(lg))
print(f"mean density lookups per track={np.mean(counts):.2f} (M*L={M*L})")

# ---------- 그림 3: 연기 한 덩이를 위에서 비춰 본 투과율 ----------
H = W = 96
yy, xx = np.mgrid[0:H, 0:W] / (H - 1)
rng = np.random.default_rng(5)
# 픽셀마다 광선 하나가 z 방향으로 지나간다고 치고, 밀도는 (x, y, z) 함수
def smoke(px, py, z):
    r2 = (px - 0.5) ** 2 + (py - 0.5) ** 2 + (z - 0.5) ** 2
    wob = 0.5 + 0.5 * np.sin(14 * px + 3 * z) * np.sin(11 * py - 2 * z)
    return np.clip(4.0 * np.exp(-r2 / 0.06) * (0.6 + 0.4 * wob), 0, None)

Mimg = 4.0  # smoke() 의 최댓값보다 크거나 같다
zs = np.linspace(0, 1, 801)
exact = np.exp(-np.trapezoid(smoke(xx[..., None], yy[..., None], zs), zs, axis=-1))

def rt_image(spp):
    acc = np.zeros((H, W))
    for _ in range(spp):
        for i in range(H):
            for j in range(W):
                acc[i, j] += ratio_tracking(rng, L=1.0, M=Mimg,
                                            dens=lambda z: smoke(xx[i, j], yy[i, j], z))
    return acc / spp

img1 = rt_image(1)
img16 = rt_image(16)
fig, axs = plt.subplots(1, 3, figsize=(9, 3.4))
for a, im, t in zip(axs, [img1, img16, exact], ["광선마다 1번", "광선마다 16번 평균", "정답 (촘촘한 적분)"]):
    a.imshow(im, cmap="gray", vmin=0, vmax=1)
    a.set_title(t, fontsize=11)
    a.axis("off")
fig.suptitle("연기 덩어리 너머로 보이는 빛의 양(투과율). 밝을수록 잘 비침", fontsize=11, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig("fig3_smoke_noise.png", dpi=150)
plt.close(fig)
print(f"smoke: mean|err| 1spp={np.abs(img1-exact).mean():.4f} 16spp={np.abs(img16-exact).mean():.4f} bias16={(img16-exact).mean():+.4f}")
assert smoke(xx[..., None], yy[..., None], zs).max() <= Mimg
