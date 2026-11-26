# 'Bluey's Happy Snaps' 2D 파이프라인 소개글에 쓴 그림을 만드는 코드 (jpcorps.com 2026-11-27)
# 모두 원리를 보여 주는 장난감이다. 게임 속 캐릭터나 실제 데이터가 아니다.
# 실행: python3 make_figures.py   (numpy, scipy, matplotlib 필요, 수 초)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import ndimage

KO_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(KO_PATH)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=KO_PATH).get_name()

# ---------------- 그림 1: RGBA 네 칸에 모양 네 개, 64x64 한 장 ----------------
HI = 1024           # 정답 모양을 그릴 고해상도
LO = 64             # 실제 텍스처 크기
OUT = 512           # 화면에 크게 띄울 크기
SPREAD = 6.0        # SDF 가 담는 거리 범위 (텍스처 텍셀 단위, ±)

yy, xx = np.mgrid[0:HI, 0:HI] / HI  # 0..1

def circle(cx, cy, r):
    return (xx - cx) ** 2 + (yy - cy) ** 2 < r * r

canopy = circle(0.5, 0.36, 0.26) | circle(0.30, 0.48, 0.17) | circle(0.70, 0.48, 0.17)          # R: 나뭇잎 덩어리
trunk = (np.abs(xx - 0.5) < 0.07) & (yy > 0.55) & (yy < 0.92)                                    # G: 줄기
spots = circle(0.40, 0.30, 0.045) | circle(0.60, 0.42, 0.05) | circle(0.47, 0.50, 0.035)          # B: 무늬
shade = canopy & ((xx - 0.40) ** 2 + (yy - 0.26) ** 2 > 0.30 ** 2)                               # A: 그늘(손으로 칠한 듯한 영역)
masks = [canopy, trunk, spots, shade]

