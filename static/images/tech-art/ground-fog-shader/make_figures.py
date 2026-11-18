"""
Ground fog shader article figures
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

BG  = '#1a1a2e'
PAN = '#16213e'
W   = 'white'
FOG_COLOR = (0.55, 0.72, 0.9)

plt.rcParams.update({'font.family': 'sans-serif', 'font.size': 10})

# ── Figure 1: 단면도 — 높이별 안개 밀도 ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
fig.patch.set_facecolor(BG)

FOG_TOP = 6.0
FALL    = 2.0   # e-folding height

# 1a: density curve
ax = axes[0]
ax.set_facecolor(PAN)
h = np.linspace(0, FOG_TOP * 1.4, 300)
density = np.where(h <= FOG_TOP, np.exp(-h / FALL), 0.0)

ax.fill_betweenx(h, 0, density, alpha=0.35, color=FOG_COLOR)
ax.plot(density, h, color='#90caf9', lw=2.2)
ax.axhline(FOG_TOP, color='#ff7043', ls='--', lw=1.5, alpha=0.9, label='fog top')
ax.axhline(0,       color='#8d6e63', lw=2.0, label='지면 (y=0)')
ax.set_xlim(-0.05, 1.1)
ax.set_ylim(-0.5, FOG_TOP * 1.4 + 0.5)
ax.set_xlabel('안개 밀도 (0=없음, 1=최대)', color=W)
ax.set_ylabel('높이 (world Y)', color=W)
ax.set_title('높이와 안개 밀도 관계', color=W, pad=8)
ax.tick_params(colors=W)
for sp in ('top','right'): ax.spines[sp].set_visible(False)
for sp in ('bottom','left'): ax.spines[sp].set_color('#555577')
ax.legend(facecolor='#0d0d22', labelcolor=W, framealpha=0.8, fontsize=9)

# 1b: cross-section view
ax2 = axes[1]
ax2.set_facecolor('#0a0a18')
xs = np.linspace(-8, 8, 240)
ys = np.linspace(-0.5, 9, 180)
X, Y = np.meshgrid(xs, ys)
fog_grid = np.where(Y <= FOG_TOP, np.exp(-Y / FALL), 0.0)
fog_grid = np.where(Y < 0, 0.0, fog_grid)

fog_cmap = LinearSegmentedColormap.from_list(
    'fog_blue', [(0,0,0,0), (*FOG_COLOR, 0.85)], N=256)
ax2.pcolormesh(X, Y, fog_grid, cmap=fog_cmap, shading='gouraud',
               vmin=0, vmax=1.0)

# ground
ax2.fill_between([-8,8], -0.5, 0, color='#3e2723', zorder=3)
ax2.plot([-8,8], [0,0], color='#8d6e63', lw=1.5, zorder=4)
# fog top line
ax2.axhline(FOG_TOP, color='#ff7043', ls='--', lw=1.2, alpha=0.7, zorder=5)
ax2.text(5.5, FOG_TOP + 0.2, 'fog top', color='#ff7043', fontsize=8)

# camera icon (simple triangle = view cone)
cam_y = 7.5
ax2.annotate('', xy=(-3, 0.3), xytext=(0, cam_y),
             arrowprops=dict(arrowstyle='->', color='#ffee58', lw=1.0))
ax2.annotate('', xy=(3,  0.3), xytext=(0, cam_y),
             arrowprops=dict(arrowstyle='->', color='#ffee58', lw=1.0))
ax2.plot(0, cam_y, 's', color='#ffee58', ms=7, label='카메라', zorder=6)

ax2.set_xlim(-8, 8)
ax2.set_ylim(-0.5, 9)
ax2.set_xlabel('수평 거리', color=W)
ax2.set_ylabel('높이', color=W)
ax2.set_title('단면도: 카메라에서 본 지면 안개', color=W, pad=8)
ax2.tick_params(colors=W)
for sp in ('top','right'): ax2.spines[sp].set_visible(False)
for sp in ('bottom','left'): ax2.spines[sp].set_color('#555577')
ax2.legend(facecolor='#0d0d22', labelcolor=W, framealpha=0.8, fontsize=9)

plt.tight_layout(pad=1.5)
plt.savefig('fig1_height_density.png', dpi=150, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("fig1 done")

# ── Figure 2: FBM 옥타브 쌓기 ──────────────────────────────────────────────
def wave(x, freq, phase, seed):
    rng = np.random.RandomState(seed)
    harmonics = rng.uniform(0.7, 1.3, 5)
    ph = rng.uniform(0, np.pi, 5)
    r = sum(h * np.sin(freq * (1 + 0.3*i) * x + phase + ph[i])
            for i, h in enumerate(harmonics))
    return r / abs(r).max()

x = np.linspace(0, 10, 600)
fig, axes = plt.subplots(5, 1, figsize=(12, 7), sharex=True)
fig.patch.set_facecolor(BG)

COLORS = ['#ef9a9a','#ffcc80','#a5d6a7','#90caf9','#ffffff']
combined = np.zeros_like(x)

for i in range(4):
    ax = axes[i]
    ax.set_facecolor(PAN)
    amp  = 0.5 ** i
    freq = 2.0 ** i
    sig  = amp * wave(x, freq, i * 0.9, seed=i * 7 + 3)
    combined += sig
    ax.plot(x, sig, color=COLORS[i], lw=1.5)
    ax.axhline(0, color=W, alpha=0.15, lw=0.6)
    ax.set_yticks([])
    ax.set_ylabel(f'oct {i+1}\nf×{int(freq)} a×{amp:.2f}', color=W,
                  fontsize=8, rotation=0, ha='right', va='center', labelpad=55)
    for sp in ('top','right','bottom','left'):
        ax.spines[sp].set_color('#333355')

axes[4].set_facecolor(PAN)
axes[4].plot(x, combined, color=COLORS[4], lw=2.0)
axes[4].axhline(0, color=W, alpha=0.15, lw=0.6)
axes[4].set_yticks([])
axes[4].set_ylabel('합산 FBM\n(4 oct)', color=W,
                   fontsize=8, rotation=0, ha='right', va='center', labelpad=55)
axes[4].set_xlabel('XZ 위치 →', color=W)
for sp in ('top','right','bottom','left'):
    axes[4].spines[sp].set_color('#333355')

fig.suptitle(
    'FBM(Fractional Brownian Motion): 옥타브를 쌓아 자연스러운 안개 패턴 만들기',
    color=W, fontsize=11, y=1.01)
plt.tight_layout(pad=1.0)
plt.savefig('fig2_fbm_octaves.png', dpi=150, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("fig2 done")

# ── Figure 3: 안개 방식 3종 비교 ───────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
fig.patch.set_facecolor(BG)

xs = np.linspace(0, 10, 220)
ys = np.linspace(0, 8,  180)
X, Y = np.meshgrid(xs, ys)
dist = np.sqrt((X - 0)**2 + Y**2)   # distance from left edge camera

sky_cmap = LinearSegmentedColormap.from_list(
    'sky', [(0.05,0.05,0.15), (0.15,0.25,0.5)], N=64)
fog_cmap = LinearSegmentedColormap.from_list(
    'fog', [(0,0,0,0), (*FOG_COLOR, 0.85)], N=256)

CONFIGS = [
    ('① 균일 안개\n(Uniform Fog)',
     lambda X,Y: np.clip(1.0 - np.exp(-dist * 0.12), 0, 1)),
    ('② 높이 안개\n(Height Fog)',
     lambda X,Y: np.where(Y <= FOG_TOP, np.exp(-Y / FALL), 0.0)),
    ('③ 높이 + FBM 노이즈\n(Height + FBM)',
     lambda X,Y: (np.where(Y <= FOG_TOP, np.exp(-Y / FALL), 0.0)
                  * np.clip(0.9 + 0.2*(
                      np.sin(X*0.9)*np.cos(Y*1.4)*0.6
                    + np.sin(X*1.8+1)*np.cos(Y*2.5)*0.3
                    + np.sin(X*3.6+2)*0.1), 0.3, 1.3))),
]

for ax, (title, fn) in zip(axes, CONFIGS):
    ax.set_facecolor('#080816')
    # sky
    ax.pcolormesh(X, Y, Y/8, cmap=sky_cmap, shading='gouraud', vmin=0, vmax=1)
    # ground detail
    ax.fill_between([0,10], 0, 0.4, color='#2e1f14')
    ax.fill_between([0,10], 0.4, 0.5, color='#3e2723')
    # fog
    fog = np.clip(fn(X, Y), 0, 1)
    fog[Y < 0] = 0
    ax.pcolormesh(X, Y, fog, cmap=fog_cmap, shading='gouraud', vmin=0, vmax=1)
    ax.set_title(title, color=W, fontsize=10, pad=6)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color('#333355')

plt.tight_layout(pad=1.2)
plt.savefig('fig3_fog_types.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("fig3 done")
print("All figures complete!")
