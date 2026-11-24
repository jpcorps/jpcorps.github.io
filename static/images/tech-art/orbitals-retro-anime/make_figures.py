# Orbitals 렌더링 소개글에 쓴 그림을 만드는 장난감 코드 (jpcorps.com 2026-11-25)
# 원문 셰이더가 아니라, 원문이 글로 설명한 '생각'을 흉내 낸 2D 계산이다.
# 실행: python3 make_figures.py   (numpy, scipy, matplotlib 필요, 1~2초)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.ndimage import gaussian_filter, map_coordinates

KO_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(KO_PATH)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=KO_PATH).get_name()

N = 320
ys, xs = np.mgrid[0:N, 0:N]
u = (xs + 0.5) / N * 2 - 1           # -1..1
v = 1 - (ys + 0.5) / N * 2           # 위가 +
L = np.array([-0.55, 0.6, 0.58]); L /= np.linalg.norm(L)


def sphere(cx, cy, cz, r):
    """정면 직교 카메라로 구를 그린다. 깊이(작을수록 가까움), 법선, 마스크를 돌려준다."""
    dx, dy = u - cx, v - cy
    d2 = r * r - dx * dx - dy * dy
    m = d2 > 0
    dz = np.sqrt(np.clip(d2, 0, None))
    depth = np.where(m, cz - dz, np.inf)
    n = np.stack([dx, dy, dz], -1) / r
    return depth, n, m


# 장면: 큰 구(몸통, 물체 1) 앞에 작은 구(머리, 물체 2). 몸통 위쪽 띠는 '면 번호'가 다른 옷깃.
dA, nA, mA = sphere(-0.12, -0.18, 0.0, 0.62)
dB, nB, mB = sphere(0.33, 0.40, -0.5, 0.36)
front_B = dB < dA
depth = np.where(front_B, dB, dA)
normal = np.where(front_B[..., None], nB, nA)
obj = np.where(np.isinf(depth), 0, np.where(front_B, 2, 1))
surf = obj.copy()
collar = (obj == 1) & (np.abs(v - (-0.18) - 0.30 - 0.12 * u) < 0.07)
surf[collar] = 3                       # 같은 물체 안의 다른 면 -> 안쪽 선이 생겨야 하는 곳
ndl = np.clip((normal * L).sum(-1), -1, 1)

# 물체마다 아티스트가 정한 3단계 색 (밝음, 중간, 그늘)
PAL = {1: [(0.98, 0.80, 0.55), (0.90, 0.62, 0.42), (0.62, 0.38, 0.36)],
       2: [(0.70, 0.86, 0.98), (0.48, 0.66, 0.90), (0.32, 0.38, 0.66)],
       3: [(0.95, 0.95, 0.90), (0.82, 0.82, 0.80), (0.55, 0.55, 0.62)]}
BG = np.array([0.93, 0.90, 0.82])


def shade_cel(ndl_field, surf_field, t1=0.35, t2=-0.05):
    img = np.tile(BG, (N, N, 1)).astype(float)
    for k, cols in PAL.items():
        m = surf_field == k
        step = np.where(ndl_field > t1, 0, np.where(ndl_field > t2, 1, 2))
        for s in range(3):
            img[m & (step == s)] = cols[s]
    return img


def shade_smooth():
    img = np.tile(BG, (N, N, 1)).astype(float)
    lam = np.clip(ndl, 0, 1) * 0.8 + 0.2
    for k, cols in PAL.items():
        m = surf == k
        img[m] = np.array(cols[1])[None] * lam[m][:, None] * 1.15
    return np.clip(img, 0, 1)


# ---------- 그림 1: 부드러운 명암 vs 3단계 셀 ----------
fig, ax = plt.subplots(1, 2, figsize=(8, 4.2))
ax[0].imshow(shade_smooth()); ax[0].set_title("보통 3D 명암 (부드럽게 이어짐)")
ax[1].imshow(shade_cel(ndl, surf)); ax[1].set_title("셀 셰이딩 (물체마다 정한 색 3단계)")
for a in ax: a.axis("off")
plt.tight_layout(); plt.savefig("fig1_cel_steps.png", dpi=110, bbox_inches="tight"); plt.close()


