# Timberborn 프레임 분석 소개글에 쓴 그림을 만드는 코드 (jpcorps.com 2026-11-26)
# 그림 1, 3 의 숫자는 원문(Alexandre Libório, 'Timberborn Frame Analysis')이 잰 값을 옮겨 그린 것이고,
# 그림 2 는 '주문(드로우 콜)이 잘게 쪼개지면 GPU 가 논다'는 생각을 보여 주는 장난감 모형이다(실측 아님).
# 실행: python3 make_figures.py   (numpy, matplotlib 필요, 1초)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

KO_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(KO_PATH)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=KO_PATH).get_name()
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

C_SHADOW, C_MAIN, C_WATER, C_POST = "#5b6c8f", "#d08c3a", "#3a9bd0", "#8fbf5b"

# ---------- 그림 1: 한 프레임의 시간 나눠 보기 (원문 RGP 측정값) ----------
passes = [("그림자 맵", 5.90, 8345, C_SHADOW),
          ("불투명 물체", 7.20, 11280, C_MAIN),
          ("물", 1.00, 73, C_WATER),
          ("후처리+UI", 0.01, 41, C_POST)]
fig, ax = plt.subplots(figsize=(9, 2.6), dpi=150)
left = 0
for name, ms, draws, c in passes:
    ax.barh(0, ms, left=left, color=c, height=0.5)
    if ms > 0.5:
        ax.text(left + ms / 2, 0, f"{name}\n{ms:.2f} ms", ha="center", va="center", color="white", fontsize=11)
        ax.text(left + ms / 2, -0.45, f"드로우 콜 {draws:,}번", ha="center", va="center", fontsize=10)
    left += ms
ax.annotate("후처리+UI 0.01 ms\n(드로우 콜 41번)", xy=(left, 0.25), xytext=(left - 0.3, 0.75),
            ha="right", fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlim(0, 14.5); ax.set_ylim(-0.75, 1.05)
ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlabel("GPU 시간 (ms) — 한 프레임 합계 약 14.1 ms")
ax.set_title("Timberborn 한 프레임, 어디에 시간이 들었나 (원문 측정값)", fontsize=12)
fig.tight_layout(); fig.savefig("fig1_frame_breakdown.png"); plt.close(fig)

# ---------- 그림 2: 장난감 모형 — 같은 나무 12그루를 따로 주문 vs 한 번에 주문 ----------
# 주문 하나마다 CPU 준비 시간 s, GPU 일 w. GPU 는 주문이 도착해야 일을 시작한다.
def timeline(n_orders, s, w):
    cpu, gpu = [], []
    t_cpu, t_gpu = 0.0, 0.0
    for i in range(n_orders):
        cpu.append((t_cpu, s)); t_cpu += s
        start = max(t_cpu, t_gpu)
        gpu.append((start, w)); t_gpu = start + w
    return cpu, gpu, t_gpu

N_TREE, S, W = 12, 1.0, 0.35            # 나무 한 그루: 준비 1, 그리기 0.35 (단위는 아무거나)
cpu_a, gpu_a, end_a = timeline(N_TREE, S, W)          # 그루마다 주문
cpu_b, gpu_b, end_b = timeline(1, S * 1.3, W * N_TREE)  # 인스턴싱: 주문 한 번(준비 조금 더), 일은 같은 양
busy_a = N_TREE * W / end_a
busy_b = N_TREE * W / end_b

fig, axes = plt.subplots(2, 1, figsize=(9, 3.8), dpi=150, sharex=True)
for ax, cpu, gpu, end, busy, title in [
        (axes[0], cpu_a, gpu_a, end_a, busy_a, f"나무 {N_TREE}그루를 한 그루씩 주문 (드로우 콜 {N_TREE}번)"),
        (axes[1], cpu_b, gpu_b, end_b, busy_b, "같은 나무를 한 번에 주문 (인스턴싱, 드로우 콜 1번)")]:
    ax.broken_barh(cpu, (1, 0.6), facecolors="#999999", edgecolor="white")
    ax.broken_barh(gpu, (0, 0.6), facecolors=C_MAIN, edgecolor="white")
    ax.set_yticks([0.3, 1.3]); ax.set_yticklabels(["GPU\n(그리기)", "CPU\n(주문 준비)"])
    ax.set_title(f"{title} — 끝나는 시각 {end:.1f}, GPU 가 일한 비율 {busy*100:.0f}%", fontsize=10.5, loc="left")
    ax.set_ylim(-0.2, 1.8)
axes[1].set_xlabel("시간 (장난감 단위) — 회색 막대 사이사이, GPU 줄의 빈칸이 'GPU 가 노는 시간'")
fig.tight_layout(); fig.savefig("fig2_draw_call_toy.png"); plt.close(fig)
print(f"toy: separate end={end_a:.2f} busy={busy_a:.2f}, instanced end={end_b:.2f} busy={busy_b:.2f}")

# ---------- 그림 3: 그림자 설정별 프레임 시간 (원문 측정값) ----------
labels = ["끔", "낮음\n1024×1024", "울트라\n8192×8192"]
frame = [6.5, 13.4, 14.5]
pixels = [0, 1024 * 1024, 8192 * 8192]
fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=150)
bars = ax.bar(labels, frame, color=["#8fbf5b", C_SHADOW, C_SHADOW], width=0.55)
for b, f, p in zip(bars, frame, pixels):
    ax.text(b.get_x() + b.get_width() / 2, f + 0.3, f"{f} ms", ha="center", fontsize=11)
    if p:
        ax.text(b.get_x() + b.get_width() / 2, f / 2, f"그림자 맵 픽셀\n약 {p/1e4:,.0f}만 개",
                ha="center", va="center", color="white", fontsize=9.5)
ax.set_ylabel("프레임 시간 (ms)")
ax.set_ylim(0, 17)
ax.set_title("그림자 픽셀이 64배 늘어도 +1.1 ms, 그림자를 끄면 절반 (원문 측정값)", fontsize=11)
fig.tight_layout(); fig.savefig("fig3_shadow_settings.png"); plt.close(fig)
print(8192**2 / 1024**2)
