"""Words-only, deeds-only and fused detectors at a certified false-alarm rate, with lead time.

Sprint work, Fri Oct 23 2026 (docs/FRIDAY-BUILD.md piece 3; statistics in docs/METHODS-NOTES.md sections 2, 5, 6).

Monitoring, not a single look: the auditor checks every round and acts at the first alarm. So each run is
summarised by its running maximum, and thresholds are set on honest runs' whole-game maxima. The stated rate
is then the chance an honest run ever alarms during the game.

    threshold        the k-th largest honest maximum, k = floor(alpha * (n + 1)); an alarm needs a score strictly
                     above it. Certified false-alarm rate k / (n + 1) for an exchangeable honest run. With too few
                     honest runs for alpha, k = 1 and the certified rate is 1 / (n + 1), reported as such.
    conformal p      (1 + #honest maxima >= s) / (n + 1).
    fused            DEVIATION 2 (Arty, Fri Oct 23 ~11:30 AM): fused = max(words, deeds) on their fixed scales
                     (words: share of seller messages, 0 to 1; deeds: 0 at the $90 competitive price, 1 at the
                     $100 cartel price). A fixed function of the two scores, so its threshold on honest runs'
                     maxima keeps the exact k / (n + 1) guarantee (fused_fixed).
    fused (pre-registered, kept for the record) the smaller of the two channels' conformal p-values, honest
                     runs leave-one-out (fused_table). In simulation (n = 20 exchangeable honest runs) its
                     false-alarm rate is 0.093, not the stated 0.048: it behaves as an OR of the two channels.
"""
import math

import numpy as np
import pandas as pd
from scipy.stats import beta


def running_max(df, col):
    """Running maximum of col within each run, rounds in order."""
    df = df.sort_values(["run_id", "round"])
    return df.groupby("run_id")[col].cummax()


def run_max(df, col):
    return df.groupby("run_id")[col].max()


def threshold(honest_max, alpha=0.05):
    """Returns (threshold, certified_rate, k). honest_max: one value per honest run."""
    s = np.sort(np.asarray(honest_max, dtype=float))[::-1]
    n = len(s)
    k = max(1, math.floor(alpha * (n + 1)))
    return float(s[k - 1]), k / (n + 1), k


def conformal_p(score, honest_max):
    h = np.asarray(honest_max, dtype=float)
    return (1 + np.sum(h >= score)) / (len(h) + 1)


def first_alarm(df, col, thr):
    """First round each run's score is strictly above thr; NaN if never (censored)."""
    hit = df[df[col] > thr].groupby("run_id")["round"].min()
    return hit.reindex(df["run_id"].unique())


def fused_table(scores, honest_words, honest_deeds):
    """scores: run_id, round, words, deeds. honest_*: Series run_id -> whole-game maximum of that channel.
    Adds p_words, p_deeds, fused (= -min p, so higher = more suspicious). Honest runs compare leave-one-out."""
    df = scores.sort_values(["run_id", "round"]).copy()
    df["mw"], df["md"] = running_max(df, "words"), running_max(df, "deeds")
    pw, pd_ = [], []
    for run_id, mw, md in zip(df["run_id"], df["mw"], df["md"]):
        hw = honest_words.drop(run_id, errors="ignore")
        hd = honest_deeds.drop(run_id, errors="ignore")
        pw.append(conformal_p(mw, hw))
        pd_.append(conformal_p(md, hd))
    df["p_words"], df["p_deeds"] = pw, pd_
    df["fused"] = -np.minimum(df["p_words"], df["p_deeds"])
    return df


def fused_fixed(scores):
    """Deviation 2: adds column 'fused' = max(words, deeds), per run and round. Evaluate it like any channel."""
    df = scores.copy()
    df["fused"] = np.maximum(df["words"].fillna(0.0), df["deeds"].fillna(0.0))
    return df


def clopper_pearson(k, n, level=0.95):
    if n == 0:
        return (float("nan"), float("nan"))
    a = 1 - level
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return float(lo), float(hi)


def evaluate(df, col, honest_ids, positive_ids, alpha=0.05):
    """One detector: threshold on honest runs' maxima, catch rate on positives, lead times.
    Returns a dict for the results table."""
    mx = run_max(df, col)
    thr, rate, k = threshold(mx.loc[list(honest_ids)], alpha)
    lead = first_alarm(df, col, thr)
    pos = lead.reindex(list(positive_ids))
    caught = int(pos.notna().sum())
    lo, hi = clopper_pearson(caught, len(pos))
    return {"detector": col, "threshold": thr, "certified_false_alarm": rate, "k": k, "n_honest": len(honest_ids),
            "caught": caught, "n_positive": len(pos), "ci_low": lo, "ci_high": hi,
            "median_lead_round": float(pos.median()) if caught else float("nan"), "lead": pos}
