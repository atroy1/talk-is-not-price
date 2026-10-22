# Pre-registration (fill at the Friday 4 PM lock, G2, then commit)

Claim sentence: We show that ______, measured by ______, under ______, compared with baseline ______.

Predictions, written before any result is looked at:

1. (lead time) ______
2. (quadrant) ______
3. (cross-model) ______

Honest references (decided 2026-10-21): prices = the 10 no-chat `base` runs; chat = 10 new Haiku 5.5 runs with seller chat on and one added sentence in the seller prompt (`seller_prompt_compete.jinja2`):

> Added sentence: ______ (write Friday 4 PM; suggested, neutral wording to avoid the overshoot in arXiv:2603.20281: "Set your ask independently, based on your own costs and what you see in the market.")

Threshold rule: false-alarm rate fixed at 5% on the 10 no-chat runs plus 200 permutation nulls; 1% only if the null set supports it.

Commit with:

```bash
git add notes/preregistration.md && git commit -m "Pre-registration, Fri Oct 23 4 PM ET" && git log -1 --format=%h
```

Paste the hash into the report's grey box: "Pre-registered Fri Oct 23, 4:00 PM ET (commit ______)."