def sdf_lowres(mask):
    """고해상도 마스크 -> 64x64 SDF (안쪽 +, 바깥 -, 텍셀 단위를 SPREAD 로 나눠 0..1 로)"""
    inside = ndimage.distance_transform_edt(mask)
    outside = ndimage.distance_transform_edt(~mask)
    d = (inside - outside) / (HI / LO)                     # 텍스처 텍셀 단위 거리
    step = HI // LO
    d = d[step // 2::step, step // 2::step]               # 텍셀 중심에서 샘플
    return np.clip(0.5 + 0.5 * d / SPREAD, 0, 1)          # 0..1 에 담기 (0.5 가 경계)

tex = np.stack([sdf_lowres(m) for m in masks], -1)       # 64x64x4
tex8 = np.round(tex * 255) / 255                         # 8비트로 저장했다고 치기

def bilinear(img, n):
    """텍스처를 n x n 화면에 GPU 처럼 쌍선형으로 읽기"""
    h, w = img.shape[:2]
    u = (np.arange(n) + 0.5) / n * w - 0.5
    v = (np.arange(n) + 0.5) / n * h - 0.5
    x0 = np.clip(np.floor(u).astype(int), 0, w - 1); x1 = np.clip(x0 + 1, 0, w - 1); fx = np.clip(u - np.floor(u), 0, 1)
    y0 = np.clip(np.floor(v).astype(int), 0, h - 1); y1 = np.clip(y0 + 1, 0, h - 1); fy = np.clip(v - np.floor(v), 0, 1)
    a = img[y0][:, x0]; b = img[y0][:, x1]; c = img[y1][:, x0]; d = img[y1][:, x1]
    fx = fx[None, :, None] if img.ndim == 3 else fx[None, :]
    fy = fy[:, None, None] if img.ndim == 3 else fy[:, None]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

PAL = dict(bg=np.array([0.96, 0.94, 0.88]), leaf=np.array([0.45, 0.70, 0.40]), leaf_dark=np.array([0.32, 0.55, 0.33]),
           trunk=np.array([0.62, 0.44, 0.30]), spot=np.array([0.95, 0.80, 0.35]), line=np.array([0.22, 0.20, 0.25]))

def shade_from_sdf(t, n):
    """SDF 텍스처 -> 색. 경계 부드럽게 하는 폭은 화면 1픽셀, 외곽선은 화면 픽셀 기준 일정 두께"""
    s = bilinear(t, n)
    px = 1.0 / (n / LO) / SPREAD * 0.5                   # 화면 1픽셀이 SDF 값으로 얼마인지
    cov = lambda ch, off=0.0: smoothstep(0.5 - px + off, 0.5 + px + off, s[..., ch])
    line_w = 2.5 * px                                    # 외곽선: 화면에서 약 2.5픽셀
    col = np.ones((n, n, 3)) * PAL["bg"]
    for ch, base in [(1, PAL["trunk"]), (0, PAL["leaf"])]:
        outer = cov(ch, -line_w)                         # 조금 부풀린 모양 = 외곽선까지 포함
        col = col * (1 - outer[..., None]) + PAL["line"] * outer[..., None]
        inner = cov(ch)
        col = col * (1 - inner[..., None]) + base * inner[..., None]
    leaf = cov(0)
    dark = cov(3) * leaf
    col = col * (1 - dark[..., None]) + PAL["leaf_dark"] * dark[..., None]
    sp = cov(2) * leaf
    col = col * (1 - sp[..., None]) + PAL["spot"] * sp[..., None]
    return np.clip(col, 0, 1)

# 비교용: 같은 64x64 크기에 색을 그대로 칠한 평범한 그림(비트맵)
hi_col = shade_from_sdf(np.stack([sdf_lowres(m) for m in masks], -1), HI)  # 정답에 가까운 고해상도 그림
step = HI // LO
bitmap = hi_col.reshape(LO, step, LO, step, 3).mean((1, 3))               # 64x64 로 줄인 색 그림
bmp_big = np.clip(bilinear(bitmap, OUT), 0, 1)
sdf_big = shade_from_sdf(tex8, OUT)

fig, axs = plt.subplots(1, 6, figsize=(15, 3.2), dpi=150,
                        gridspec_kw=dict(width_ratios=[1, 1, 1, 1, 2.2, 2.2]))
names = ["R: 잎 덩어리", "G: 줄기", "B: 무늬", "A: 그늘"]
for i in range(4):
    axs[i].imshow(tex8[..., i], cmap="gray", vmin=0, vmax=1, interpolation="nearest")
    axs[i].set_title(names[i], fontsize=10)
crop = slice(OUT // 8, OUT * 5 // 8), slice(OUT // 8, OUT * 5 // 8)          # 잎 왼쪽 위를 확대
axs[4].imshow(bmp_big[crop]); axs[4].set_title("색 그림 64×64 를 늘린 것", fontsize=10)
axs[5].imshow(sdf_big[crop]); axs[5].set_title("SDF 64×64 (RGBA) 로 그린 것", fontsize=10)
for a in axs: a.set_xticks([]); a.set_yticks([])
fig.suptitle("같은 64×64 텍스처 한 장, 같은 메모리. 늘렸을 때 경계가 다르다", fontsize=12)
fig.tight_layout(); fig.savefig("fig1_sdf_channels.png"); plt.close(fig)

# ---------------- 그림 2: 8방향 카드 고르기 + 겹친 판이 옆에서 벌어지는 정도 ----------------
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), dpi=150)
ax = axs[0]
for k in range(8):
    a0 = np.radians(k * 45 - 22.5)
    a1 = np.radians(k * 45 + 22.5)
    th = np.linspace(a0, a1, 30)
    ax.fill(np.r_[0, np.cos(th), 0], np.r_[0, np.sin(th), 0], color=plt.cm.tab20(k * 2 % 20), alpha=0.35, lw=0)
    ax.text(0.72 * np.cos(np.radians(k * 45)), 0.72 * np.sin(np.radians(k * 45)), f"{k}번\n{k*45}°",
            ha="center", va="center", fontsize=9)
ax.plot(0, 0, "ko", ms=6); ax.text(0, -0.1, "캐릭터", ha="center", va="top", fontsize=9)
cam = np.radians(110)
ax.annotate("", xy=(0.05 * np.cos(cam), 0.05 * np.sin(cam)), xytext=(1.15 * np.cos(cam), 1.15 * np.sin(cam)),
            arrowprops=dict(arrowstyle="->", lw=1.5))
