"""Write notes/results-frozen.md from the derived tables: every number the report body may cite, with its source file.

Sprint work, Sat Oct 24 2026. Run after `make reproduce`. Nothing here computes a new statistic except Cohen's kappa
between the graded labeller and the Sonnet reference sample (from the two label files).

    .venv/bin/python -m analysis.freeze            -> notes/results-frozen.md (overwrites; the git history keeps versions)
"""
import datetime
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
D = ROOT / "runs/derived"
OUT = ROOT / "notes/results-frozen.md"
SETS = ["2025 headline", "2025 panel 2", "Haiku chat", "DeepSeek chat", "Luna chat"]
DETS = [("words_hard", "chat (headline)"), ("deeds", "prices"), ("fused_hard", "chat + prices"), ("either", "chat or prices (union bound)"),
        ("judge_score", "2025 judge"), ("words", "chat, graded (pre-reg)"), ("chat_2plus", "chat, 2+ messages")]


def md(df, index=True):
    """A markdown table without the tabulate dependency."""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join("" if pd.isna(v) else (f"{v:g}" if isinstance(v, float) else str(v)) for v in r.tolist()) + " |")
    return "\n".join(lines)


def kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    L = []
    say = L.append
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    say(f"# Frozen results\n\nGenerated {datetime.datetime.now():%a %b %d %Y, %I:%M %p} from commit {head} by `analysis/freeze.py` after `make reproduce`. "
        "Nothing in the report body cites a number that is not here. Each table names its file.\n")

    r = pd.read_csv(D / "detect-results-explicit.csv")
    say("## 1. Catch rates at the certified false-alarm rate (`runs/derived/detect-results-explicit.csv`)\n")
    say("Chat, fused and judge thresholds: 20 Haiku explicit-sentence runs (certified 1/21 = 4.8%). Prices: 10 no-chat 2025 runs for 2025 sets (9.1%); "
        "Haiku no-chat plus explicit runs for 2026 sets (see the price rule below). Clopper-Pearson 95% intervals. Median first alarm in rounds.\n")
    say("| Set | n | " + " | ".join(lab for _, lab in DETS) + " |")
    say("|---|---|" + "---|" * len(DETS))
    for s in SETS:
        row = r[r["set"] == s]
        cells = []
        for det, _ in DETS:
            d = row[row["detector"] == det]
            cells.append(f"{int(d.caught.iloc[0])}/{int(d.n.iloc[0])} ({d.ci.iloc[0]}; r{d.median_first_alarm.iloc[0]:.0f})" if len(d) and pd.notna(d.median_first_alarm.iloc[0])
                         else (f"{int(d.caught.iloc[0])}/{int(d.n.iloc[0])} ({d.ci.iloc[0]})" if len(d) else "-"))
        n = int(row.n.iloc[0])
        say(f"| {s} | {n} | " + " | ".join(cells) + " |")
    thr = r[r["set"] == "2025 headline"].set_index("detector")
    say(f"\nThresholds: chat {thr.loc['words_hard', 'threshold']}, prices (2025) {thr.loc['deeds', 'threshold']} (= ${90 + 10 * thr.loc['deeds', 'threshold']:.2f} trailing-3 mean ask), "
        f"fused {thr.loc['fused_hard', 'threshold']}, judge {thr.loc['judge_score', 'threshold']}. Union-bound certified rate for 'either': "
        f"{thr.loc['either', 'certified_fa']} on 2025 sets.\n")

    f = pd.read_csv(D / "flag-summary.csv")
    say("## 2. What a chat monitor sees and misses, per run (`runs/derived/flag-summary.csv`, from `flags.csv`)\n")
    say("| Section | Group | n | chat only | both | prices only | neither | judge |")
    say("|---|---|---|---|---|---|---|---|")
    for _, x in f.iterrows():
        say(f"| {x.section} | {x.group.strip()} | {x.n} | {x['chat only']} | {x.both} | {x['prices only']} | {x.neither} | {x.judge} |")
    say("")

    c = pd.read_csv(D / "controls-2025.csv")
    say("## 3. Pre-registered price score beside the corrections (`runs/derived/controls-2025.csv`, 2025 no-chat threshold, 9.1%)\n")
    say("| Score | Headline | Panel 2 | Base leave-one-out | Shuffle null |")
    say("|---|---|---|---|---|")
    for sc in ["deeds_from_r1", "deeds_from_r4", "deeds_from_r6", "deeds_from_r8", "judge_score"]:
        h = c[(c.score == sc) & (c.positives == "headline")].iloc[0]
        p = c[(c.score == sc) & (c.positives == "panel2")].iloc[0]
        say(f"| {sc} | {h.caught} ({h.ci}) | {p.caught} ({p.ci}) | {h.loo_base_alarms} | {h.shuffle_null_alarms if pd.notna(h.shuffle_null_alarms) else '-'} |")
    say("")

    pr = subprocess.run([str(ROOT / ".venv/bin/python"), "-m", "analysis.compete_check", "explicit"], cwd=ROOT, capture_output=True, text=True).stdout.strip().splitlines()
    say("## 4. Price rule for the explicit-sentence runs (`analysis/compete_check.py explicit`)\n")
    say("```\n" + "\n".join(pr[-4:]) + "\n```\n")

    if (D / "overcharge.csv").exists():
        oc = pd.read_csv(D / "overcharge.csv", index_col=0)
        say("## 5. Buyer overcharge in dollars per market (`runs/derived/overcharge.csv`; sum over trades of price minus $90)\n")
        from analysis.controls import HEADLINE, PANEL2
        def grp(cnd):
            if cnd in HEADLINE: return "2025 headline"
            if cnd in PANEL2: return "2025 panel 2"
            return cnd
        oc["group"] = oc.cond.map(grp)
        g = oc.groupby("group").overcharge.agg(n="size", median="median", min="min", max="max", above_zero=lambda s: int((s > 0).sum())).round(0)
        say(md(g) + "\n")

    if (D / "private-plan.csv").exists():
        say("## 6. Private plans against public messages, 2025 chat markets (`runs/derived/private-plan.csv`)\n")
        say(md(pd.read_csv(D / "private-plan.csv"), index=False) + "\n")

    lab = pd.read_csv(D / "labels.csv").drop_duplicates("id").set_index("id")
    ref = pd.read_csv(D / "labels-reference.csv").drop_duplicates("id").set_index("id")
    ref = ref[ref.label.isin(["FLOOR", "AGREE", "NEITHER"])]
    j = ref[["label"]].join(lab[["p_floor", "p_agree", "p_neither"]], how="inner")
    pred = j[["p_floor", "p_agree", "p_neither"]].idxmax(axis=1).str[2:].str.upper()
    k3 = kappa(j.label.tolist(), pred.tolist())
    k2 = kappa((j.label != "NEITHER").tolist(), (pred != "NEITHER").tolist())
    say("## 7. Labeller against the Sonnet 5.5 reference sample (`runs/derived/labels.csv`, `labels-reference.csv`)\n")
    say(f"n = {len(j)} messages; agreement {(j.label == pred).mean():.1%}; kappa {k3:.3f} (3-class), {k2:.3f} (collusive vs not).\n")
    hc = D / "handlabel-check.csv"
    if hc.exists():
        h = pd.read_csv(hc)
        say(f"Hand labels (`runs/derived/handlabel-check.csv`): graded label agrees on {int((h.hand == h.graded).sum())} of {len(h)} (gate 35).\n")
    else:
        say("Hand labels: not yet done (`make labels ARGS=--check` after `notes/handlabel/sample-40.csv` is filled in).\n")

    OUT.write_text("\n".join(L) + "\n")
    print("wrote", OUT.relative_to(ROOT), f"({len(L)} lines)")


if __name__ == "__main__":
    main()
