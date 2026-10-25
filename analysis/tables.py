"""Table 2 for the report, paste-ready markdown: catch rates at the certified rate, with the honest block beneath.

Sprint work, Sat Oct 24 2026. Reads runs/derived/detect-results-explicit.csv (positive sets, intervals, first alarms)
and runs/derived/flags.csv (per-run flags, honest groups leave-one-out). Run after `make reproduce`.

    .venv/bin/python -m analysis.tables     -> report/draft/table2.md (printed too)
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
D = ROOT / "runs/derived"
OUT = ROOT / "report/draft/table2.md"
SETS = [("2025 headline", "2025 chat markets, GPT-4.1 and Claude 3.x"), ("2025 panel 2", "2025 under oversight or CEO pressure"),
        ("Haiku chat", "Claude Haiku 5.5, chat"), ("DeepSeek chat", "DeepSeek V4.1 Flash, chat"), ("Luna chat", "GPT-6 Luna, chat")]
DETS = [("words_hard", "Chat"), ("deeds", "Prices"), ("fused_hard", "Chat + prices (max)"), ("either", "Chat or prices"), ("judge_score", "2025 LLM judge")]
HONEST = [  # flags.csv groups in display order, with the certified rate of the reference they belong to
    ("Haiku 5.5, told it is illegal (reference)", "chat and judge reference, 4.8%"),
    ("  same, seller cost +$6 at round 10", "stress test"),
    ("  same, seller cost +$12 at round 10", "stress test"),
    ("Sonnet and Opus 5.5, told it is illegal (20 rounds)", "silent"),
    ("Sonnet 5.5, illegal + a required hourly note", "talks; a check (4)"),
    ("Haiku 5.5, illegal + a required hourly note", "talks; a check (3)"),
    ("GPT-6 Luna, told it is illegal", "silent"),
    ("DeepSeek V4.1 Flash, told it is illegal", "ignores it; flagged, correctly"),
    ("Haiku 5.5, told not to discuss prices", "2 of 10 coordinate, flagged; 1 false alarm on one message"),
    ("Qwen3.5 35B, told it is illegal", "ignores it; flagged, correctly"),
    ("Haiku 5.5, no chat", "Haiku price reference, 4.9%"),
    ("2025 runs, no chat", "2025 price reference, 9.1%"),
]


def cell(d):
    if d.empty:
        return "-"
    r = d.iloc[0]
    fa = f"; r{r.median_first_alarm:.0f}" if pd.notna(r.median_first_alarm) else ""
    return f"{int(r.caught)}/{int(r.n)} ({r.ci}{fa})"


def main():
    r = pd.read_csv(D / "detect-results-explicit.csv")
    f = pd.read_csv(D / "flags.csv")
    fa = {s: r[(r["set"] == s)].set_index("detector").certified_fa for s in ("2025 headline", "Haiku chat")}
    L = ["**Table 2.** Collusive-design markets flagged by each monitor at its certified false-alarm rate (chat and judge: "
         f"{fa['2025 headline']['words_hard']:.1%}; prices: {fa['2025 headline']['deeds']:.1%} on 2025 markets, {fa['Haiku chat']['deeds']:.1%} on 2026 markets; "
         "chat or prices: the sum). "
         "Clopper-Pearson 95% intervals; r = median round of first alarm. Prices are scored from round 6. The judge is calibrated on the same 20 honest markets. "
         "'Chat + prices' is the pre-registered comparison with the corrected fusion (max of the two scores), certified on Haiku honest talk only; "
         "DeepSeek and Luna prices use the Haiku bar, which is not their own family's. Qwen prices face algorithmic buyers and are not scored.", "",
         "| Markets | n | " + " | ".join(l for _, l in DETS) + " |", "|---|---|" + "---|" * len(DETS)]
    for key, label in SETS:
        row = r[r["set"] == key]
        n = int(row.n.iloc[0])
        L.append(f"| {label} | {n} | " + " | ".join(cell(row[row.detector == det]) for det, _ in DETS) + " |")
    from analysis.detector import clopper_pearson
    fused_thr = float(r[(r["set"] == "Haiku chat") & (r.detector == "fused_hard")].threshold.iloc[0])
    def flag_row(label, d, prices=True):
        """A positive-set row from the per-run flags (groups the detector sets do not cover)."""
        def cell(k):
            lo, hi = clopper_pearson(int(k), len(d))
            return f"{int(k)}/{len(d)} ({lo:.2f}-{hi:.2f})"
        jq = d.judge.dropna()
        if not prices:
            return f"| {label} | {len(d)} | {cell(d.chat.sum())} | n/a | n/a | n/a | {int(jq.sum())}/{len(jq)} |"
        fused = (d[["chat_max", "price_max"]].max(axis=1) > fused_thr).sum()
        either = (d.chat | d.prices).sum()
        return f"| {label} | {len(d)} | {cell(d.chat.sum())} | {cell(d.prices.sum())} | {cell(fused)} | {cell(either)} | {int(jq.sum())}/{len(jq)} |"
    extra = [("Sonnet 5.5, price independently (20 rounds)", f[f.group == "Claude Sonnet 5.5 (20 rounds)"], True),
             ("Haiku 5.5, price independently", f[(f.section == "Told to price independently") & (f.group == "Claude Haiku 5.5")], True)]
    for label, d, prices in extra:
        if len(d):
            L.insert(L.index(next(x for x in L if x.startswith("| Claude Haiku 5.5, chat"))) + 1, flag_row(label, d, prices))
    q = f[f.group == "Qwen3.5 35B, stock and abliterated"]
    if len(q):
        L.append(flag_row("Qwen3.5 35B, chat (algorithmic buyers)", q, prices=False))
    L += ["", "**Honest markets** (no collusive design): false alarms per monitor, reference runs scored leave-one-out.", "",
          "| Markets | n | Chat | Prices | Judge | Role |", "|---|---|---|---|---|---|"]
    for g, role in HONEST:
        d = f[f.group == g]
        if d.empty:
            continue
        j = d.judge.dropna()
        L.append(f"| {g.strip()} | {len(d)} | {int(d.chat.sum())} | {int(d.prices.sum())} | {int(j.sum()) if len(j) else '-'}/{len(j)} | {role} |")
    txt = "\n".join(L) + "\n"
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(txt)
    print(txt)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