ax.text(1.22 * np.cos(cam), 1.22 * np.sin(cam), "카메라 110°\n→ 가장 가까운 2번(90°) 그림", ha="center", fontsize=9)
idx = int(np.round(110 / 45)) % 8
assert idx == 2
ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.2, 1.45); ax.axis("off")
ax.set_title("위에서 본 모습: 45°마다 그림 한 벌, 모두 8벌", fontsize=11)

ax = axs[1]
pitch = np.linspace(0, 80, 200)                          # 카메라를 위아래로 기울인 각도
gap = 0.10                                               # 판 사이 간격(장난감 단위)
for g, lab, c in [(gap, "판 간격 그대로", "#d05a3a"), (gap * 0.25, "간격을 1/4 로 눌렀을 때", "#3a7bd0")]:
    shift = 2 * g * np.sin(np.radians(pitch))            # 앞판과 뒷판(2칸 떨어짐)이 화면에서 어긋나는 양
    ax.plot(pitch, shift, color=c, lw=2, label=lab)
ax.set_xlabel("카메라를 위·아래로 기울인 각도 (°)")
ax.set_ylabel("앞판과 뒷판이 화면에서 어긋나는 양")
ax.set_title("겹친 판은 비스듬히 볼수록 벌어진다 (장난감 계산)", fontsize=11)
ax.legend(frameon=False); ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.tight_layout(); fig.savefig("fig2_eight_angles.png"); plt.close(fig)

# ---------------- 그림 3: 외곽선 두께, 거리와 상관없이 ----------------
W, H = 1280, 720
fov = np.radians(60)
f = 1 / np.tan(fov / 2)
def proj(p):  # 원근 투영: 뷰 공간 점 -> 클립 공간 (x, y, w)
    x, y, z = p
    return np.array([f * x * H / W, f * y, z])           # w = 카메라에서의 깊이 z

def screen(c):  # 클립 -> 화면 픽셀
    return np.array([(c[0] / c[2] * 0.5 + 0.5) * W, (c[1] / c[2] * 0.5 + 0.5) * H])

dists = np.linspace(2, 40, 60)
world_push = 0.02                                        # 보통 뒤집은 껍데기: 월드에서 2cm 부풀리기
target_px = 3.0                                          # 화면에서 늘 3픽셀로
px_world, px_const = [], []
for d in dists:
    p = np.array([0.5, 0.0, d]); n = np.array([1.0, 0.0, 0.0])          # 공 오른쪽 끝 점과 그 법선
    # (가) 월드 공간에서 고정 거리만큼 부풀리기
    px_world.append(screen(proj(p + n * world_push))[0] - screen(proj(p))[0])
    # (나) 클립 공간에서 부풀리고 w 를 곱하기 — 아래 HLSL 과 같은 계산
    c = proj(p)
    cn = proj(n) ; cn = cn[:2] / np.linalg.norm(cn[:2])
    c2 = c.copy(); c2[:2] += cn / np.array([W, H]) * target_px * 2.0 * c[2]
    px_const.append(screen(c2)[0] - screen(c)[0])
px_world = np.array(px_world); px_const = np.array(px_const)
assert np.allclose(px_const, target_px, atol=1e-6), px_const[:3]

fig, ax = plt.subplots(figsize=(8, 3.8), dpi=150)
ax.plot(dists, px_world, lw=2, color="#d05a3a", label="월드에서 2cm 부풀리기 (흔한 방법)")
ax.plot(dists, px_const, lw=2, color="#3a7bd0", label="화면에서 3픽셀로 맞추기 (w 곱하기)")
ax.set_xlabel("카메라와의 거리 (m)"); ax.set_ylabel("화면에 보이는 외곽선 두께 (픽셀)")
ax.set_ylim(0, max(px_world.max(), 4) * 1.05)
ax.set_title("1280×720, 시야각 60° 장난감 계산: 멀어지면 선이 가늘어진다", fontsize=11)
ax.legend(frameon=False); ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.tight_layout(); fig.savefig("fig3_outline_thickness.png"); plt.close(fig)
print("world px at 2m, 10m, 40m:", np.interp([2, 10, 40], dists, px_world).round(2))
print("const px:", px_const.min().round(3), px_const.max().round(3))
