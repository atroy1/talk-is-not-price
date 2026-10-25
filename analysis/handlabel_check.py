"""The 40-message check without a human: two blind Claude readers, a reconciled consensus, and the labeller against each.

Sprint work, Sat Oct 24 2026. Replaces an in-session script that keyed its output on a pandas attribute by mistake
(`row.item` is a method, not the column); every column here is accessed by name. Reads
  notes/handlabel/sample-40.csv            the texts (author's label column left empty)
  notes/handlabel/sample-40-claude.csv     pass 1, Claude Fable 5.1 in the analysis session, blind
  notes/handlabel/sample-40-pass2.csv      pass 2, a Sonnet 5.5 agent given only the definitions and the file
  notes/handlabel/reconciliation.csv       the items where the passes differ, each resolved on the full text with a reason
and labels the 40 texts with the graded labeller (40 API calls, about $0.0003).

    .venv/bin/python -m analysis.handlabel_check   -> runs/derived/handlabel-three-way.csv, handlabel-consensus-check.csv
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.labels import CLASSES, label_graded  # noqa: E402

H = ROOT / "notes/handlabel"
D = ROOT / "runs/derived"


def kappa(x, y):
    x, y = list(x), list(y)
    n = len(x)
    po = sum(i == j for i, j in zip(x, y)) / n
    cats = set(x) | set(y)
    pe = sum((x.count(c) / n) * (y.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    base = pd.read_csv(H / "sample-40.csv")[["item", "text"]]
    p1 = pd.read_csv(H / "sample-40-claude.csv")[["item", "label"]].rename(columns={"label": "pass1"})
    p2 = pd.read_csv(H / "sample-40-pass2.csv")[["item", "label"]].rename(columns={"label": "pass2"})
    rec = pd.read_csv(H / "reconciliation.csv")[["item", "final"]]
    df = base.merge(p1, on="item").merge(p2, on="item").merge(rec, on="item", how="left")
    for c in ("pass1", "pass2", "final"):
        df[c] = df[c].str.upper()
    df["consensus"] = df["final"].where(df["final"].notna(), df["pass1"])
    assert ((df.pass1 == df.pass2) | df["final"].notna()).all(), "a disagreement is not reconciled"
    rows = []
    for text in df["text"]:
        p = label_graded(text)
        rows.append({"labeller": max(CLASSES, key=lambda c: p["p_" + c.lower()]), "p_coll": round(p["p_floor"] + p["p_agree"], 3)})
    df = pd.concat([df, pd.DataFrame(rows)], axis=1)
    df.to_csv(D / "handlabel-three-way.csv", index=False)
    b = lambda s: s != "NEITHER"
    out = []
    for a, c in (("pass1", "pass2"), ("labeller", "pass1"), ("labeller", "pass2"), ("labeller", "consensus")):
        out.append({"pair": f"{a} vs {c}", "three_class": int((df[a] == df[c]).sum()), "kappa3": round(kappa(df[a], df[c]), 3),
                    "collusive_or_not": int((b(df[a]) == b(df[c])).sum()), "kappa2": round(kappa(b(df[a]), b(df[c])), 3)})
    summ = pd.DataFrame(out)
    summ.to_csv(D / "handlabel-consensus-check.csv", index=False)
    print(summ.to_string(index=False))
    print("reconciled items:", df[df["final"].notna()][["item", "pass1", "pass2", "consensus", "labeller"]].to_string(index=False))
    print("consensus vs labeller misses:", df[df.consensus != df.labeller][["item", "consensus", "labeller", "p_coll"]].to_string(index=False))


if __name__ == "__main__":
    main()
