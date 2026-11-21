"""
'코사인 팔레트' 글(2026-11-22) 그림 5장. python3 make_figures.py 로 실행 (수 초).
식은 Inigo Quilez 글의 color(t) = a + b*cos(2*pi*(c*t + d)) 그대로이고,
예시 숫자 7세트도 원문 표의 값이다. 그림과 코드는 직접 새로 만들었다.
셰이더토이처럼 계산 결과를 그대로 화면 값으로 쓴다(감마 변환 없음).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "Noto Sans CJK KR", "font.size": 11,
                     "axes.unicode_minus": False})
BG, FG = "#1a1a2e", "white"


def palette(t, a, b, c, d):
    t = np.asarray(t, dtype=float)[..., None]
    a, b, c, d = (np.asarray(v, dtype=float) for v in (a, b, c, d))
    return np.clip(a + b * np.cos(2 * np.pi * (c * t + d)), 0, 1)


# 원문 표의 일곱 세트 (a, b, c, d)
EXAMPLES = [
    ((.5, .5, .5), (.5, .5, .5), (1, 1, 1), (0.00, 0.33, 0.67)),
    ((.5, .5, .5), (.5, .5, .5), (1, 1, 1), (0.00, 0.10, 0.20)),
    ((.5, .5, .5), (.5, .5, .5), (1, 1, 1), (0.30, 0.20, 0.20)),
    ((.5, .5, .5), (.5, .5, .5), (1, 1, .5), (0.80, 0.90, 0.30)),
    ((.5, .5, .5), (.5, .5, .5), (1, .7, .4), (0.00, 0.15, 0.20)),
    ((.5, .5, .5), (.5, .5, .5), (2, 1, 0), (0.50, 0.20, 0.25)),
    ((.8, .5, .4), (.2, .4, .2), (2, 1, 1), (0.00, 0.25, 0.25)),
]


def style(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_color("#666")
    ax.tick_params(colors="#bbb")


# ── 그림 1: 코사인 하나에 a, b, c, d 가 하는 일 ─────────────────────────
t = np.linspace(0, 1, 400)
fig, axs = plt.subplots(2, 2, figsize=(9, 5.6), facecolor=BG)
cases = [
    ("a: 가운데 높이 (밝기)", [(0.5, 0.5, 1, 0), (0.7, 0.5, 1, 0)], ["a=0.5", "a=0.7"]),
    ("b: 출렁임 폭 (대비)", [(0.5, 0.5, 1, 0), (0.5, 0.2, 1, 0)], ["b=0.5", "b=0.2"]),
    ("c: 0→1 동안 몇 번 출렁이나", [(0.5, 0.5, 1, 0), (0.5, 0.5, 2, 0)], ["c=1", "c=2"]),
    ("d: 옆으로 얼마나 밀까 (위상)", [(0.5, 0.5, 1, 0), (0.5, 0.5, 1, 0.25)], ["d=0", "d=0.25"]),
]
for ax, (title, params, labels) in zip(axs.flat, cases):
    style(ax)
    for (a, b, c, d), lab, col in zip(params, labels, ["#9ad0ff", "#ffb36b"]):
        ax.plot(t, a + b * np.cos(2 * np.pi * (c * t + d)), color=col, lw=2.2, label=lab)
    ax.set_ylim(-0.05, 1.25)
    ax.set_title(title, color=FG, fontsize=12)
    ax.legend(facecolor=BG, edgecolor="#666", labelcolor=FG, fontsize=9, loc="upper right")
    ax.set_xlabel("t", color="#bbb")
fig.tight_layout()
fig.savefig("fig1_abcd.png", dpi=110, facecolor=BG)
plt.close(fig)

# ── 그림 2: 무지개 팔레트(예시 1)를 채널별로 뜯어 보기 ──────────────────
a, b, c, d = EXAMPLES[0]
fig = plt.figure(figsize=(9, 4.6), facecolor=BG)
ax = fig.add_axes([0.08, 0.32, 0.88, 0.6])
style(ax)
for i, (col, name) in enumerate(zip(["#ff5555", "#55dd55", "#5599ff"], ["R (d=0.00)", "G (d=0.33)", "B (d=0.67)"])):
    ax.plot(t, a[i] + b[i] * np.cos(2 * np.pi * (c[i] * t + d[i])), color=col, lw=2.2, label=name)
ax.set_xlim(0, 1)
ax.set_ylim(-0.05, 1.05)
ax.set_xticks([])
ax.legend(facecolor=BG, edgecolor="#666", labelcolor=FG, fontsize=9, ncol=3, loc="upper center")
ax.set_title("같은 코사인 세 개를 1/3씩 어긋나게 → 무지개", color=FG, fontsize=12)
ax2 = fig.add_axes([0.08, 0.1, 0.88, 0.16])
ax2.imshow(palette(t, a, b, c, d)[None].repeat(30, 0), aspect="auto", extent=[0, 1, 0, 1])
ax2.set_yticks([])
ax2.tick_params(colors="#bbb")
ax2.set_xlabel("t", color="#bbb")
fig.savefig("fig2_rainbow.png", dpi=110, facecolor=BG)
plt.close(fig)

# ── 그림 3: 원문 표의 일곱 세트를 띠로 그려 보기 ───────────────────────
fig, axs = plt.subplots(len(EXAMPLES), 1, figsize=(9, 5.2), facecolor=BG)
for i, (ax, p) in enumerate(zip(axs, EXAMPLES)):
    ax.imshow(palette(t, *p)[None].repeat(20, 0), aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(-8, 10, str(i + 1), color=FG, ha="right", va="center", fontsize=12)
fig.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.02, hspace=0.25)
fig.savefig("fig3_examples.png", dpi=110, facecolor=BG)
plt.close(fig)

# ── 그림 4: 흑백 값에 색 입히기 (높이 지도) ─────────────────────────────
rng = np.random.default_rng(7)
N = 256


def value_noise(n, cells):
    g = rng.random((cells + 1, cells + 1))
    x = np.linspace(0, cells, n, endpoint=False)
    i = x.astype(int)
    f = x - i
    f = f * f * (3 - 2 * f)
    a_ = g[i][:, i]
    b_ = g[i][:, i + 1]
    c_ = g[i + 1][:, i]
    d_ = g[i + 1][:, i + 1]
    fx, fy = f[None, :], f[:, None]
    return (a_ * (1 - fx) + b_ * fx) * (1 - fy) + (c_ * (1 - fx) + d_ * fx) * fy


h = sum(value_noise(N, 4 * 2 ** o) * 0.5 ** o for o in range(5))
h = (h - h.min()) / (h.max() - h.min())
fig, axs = plt.subplots(1, 3, figsize=(10, 3.7), facecolor=BG)
imgs = [np.repeat(h[..., None], 3, 2), palette(h, *EXAMPLES[0]), palette(h, *EXAMPLES[6])]
titles = ["원래 흑백 값", "팔레트 1 (무지개)", "팔레트 7"]
for ax, im, ti in zip(axs, imgs, titles):
    ax.imshow(im)
    ax.set_title(ti, color=FG, fontsize=12)
    ax.axis("off")
fig.tight_layout()
fig.savefig("fig4_colorize.png", dpi=110, facecolor=BG)
plt.close(fig)

# ── 그림 5: 바탕색에 곱해서 '조금씩 다른' 풀잎 만들기 ───────────────────
BASE = np.array([0.35, 0.6, 0.25])                 # 풀잎 바탕색
VAR = ((0.85, 0.85, 0.85), (0.3, 0.25, 0.2), (1, 1, 1), (0.0, 0.1, 0.25))  # 얌전한 팔레트(직접 고른 값)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), facecolor=BG)
for k, ax in enumerate(axs):
    ax.set_facecolor("#2b2418")
    rng2 = np.random.default_rng(3)
    for j in range(90):
        x0 = rng2.random() * 10
        hgt = 1.5 + rng2.random() * 2
        lean = (rng2.random() - 0.5) * 1.2
        tid = rng2.random()                          # 풀잎마다 다른 번호 → t
        col = BASE * palette(tid, *VAR) if k == 1 else BASE
        ax.fill([x0 - 0.12, x0 + 0.12, x0 + lean], [0, 0, hgt], color=np.clip(col, 0, 1), lw=0)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(["모두 같은 색", "바탕색 × 팔레트(풀잎마다 t 다르게)"][k], color=FG, fontsize=12)
fig.tight_layout()
fig.savefig("fig5_grass.png", dpi=110, facecolor=BG)
plt.close(fig)

# ── 그림 6: c 를 0.5 의 배수로 안 두면 반복할 때 이음매가 생긴다 ──────────
tt = np.linspace(0, 3, 900) % 1.0
fig, axs = plt.subplots(2, 1, figsize=(9, 2.6), facecolor=BG)
for ax, cc, lab in zip(axs, [1.0, 0.7], ["c = 1.0 : 세 번 이어 붙여도 매끈", "c = 0.7 : 이어 붙인 자리가 툭 끊긴다"]):
    p = ((.5, .5, .5), (.5, .5, .5), (cc, cc, cc), (0.0, 0.33, 0.67))
    ax.imshow(palette(tt, *p)[None].repeat(20, 0), aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(lab, color=FG, fontsize=11)
fig.tight_layout()
fig.savefig("fig6_seam.png", dpi=110, facecolor=BG)
plt.close(fig)

print("done")
