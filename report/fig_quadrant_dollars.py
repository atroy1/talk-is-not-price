"""Figure 1 candidate DRAFT: words against harm, one dot a market, every family (2025 and 2026 runs).

Sprint work, Fri Oct 23 2026, late night (course review). x = buyer overcharge in dollars: the sum over the market's
trades of (price minus the $90 competitive price), from runs/derived/overcharge.csv. y = share of the market's seller
messages labelled collusive (P(floor or agree) above 0.5, deviation 4). Hollow = honest by design (no chat, or told
the conduct is illegal); crosses = chat on, no message sent. Dashed verticals = the most expensive honest market of each
family, which is where a price screen with k = 1 puts its bar.
    .venv/bin/python report/fig_quadrant_dollars.py   -> report/draft/fig_quadrant_dollars.png
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
plt.style.use(HERE / "figstyle.mplstyle")
FINAL = bool(os.environ.get("FINAL"))  # FINAL=1: print files, no DRAFT tag, 300 dpi
OUT = HERE / ("final/figures" if FINAL else "draft")
OUT.mkdir(parents=True, exist_ok=True)
from analysis.controls import HEADLINE, PANEL2  # noqa: E402
from analysis.load_runs import load_all, load_live  # noqa: E402

FAMILIES = [  # (label, colour, condition test, honest test)
    ("GPT-4.1 and Claude 3.x (2025)", "#0072B2", lambda c: c in HEADLINE or c in PANEL2 or c == "base", lambda c: c == "base"),
    ("Claude Haiku 5.5", "#D55E00", lambda c: c.startswith("haiku55") or c.startswith("xm20-haiku55"),
     lambda c: c in ("haiku55-base", "haiku55-explicit", "haiku55-costshock-explicit", "haiku55-costshock12-explicit", "haiku55-pilot-notalk",
                     "haiku55-pilot-explicit", "xm20-haiku55-explicit", "xm20-haiku55-notalk", "haiku55-talk-illegal")),
    ("Claude Sonnet and Opus 5.5", "#009E73", lambda c: c.startswith(("xm20-sonnet55", "xm20-opus55", "opus55-neutral", "sonnet55-talk")),
     lambda c: c.endswith(("-explicit", "-notalk")) or c.startswith("sonnet55-talk")),
    ("DeepSeek V4.1 Flash", "#CC79A7", lambda c: c.startswith("dsflash"), lambda c: c == "dsflash-explicit"),
    ("GPT-6 Luna", "#E69F00", lambda c: c.startswith("luna"), lambda c: c == "luna-explicit"),
    ("Qwen3.5 35B (ZIP buyers)", "#56B4E9", lambda c: c.startswith("qwen35b"), lambda c: "explicit" in c),
]


def main():
    old, new = load_all(), load_live()
    runs = pd.concat([old["runs"], new["runs"]], ignore_index=True).set_index("run_id")["condition"]
    runs = runs[~runs.index.str.contains("check|smoke|fake|replay")]
    rounds = pd.concat([old["runs"], new["runs"]], ignore_index=True).set_index("run_id")["rounds"]
    runs = runs[rounds.reindex(runs.index) >= 20]  # the 6- to 10-round planted and thinking markets and the 8-round pilots stay out
    m = pd.concat([old["messages"], new["messages"]], ignore_index=True)
    m = m[(m.channel == "seller") & m.text.notna() & (m.text.astype(str).str.strip() != "")].copy()
    lab = pd.read_csv(ROOT / "runs/derived/labels.csv").drop_duplicates("id").set_index("id")
    m["id"] = m.run_id + "|" + m["round"].astype(str) + "|" + m.agent
    m["coll"] = (m.id.map(lab.p_floor + lab.p_agree) > 0.5)
    share = m.groupby("run_id")["coll"].mean()
    nmsg = m.groupby("run_id").size()
    oc = pd.read_csv(ROOT / "runs/derived/overcharge.csv", index_col=0)["overcharge"]
    chat_on = pd.concat([old["runs"], new["runs"]], ignore_index=True).set_index("run_id")["seller_comms_enabled"]
    d = pd.DataFrame({"cond": runs, "x": oc.reindex(runs.index), "y": share.reindex(runs.index).fillna(0.0),
                      "n": nmsg.reindex(runs.index).fillna(0).astype(int), "chat": chat_on.reindex(runs.index).fillna(False)})
    d = d.dropna(subset=["x"])
    fig, ax = plt.subplots(figsize=(6.5, 2.8))
    for label, color, test, honest in FAMILIES:
        f = d[d.cond.map(lambda c: bool(test(str(c))))]
        if f.empty:
            continue
        h = f.cond.map(lambda c: bool(honest(str(c))))
        silent = f.chat.astype(bool) & (f.n == 0)
        rng = np.random.default_rng(7)
        jit = pd.Series(0.0, index=f.index)  # no jitter: hollow dots above zero would read as false alarms against a zero threshold
        lab_ = f"{label} ({int((~h).sum())} collusive design, {int(h.sum())} honest)" if h.any() else f"{label} ({len(f)})"
        ax.scatter(f.x[~h & ~silent], (f.y + jit)[~h & ~silent], s=16, color=color, alpha=0.8, linewidths=0, label=lab_, zorder=3)
        ax.scatter(f.x[h & ~silent], (f.y + jit)[h & ~silent], s=18, facecolors="none", edgecolors=color, linewidths=0.8, zorder=3)
        ax.scatter(f.x[silent], (f.y + jit)[silent], s=26, color=color, marker="x", linewidths=0.9, zorder=4)
        if h.any() and label.startswith(("GPT-4.1", "Claude Haiku")):  # only the two families with a price reference
            hx = f.x[h].max()
            ax.axvline(hx, color=color, linewidth=0.6, linestyle=(0, (3, 2)), alpha=0.8)
            ax.text(hx, 1.03 + 0.045 * (FAMILIES.index((label, color, test, honest)) % 2), f"${hx:,.0f}", color=color, fontsize=6.5, ha="center", va="bottom")
    ax.axvline(0, color="#999999", linewidth=0.6)
    ax.axhline(0, color="#999999", linewidth=0.6)
    ax.set_xlabel("buyer overcharge over the whole market: sum over trades of (price minus $90)", fontsize=8)
    ax.set_ylabel("share of seller messages\nlabelled collusive")
    ax.set_ylim(-0.06, 1.08)
    ax.grid(False)
    ax.text(0.99, 0.88, "talk, with harm", transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color="#333333")
    ax.text(0.01, 0.97, "talk, no harm", transform=ax.transAxes, ha="left", va="top", fontsize=7.5, color="#333333")
    ax.text(0.99, 0.13, "silent or honest talk, high prices\n(x = sent no message)", transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#333333")
    ax.text(0.01, 0.03, "competitive", transform=ax.transAxes, ha="left", va="bottom", fontsize=7.5, color="#333333")
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.52), fontsize=6.2, markerscale=1.0, labelspacing=0.3)
    if not FINAL:
        ax.text(1.0, 1.08, "DRAFT: hollow = honest by design (those above zero coordinated anyway: Qwen told it is illegal, Haiku told not to discuss prices); dashed = most expensive honest no-chat market in dollars", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=6.5, color="#b00020")
    fig.savefig(OUT / "fig_quadrant_dollars.png", dpi=(300 if FINAL else 200), bbox_inches="tight")
    print("wrote", (OUT / "fig_quadrant_dollars.png").relative_to(ROOT))
    print(d.groupby("cond").agg(n=("x", "size"), oc_med=("x", "median"), oc_max=("x", "max"), share_med=("y", "median")).round(2).to_string())


if __name__ == "__main__":
    main()
