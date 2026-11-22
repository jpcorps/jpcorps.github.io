"""
'엔드필드 한 프레임' 글(2026-11-23) 그림 4장. python3 make_figures.py 로 실행 (수 초).
원문(Behind the Frame · Endfield)의 그림이 아니라, 개념 설명용으로 직접 만든 장난감 그림이다.
게임의 실제 텍스처·셰이더 값을 쓰지 않았다. (머리카락 하이라이트의 0.06 밀기, 지수 200 만 원문 숫자)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "Noto Sans CJK KR", "font.size": 11,
                     "axes.unicode_minus": False})
BG, FG = "#1a1a2e", "white"


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- 1. 프레임 순서
def fig_flow():
    steps = [
        ("준비", "하늘 표\n그림자 지도\n안개", "#4a6fa5"),
        ("깊이 + G버퍼", "배경과 캐릭터의\n재료 정보를 적어 둠", "#4a6fa5"),
        ("화면 공간 효과", "AO · 반사\n접촉 그림자", "#4a6fa5"),
        ("배경 조명", "디퍼드\n캐릭터 자리는\n건너뜀", "#4a6fa5"),
        ("캐릭터 조명", "포워드\n피부·얼굴·옷\n머리·눈 따로", "#c0504d"),
        ("외곽선 · 덧칠", "외곽선\n머리 채우기\n얼굴·눈 겹치기", "#c0504d"),
        ("마무리", "TAA · 블룸\n톤 매핑 · UI", "#4a6fa5"),
    ]
    fig, ax = plt.subplots(figsize=(12, 3.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 14.4); ax.set_ylim(0, 3.4); ax.axis("off")
    w, gap = 1.75, 0.27
    for i, (t, s, c) in enumerate(steps):
        x = 0.15 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.7), w, 1.9, boxstyle="round,pad=0.03",
                                    fc=c, ec="none"))
        ax.text(x + w / 2, 2.25, t, ha="center", va="center", color=FG,
                fontsize=12, weight="bold")
        ax.text(x + w / 2, 1.35, s, ha="center", va="center", color=FG, fontsize=9)
        if i < len(steps) - 1:
            ax.annotate("", (x + w + gap - 0.02, 1.65), (x + w + 0.02, 1.65),
                        arrowprops=dict(arrowstyle="->", color=FG, lw=1.5))
    ax.text(7.2, 0.3, "파란 칸: 배경과 캐릭터가 같이 쓰는 단계    빨간 칸: 캐릭터만을 위한 단계",
            ha="center", color="#cccccc", fontsize=10)
    ax.text(7.2, 3.1, "엔드필드 한 프레임의 큰 순서 (원문 분석을 간추려 다시 그림)",
            ha="center", color=FG, fontsize=13)
    fig.savefig("fig1_frame_flow.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- 2. 스텐실로 길 나누기
def fig_stencil():
    n = 240
    y, x = np.mgrid[0:n, 0:n] / n
    # 바닥과 벽(배경), 가운데 캡슐 모양 캐릭터
    ground = y > 0.62
    char = (((x - 0.5) / 0.13) ** 2 + ((y - 0.36) / 0.11) ** 2 < 1) | \
           ((np.abs(x - 0.5) < 0.1) & (y > 0.43) & (y < 0.8))
    tag = np.where(char, 4, np.where(ground, 1, 0))

    sky = np.stack([0.45 + 0.2 * (1 - y), 0.6 + 0.2 * (1 - y), 0.85 + 0 * y], -1)
    floor = np.stack([0.55 + 0 * y, 0.5 + 0 * y, 0.4 + 0 * y], -1) * (0.6 + 0.6 * (y - 0.62))[..., None]
    scene = np.where(ground[..., None], floor, sky)
    shadow = (np.abs(x - 0.62) < 0.13) & (y > 0.78) & (y < 0.84)
    scene = np.where(shadow[..., None], scene * 0.55, scene)

    after_scene = np.where(char[..., None], 0.0, scene)
    # 캐릭터: 램프(두 단계 + 부드러운 경계)로 칠함
    nx = (x - 0.5) / 0.13
    lam = np.clip(0.5 + 0.9 * nx, 0, 1)
    band = smoothstep(0.42, 0.5, lam)
    lit, dark = np.array([1.0, 0.82, 0.72]), np.array([0.72, 0.5, 0.55])
    ccol = dark + (lit - dark) * band[..., None]
    final = np.where(char[..., None], ccol, scene)
    # 외곽선: 캐릭터 경계 바깥 2픽셀
    from numpy import roll
    grow = char.copy()
    for dx in (-3, -2, -1, 1, 2, 3):
        grow |= roll(char, dx, 1) | roll(char, dx, 0)
    outline = grow & ~char
    final2 = np.where(outline[..., None], np.array([0.25, 0.15, 0.2]), final)

    tagcol = np.array([[0.3, 0.45, 0.8], [0.45, 0.7, 0.35], [0, 0, 0], [0, 0, 0], [0.9, 0.35, 0.3]])[tag]
    panels = [(tagcol, "① 스텐실 표시\n(파랑·초록=배경, 빨강=캐릭터)"),
              (after_scene, "② 배경 조명 뒤\n캐릭터 자리는 비어 있음"),
              (final2, "③ 캐릭터 패스 + 외곽선\n같은 깊이 위에 덧그림")]
    fig, axs = plt.subplots(1, 3, figsize=(11, 4.2), facecolor=BG)
    for a, (img, t) in zip(axs, panels):
        a.imshow(np.clip(img, 0, 1)); a.set_title(t, color=FG, fontsize=11); a.axis("off")
    fig.suptitle("장난감 그림: 배경은 디퍼드로, 캐릭터는 나중에 포워드로", color=FG, fontsize=13)
    fig.savefig("fig2_stencil_routing.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- 3. 얼굴 문턱값 지도
def face_mask(n):
    y, x = np.mgrid[0:n, 0:n] / (n - 1) * 2 - 1   # -1..1
    face = (x / 0.8) ** 2 + ((y + 0.05) / 0.95) ** 2 < 1
    return x, y, face


def fig_face():
    n = 260
    x, y, face = face_mask(n)
    # (가) 울퉁불퉁한 메시 노멀로 N·L : 코·광대 굴곡을 흉내 낸 잡음 섞인 노멀
    rng = np.random.default_rng(3)
    nz = np.sqrt(np.clip(1 - (x / 0.85) ** 2 - (y / 1.0) ** 2 * 0.3, 0.02, 1))
    nose = np.exp(-((x / 0.09) ** 2 + ((y - 0.1) / 0.25) ** 2))
    cheek = np.exp(-(((np.abs(x) - 0.45) / 0.18) ** 2 + ((y - 0.25) / 0.15) ** 2))
    bumpx = x / 0.85 + 0.9 * nose * np.sign(x) * 0.0 + 0.5 * np.gradient(nose, axis=1) * n / 8 \
        - 0.35 * np.gradient(cheek, axis=1) * n / 8
    # 저해상도 잡음(메시 면 경계 느낌)
    lo = rng.normal(0, 0.09, (12, 12))
    lo = np.kron(lo, np.ones((n // 12 + 1, n // 12 + 1)))[:n, :n]
    bumpx = bumpx + lo

    # (나) 문턱값 지도: 빛이 정면(0)에서 옆(1)으로 돌 때, 이 픽셀이 '그늘로 바뀌는 시점'
    # 빛이 오른쪽에서 올 때 기준. 오른쪽은 끝까지 밝고, 왼쪽 가장자리부터 그늘이 들어온다.
    T = 0.5 + 0.5 * (x / 0.8)                      # 가로 위치에 따른 기본값
    T = T + 0.10 * np.exp(-((x + 0.02) / 0.1) ** 2 - ((y - 0.05) / 0.3) ** 2)   # 콧날 근처
    T = T - 0.12 * np.exp(-((x + 0.3) / 0.15) ** 2 - ((y - 0.45) / 0.12) ** 2)  # 왼쪽 볼 아래 그늘 모양
    T = np.clip(T, 0, 1)

    def shade_threshold(a, side):
        Tm = T if side > 0 else T[:, ::-1]        # 빛이 반대편이면 지도를 좌우로 뒤집어 읽는다
        return smoothstep(a - 0.02, a + 0.02, Tm)

    def shade_ndl(a, side):
        lx = side * np.sin(a * np.pi / 2); lz = np.cos(a * np.pi / 2)
        ndl = bumpx * lx + nz * lz
        return smoothstep(-0.02, 0.02, ndl)

    lit, dark = np.array([1.0, 0.86, 0.78]), np.array([0.78, 0.58, 0.62])

    def paint(s):
        img = dark + (lit - dark) * s[..., None]
        return np.where(face[..., None], img, np.array([0.1, 0.1, 0.18]))

    cases = [(0.35, 1, "빛: 오른쪽 조금"), (0.7, 1, "빛: 오른쪽 많이"), (0.7, -1, "빛: 왼쪽 많이")]
    fig, axs = plt.subplots(2, 4, figsize=(12, 6.6), facecolor=BG)
    mapimg = np.where(face, T, np.nan)
    axs[0, 0].imshow(mapimg, cmap="gray", vmin=0, vmax=1)
    axs[0, 0].set_title("문턱값 지도 (손으로 그리는 그림)", color=FG, fontsize=10)
    axs[1, 0].imshow(np.where(face, np.clip(0.5 + 0.5 * bumpx, 0, 1), np.nan), cmap="gray")
    axs[1, 0].set_title("울퉁불퉁한 노멀 (가로 성분)", color=FG, fontsize=10)
    for j, (a, s, t) in enumerate(cases, 1):
        axs[0, j].imshow(paint(shade_threshold(a, s)))
        axs[0, j].set_title("지도 방식 · " + t, color=FG, fontsize=10)
        axs[1, j].imshow(paint(shade_ndl(a, s)))
        axs[1, j].set_title("N·L 방식 · " + t, color=FG, fontsize=10)
    for a in axs.ravel():
        a.axis("off")
    fig.suptitle("장난감 그림: 위는 문턱값 지도로, 아래는 노멀 N·L 로 얼굴 그늘 만들기", color=FG, fontsize=13)
    fig.savefig("fig3_face_threshold.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- 4. 머리카락 두 줄 하이라이트
def fig_hair():
    h, w = 300, 220
    v, u = np.mgrid[0:h, 0:w]
    phi = (u / (w - 1) - 0.5) * np.pi * 0.9          # 원기둥 둘레 각도
    t = v / (h - 1)
    # 머리 다발: 위에서 아래로 내려가며 앞으로 살짝 휘는 원기둥
    bend = 1.6 * (t - 0.5)
    N = np.stack([np.sin(phi), -np.sin(bend) * np.cos(phi), np.cos(phi) * np.cos(bend)], -1)
    T = np.stack([0 * phi, np.cos(bend), np.sin(bend)], -1)   # 가닥 방향(아래쪽)
    V = np.array([0, 0, 1.0])
    L = np.array([0.3, 0.1, 0.95]); L /= np.linalg.norm(L)
    H = (L + V); H /= np.linalg.norm(H)
    rng = np.random.default_rng(5)
    stripe = np.repeat(rng.normal(0, 1, (1, w)), h, 0)
    stripe = np.convolve(stripe[0], np.ones(5) / 5, "same")[None, :].repeat(h, 0)

    def lobe(shift, n, jitter):
        Ti = T + N * (shift + jitter * 0.04 * stripe)[..., None]
        Ti /= np.linalg.norm(Ti, axis=-1, keepdims=True)
        th = np.sum(Ti * H, -1)
        return np.sqrt(np.clip(1 - th * th, 0, 1)) ** n

    base = np.array([0.32, 0.22, 0.38])
    diff = np.clip(np.sum(N * L, -1), 0, 1)[..., None] * 0.7 + 0.3

    def render(spec):
        return np.clip(base * diff + 0.75 * spec, 0, 1)

    one = lobe(0.0, 200, 0)[..., None] * np.array([1, 0.95, 0.9])
    two = lobe(0.06, 200, 0)[..., None] * np.array([1, 0.95, 0.9]) + \
        lobe(-0.06, 40, 0)[..., None] * np.array([0.55, 0.35, 0.6]) * 0.7
    three = lobe(0.06, 200, 1)[..., None] * np.array([1, 0.95, 0.9]) + \
        lobe(-0.06, 40, 1)[..., None] * np.array([0.55, 0.35, 0.6]) * 0.7
    fig, axs = plt.subplots(1, 3, figsize=(9, 4.6), facecolor=BG)
    for a, img, ttl in zip(axs, [render(one), render(two), render(three)],
                           ["하이라이트 1줄\n(밀지 않음)", "2줄: 하나는 위로, 하나는 아래로\n밀어서 색과 굵기를 다르게",
                            "2줄 + 가닥마다 미는 양을\n조금씩 흔들기"]):
        a.imshow(img); a.set_title(ttl, color=FG, fontsize=10); a.axis("off")
    fig.suptitle("장난감 그림: 머리 다발(원기둥)의 '가닥 방향' 하이라이트", color=FG, fontsize=13)
    fig.savefig("fig4_hair_highlight.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig_flow(); fig_stencil(); fig_face(); fig_hair()
    print("done")