# ---------- 그림 2: 번호 버퍼 + 깊이로 선 뽑기 ----------
def line_masks(surf_f, obj_f, depth_f, radius=2.0, ztol=0.08):
    """주변 8방향을 radius 픽셀 떨어진 곳에서 읽어(UV 오프셋) 다르면 선."""
    d = np.where(np.isinf(depth_f), 10.0, depth_f)
    outer = np.zeros((N, N), bool); inner = np.zeros((N, N), bool)
    for ang in np.arange(8) * np.pi / 4:
        ox, oy = int(round(np.cos(ang) * radius)), int(round(np.sin(ang) * radius))
        s2 = np.roll(np.roll(surf_f, oy, 0), ox, 1)
        o2 = np.roll(np.roll(obj_f, oy, 0), ox, 1)
        d2 = np.roll(np.roll(d, oy, 0), ox, 1)
        outer |= (o2 != obj_f) & (d < d2 - ztol)        # 내가 더 앞에 있을 때만: 선이 한 줄로
        outer |= (obj_f > 0) & (o2 == 0)
        inner |= (o2 == obj_f) & (s2 != surf_f) & (obj_f > 0)
    return outer, inner


outer, inner = line_masks(surf, obj, depth)
fig, ax = plt.subplots(1, 3, figsize=(11, 4))
cmap = matplotlib.colors.ListedColormap([BG, (0.85, 0.5, 0.3), (0.3, 0.5, 0.9), (0.6, 0.85, 0.5)])
ax[0].imshow(surf, cmap=cmap, vmin=0, vmax=3); ax[0].set_title("① 면 번호 버퍼\n(색 = 번호, 옷깃은 다른 번호)")
dd = np.where(np.isinf(depth), np.nan, depth)
ax[1].imshow(dd, cmap="gray"); ax[1].set_title("② 깊이 버퍼\n(어두울수록 가까움)")
lines = np.ones((N, N, 3)); lines[outer] = (0.1, 0.1, 0.15); lines[inner] = (0.85, 0.2, 0.2)
ax[2].imshow(lines); ax[2].set_title("③ 이웃과 비교해 뽑은 선\n(검정 = 바깥선, 빨강 = 안쪽 선)")
for a in ax: a.axis("off")
plt.tight_layout(); plt.savefig("fig2_line_from_ids.png", dpi=110, bbox_inches="tight"); plt.close()


# ---------- 그림 3: 흐리고, 깎고, 노이즈로 끊기 + 셀 흔들기 ----------
def value_noise(seed, scale):
    rng = np.random.default_rng(seed)
    g = rng.random((N // scale + 2, N // scale + 2))
    return map_coordinates(g, [ys / scale, xs / scale], order=3, mode="nearest")


def hand_drawn(seed):
    # 셀 명암 경계도 노이즈로 살짝 흔든다
    wob = (value_noise(seed + 100, 24) - 0.5) * 0.16
    img = shade_cel(ndl + wob, surf)
    m = (outer | inner).astype(float)
    soft = gaussian_filter(m, 1.6)                       # 흐리게 -> 굵기 조절 여지
    soft = soft / soft.max()
    width = 0.18 + 0.22 * value_noise(seed + 7, 40)       # 깎는 문턱값이 곳곳에서 달라 굵기가 달라짐
    breaks = value_noise(seed + 3, 14)                    # 이 값이 크면 선을 뺀다 -> 끊김
    alpha = np.clip((soft - width) * 6, 0, 1) * np.clip((0.80 - breaks) * 8, 0, 1)
    ink = np.array([0.12, 0.10, 0.14])
    return img * (1 - alpha[..., None]) + ink * alpha[..., None]


clean = shade_cel(ndl, surf)
clean[outer | inner] = (0.12, 0.10, 0.14)
fig, ax = plt.subplots(1, 3, figsize=(11, 4))
ax[0].imshow(clean); ax[0].set_title("깔끔한 디지털 결과")
ax[1].imshow(hand_drawn(1)); ax[1].set_title("흐리고·깎고·노이즈로 끊은 선\n+ 명암 경계 흔들기 (다시 그리기 1번)")
ax[2].imshow(hand_drawn(2)); ax[2].set_title("같은 장면, '다시 그리기' 2번\n(움직일 때만 이렇게 바뀜)")
for a in ax: a.axis("off")
plt.tight_layout(); plt.savefig("fig3_imperfect_lines.png", dpi=110, bbox_inches="tight"); plt.close()


# ---------- 그림 4: 화면은 30fps, 셀 움직임은 12fps ----------
t = np.arange(0, 1.0001, 1 / 30)
pos = np.sin(t * np.pi * 1.2)
step12 = np.floor(t * 12 + 1e-6) / 12
pos12 = np.sin(step12 * np.pi * 1.2)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(t, pos, "o-", ms=3, color="#999", label="화면 갱신 (초당 30장): 매번 새 위치")
ax.step(t, pos12, where="post", color="#d9534f", lw=2, label="셀 움직임 (초당 12장): 같은 그림을 2~3장씩 우려먹기")
ax.set_xlabel("시간 (초)"); ax.set_ylabel("물체 위치")
ax.legend(loc="lower center", fontsize=9); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("fig4_stepped_motion.png", dpi=110, bbox_inches="tight"); plt.close()
print("done")
