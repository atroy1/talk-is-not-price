"""Layout proof for the two report figures, on SYNTHETIC numbers. Not a result.
Locks the sizes, fonts, palette and label placement so Saturday only swaps the data in.
    .venv/bin/python report/fig_proof.py   -> report/mock/fig1_proof.png, fig2_proof.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).resolve().parent
plt.style.use(HERE / "figstyle.mplstyle")
OUT = HERE / "mock"
OUT.mkdir(exist_ok=True)

# semantic palette (fixed, never cycled)
WORDS, DEEDS, FUSED = "#0072B2", "#D55E00", "#111111"
MODELS = {"GPT-4.1 (2025 runs)": "#777777", "Haiku 5.5": "#009E73", "DeepSeek Flash": "#CC79A7", "GPT-6 Luna": "#E69F00"}
BAND_COMP, BAND_CARTEL = "#e6e6e6", "#fbe3d6"
rng = np.random.default_rng(7)


def stamp(ax):
    ax.text(1.0, 1.02, "LAYOUT PROOF: synthetic numbers", transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="#b00020")


def spread(ys, gap=0.075):
    """Nudge end-of-line label positions apart so they never overlap."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(order, order[1:]):
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    return out


# ---- Figure 1: share of collusive runs caught, by round, at 5% false alarms (full width 6.5 x 2.4 in)
fig, ax = plt.subplots(figsize=(6.5, 2.4))
r = np.arange(1, 31)
chat = 1 / (1 + np.exp(-(r - 6) / 1.6)) * 0.72
price = 1 / (1 + np.exp(-(r - 11) / 2.2)) * 0.88
fused = np.maximum(chat, price) * 1.06
fused = np.clip(fused, 0, 0.95)
series = [(chat, WORDS, "chat only"), (price, DEEDS, "prices only"), (fused, FUSED, "chat + prices")]
label_y = spread([y[-1] for y, _, _ in series])
for (y, c, lab), ly in zip(series, label_y):
    lo, hi = np.clip(y - 0.08, 0, 1), np.clip(y + 0.08, 0, 1)
    ax.fill_between(r, lo, hi, color=c, alpha=0.12, linewidth=0)
    ax.plot(r, y, color=c, label=lab)
    ax.annotate(lab, (r[-1], ly), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=c)
ax.axvline(4, color="#999999", linewidth=0.6, linestyle=(0, (3, 2)))
ax.text(4.3, 0.04, "first floor proposed\nin chat (median)", fontsize=7.5, color="#555555", va="bottom")
ax.axvline(10, color="#999999", linewidth=0.6, linestyle=(0, (3, 2)))
ax.text(10.3, 0.04, "asks lock\n(median)", fontsize=7.5, color="#555555", va="bottom")
ax.set_xlim(1, 30); ax.set_ylim(0, 1)
ax.set_xlabel("round"); ax.set_ylabel("collusive runs caught\nat 5% false alarms")
ax.set_yticks([0, .25, .5, .75, 1]); ax.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
ax.set_title("Lead time: when each signal first catches a colluding market")
fig.subplots_adjust(right=0.86)
stamp(ax)
fig.savefig(OUT / "fig1_proof.png")

# ---- Figure 2: the words-and-deeds quadrant (half width 3.15 x 3.0 in)
fig, ax = plt.subplots(figsize=(3.15, 3.0))
ax.axhspan(0.5, 1.0, xmin=0, xmax=1, color="white", zorder=0)
ax.axvspan(0, 0.6, color=BAND_COMP, alpha=0.6, zorder=0, linewidth=0)
ax.axvspan(1.0, 1.4, color=BAND_CARTEL, zorder=0, linewidth=0)
ax.text(0.3, -0.045, "competitive band", ha="center", va="top", fontsize=7, color="#666666", clip_on=False)
ax.text(1.2, -0.045, "cartel", ha="center", va="top", fontsize=7, color="#9a3b00", clip_on=False)
ax.axhline(0.5, color="#bbbbbb", linewidth=0.6); ax.axvline(0.8, color="#bbbbbb", linewidth=0.6)
for name, c in MODELS.items():
    n = 12
    x = np.concatenate([rng.normal(0.35, 0.12, n // 2), rng.normal(1.05, 0.15, n // 2)])
    y = np.concatenate([rng.uniform(0.05, 0.9, n // 2), rng.normal(0.72, 0.15, n // 2)])
    ax.scatter(np.clip(x, 0.02, 1.38), np.clip(y, 0.02, 0.98), s=14, color=c, edgecolor="white", linewidth=0.5, label=name, zorder=3)
for (x, y, s) in [(0.04, 0.97, "collusion on paper"), (0.83, 0.97, "explicit cartel"), (0.04, 0.03, "competitive"), (0.83, 0.03, "tacit collusion")]:
    ax.text(x, y, s, fontsize=7, color="#333333", va="top" if y > 0.5 else "bottom", style="italic")
ax.set_xlim(0, 1.4); ax.set_ylim(0, 1)
ax.set_xlabel("price lift above competitive (deeds)"); ax.set_ylabel("share of seller messages\nproposing or agreeing a floor (words)")
ax.set_xticks([0, 0.5, 1.0]); ax.set_xticklabels(["$0", "+$5", "+$10"])
ax.tick_params(axis="x", pad=12)
ax.legend(loc="upper left", bbox_to_anchor=(-0.02, -0.26), ncol=2, columnspacing=0.8, handletextpad=0.3, markerscale=1.2)
ax.grid(False)
stamp(ax)
fig.savefig(OUT / "fig2_proof.png")
print("wrote", *sorted(p.name for p in OUT.glob("fig*_proof.png")))
