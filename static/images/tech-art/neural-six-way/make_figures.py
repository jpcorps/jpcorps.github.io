"""
'뉴럴 6방향 라이트맵' 글(2026-11-20) 그림 4장. python3 make_figures.py 로 실행 (수십 초).
모두 원리를 보여 주는 장난감 계산이며, 원문 논문이나 유니티/언리얼의 실제 코드가 아니다.

- 연기 덩어리: 56^3 격자에 가우시안 덩어리 몇 개 + 노이즈 (비대칭으로 일부러 만듦)
- 조명: 단일 산란(빛이 한 번만 튕김), 등방성 위상 함수, 흰색 평행광 하나
- 카메라: 정사영(orthographic), +z 쪽에서 -z 를 바라봄
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.ndimage import map_coordinates, gaussian_filter

plt.rcParams.update({"font.family": "Noto Sans CJK JP", "font.size": 11,
                     "axes.unicode_minus": False})
BG = np.array([0.10, 0.12, 0.20])
N = 56
rng = np.random.default_rng(3)

# ── 연기 덩어리 만들기 ──────────────────────────────────────────────
c = (np.arange(N) - (N - 1) / 2) / (N / 2)          # -1 ~ 1
X, Y, Z = np.meshgrid(c, c, c, indexing="ij")        # vol[x, y, z]

def blob(cx, cy, cz, sx, sy, sz):
    return np.exp(-(((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2 + ((Z - cz) / sz) ** 2))

dens = (blob(-0.15, -0.25, 0.05, 0.42, 0.30, 0.22)
        + 0.9 * blob(0.30, 0.10, 0.00, 0.30, 0.28, 0.20)
        + 0.8 * blob(-0.35, 0.30, 0.00, 0.22, 0.22, 0.18)
        + 0.9 * blob(0.15, 0.05, -0.55, 0.20, 0.35, 0.30))   # 뒤쪽에 숨은 혹 (옆에서 보면 보임)
noise = gaussian_filter(rng.standard_normal(dens.shape), 2.0)
dens = np.clip(dens * (1 + 2.2 * noise) - 0.18, 0, None)
SIGMA = 9.0 * dens                                    # 소광 계수 (격자 1칸 = 2/N)
DX = 2.0 / N

def light_trans(sig, L, step=0.5):
    """각 칸에서 빛 쪽(L 방향)으로 걸어가며 투과율 T = exp(-적분 sigma) 계산."""
    L = np.asarray(L, float) / np.linalg.norm(L)
    idx = np.indices(sig.shape).reshape(3, -1).astype(float)
    tau = np.zeros(idx.shape[1])
    for s in np.arange(step, N * 1.8, step):
        p = idx + L[:, None] * s
        tau += map_coordinates(sig, p, order=1, mode="constant", cval=0.0) * step * DX
    return np.exp(-tau).reshape(sig.shape)

def render(sig, Tl):
    """+z 카메라에서 -z 로 걸어 들어가며 단일 산란 누적. 반환: 산란광 S, 전체 투과율 T."""
    S = np.zeros((N, N)); T = np.ones((N, N))
    for k in range(N - 1, -1, -1):                    # 카메라에 가까운 칸부터
        a = 1 - np.exp(-sig[:, :, k] * DX)
        S += T * a * Tl[:, :, k]
        T *= 1 - a
    return S, T                                        # 배열은 [x, y]

def to_img(S, T, tint=(1.0, 0.96, 0.9)):
    col = S[..., None] * np.array(tint) + T[..., None] * BG
    img = np.transpose(col, (1, 0, 2))[::-1]          # [y, x] 로, 위가 +y
    return np.clip(img, 0, 1) ** (1 / 2.2)

AXES = {"+X": (1, 0, 0), "-X": (-1, 0, 0), "+Y": (0, 1, 0),
        "-Y": (0, -1, 0), "+Z": (0, 0, 1), "-Z": (0, 0, -1)}

def bake_six(sig):
    maps = {}
    for k, d in AXES.items():
        S, T = render(sig, light_trans(sig, d))
        maps[k] = S
    return maps, T

def six_way(maps, L):
    """빛 방향 성분의 부호로 +/- 그림을 고르고, 성분의 제곱(합이 1)을 가중치로 섞는다.
    (논문 식 5는 성분의 절댓값을 쓴다. 이 장난감에서는 절댓값을 쓰면 대각선 빛일 때
     1.4~1.6배 밝아져서, 합이 1이 되는 제곱을 썼다.)"""
    L = np.asarray(L, float) / np.linalg.norm(L)
    out = np.zeros_like(maps["+X"])
    for i, ax in enumerate("XYZ"):
        out += L[i] ** 2 * maps[("+" if L[i] >= 0 else "-") + ax]
    return out

maps, T_front = bake_six(SIGMA)

# ── 그림 1: 여섯 방향에서 한 번씩 비춰 구운 라이트맵 ───────────────────
names = {"+X": "오른쪽(+X)에서", "-X": "왼쪽(-X)에서", "+Y": "위(+Y)에서",
         "-Y": "아래(-Y)에서", "+Z": "앞(+Z, 카메라 쪽)에서", "-Z": "뒤(-Z)에서"}
fig, axs = plt.subplots(2, 3, figsize=(9, 7.0), facecolor="white")
for ax, k in zip(axs.T.flat, ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]):
    g = np.clip(maps[k] * 1.6, 0, 1).T[::-1] ** (1 / 2.2)      # 흑백 한 채널
    ax.imshow(g, cmap="gray", vmin=0, vmax=1)
    ax.set_title(names[k] + " 비춤", fontsize=11)
    ax.axis("off")
fig.suptitle("같은 연기를 여섯 방향에서 한 번씩 비춰 찍은 흑백 그림 6장", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.94], h_pad=2.0)
fig.savefig("fig1_six_maps.png", dpi=110)
plt.close(fig)

# ── 그림 2: 아무 방향 빛 = 여섯 장 섞기. 정답과 비교 ─────────────────────
tests = [("오른쪽 위", (1, 1, 0.3)), ("왼쪽 앞", (-1, 0.2, 0.8)),
         ("뒤(역광)", (0.3, 0.2, -1)), ("왼쪽 아래 뒤", (-0.6, -0.7, -0.4))]
fig, axs = plt.subplots(2, 4, figsize=(11, 6.9), facecolor="white")
report = []
for j, (lab, L) in enumerate(tests):
    S_true, T = render(SIGMA, light_trans(SIGMA, L))
    S_6 = six_way(maps, L)
    m = (1 - T) > 0.05
    rel = np.abs(S_6 - S_true)[m].mean() / S_true[m].mean()
    bright = S_6[m].sum() / S_true[m].sum()
    report.append((lab, rel, bright))
    axs[0, j].imshow(to_img(S_true * 1.6, T)); axs[0, j].set_title(f"빛: {lab}\n정답(직접 계산)", fontsize=10)
    axs[1, j].imshow(to_img(S_6 * 1.6, T));    axs[1, j].set_title(f"6장 섞기\n평균 오차 {rel*100:.0f}%, 밝기 {bright:.2f}배", fontsize=10)
    for a in axs[:, j]: a.axis("off")
fig.suptitle("빛 방향을 바꿔도, 미리 구운 6장을 섞는 것만으로 꽤 비슷하게 나온다", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.94], h_pad=2.0)
fig.savefig("fig2_relight.png", dpi=110)
plt.close(fig)

# ── 그림 3: 카메라가 옆으로 돌면? 빌보드의 한계 ─────────────────────────
# 옆 카메라(+x 에서 -x 를 봄)에서의 화면 좌표: 오른쪽 = -z, 위 = +y, 카메라 쪽 = +x
side = np.ascontiguousarray(SIGMA.transpose(2, 1, 0)[::-1, :, :])   # side[i,j,k] = SIGMA[k, j, N-1-i]
L_world = np.array([0.4, 0.8, 0.45])
L_cam_side = np.array([-L_world[2], L_world[1], L_world[0]])    # (right, up, toward)
S_f, T_f = render(SIGMA, light_trans(SIGMA, L_world))
S_s, T_s = render(side, light_trans(side, L_cam_side))
S_b = six_way(maps, L_cam_side)                                 # 빌보드는 앞에서 구운 그림을 그대로 씀
fig, axs = plt.subplots(1, 3, figsize=(10.5, 4.6), facecolor="white")
for a, (img, t) in zip(axs, [(to_img(S_f * 1.6, T_f), "앞에서 본 정답"),
                             (to_img(S_s * 1.6, T_s), "옆으로 90° 돌아가 본 정답"),
                             (to_img(S_b * 1.6, T_front), "옆에서 본 6방향 빌보드\n(앞에서 구운 그림 그대로)")]):
    a.imshow(img); a.set_title(t, fontsize=11); a.axis("off")
fig.suptitle("미리 구운 그림은 '찍은 방향'에서만 맞다 — 옆에서 보면 모양이 그대로", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.94], h_pad=2.0)
fig.savefig("fig3_view_problem.png", dpi=110)
plt.close(fig)

# ── 그림 4: 논문의 흐름 (도식) ────────────────────────────────────────
steps = ["유체 시뮬레이션\n(매 프레임, GPU)", "가이드 맵\n큰 보폭 레이마칭\n산란·투명도·깊이",
         "U-Net\n(신경망)", "6방향 라이트맵\n+ 투명도", "기존 6방향 셰이딩\n(빌보드, 조명 여러 개)"]
fig, ax = plt.subplots(figsize=(11, 2.6), facecolor="white")
ax.set_xlim(0, 11); ax.set_ylim(0, 2.6); ax.axis("off")
cols = ["#dfe9f7", "#e6f4e1", "#fde9cf", "#f2e1f5", "#e3e3e3"]
for i, (t, cc) in enumerate(zip(steps, cols)):
    x = 0.15 + i * 2.2
    ax.add_patch(FancyBboxPatch((x, 0.55), 1.85, 1.5, boxstyle="round,pad=0.05", fc=cc, ec="#555"))
    ax.text(x + 0.925, 1.3, t, ha="center", va="center", fontsize=10)
    if i < 4:
        ax.annotate("", xy=(x + 2.15, 1.3), xytext=(x + 1.95, 1.3),
                    arrowprops=dict(arrowstyle="->", lw=1.6))
ax.text(5.5, 0.18, "가운데 세 칸이 '굽기'를 대신해 매 프레임 일어난다 (논문 그림 3을 바탕으로 간단히 다시 그림)",
        ha="center", fontsize=9.5, color="#444")
fig.savefig("fig4_pipeline.png", dpi=110, bbox_inches="tight")
plt.close(fig)

for lab, rel, b in report:
    print(f"{lab}: 평균 상대 오차 {rel*100:.1f}%, 밝기 비 {b:.3f}")
print("앞/옆 투과율 차이(실루엣):", np.abs((1 - T_f) - (1 - T_s)).mean().round(3))
