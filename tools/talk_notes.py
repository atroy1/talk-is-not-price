#!/usr/bin/env python3
"""Transcript -> a cited note. Local model only (task "talk_notes" in config/models.toml).

    python -m tools.talk_notes <slug> [--window 480] [--dry-run] [--speaker "..."] [--title "..."] [--url "..."]

Reads talks/<slug>/transcript.srt, sends ~8-minute windows (30 s overlap) to the local lane, asks for
claims as verbatim quotes with timestamps, checks every quote against the transcript text, and writes
notes/talks/<slug>.md. Quotes that fail the check are kept but flagged; nothing unflagged is invented.
--dry-run writes the prompts to talks/<slug>/prompts/ and makes no call.
"""
import argparse
import json
import re
from datetime import date
from pathlib import Path

from tools.llm import complete, ROOT
from tools.srt_to_md import parse, mmss

SYSTEM = """You read one window of a machine transcript of a research talk about collusion between AI agents.
Return JSON only: {"items":[{"t":"mm:ss","kind":"finding|number|open_problem|method|definition|aside",
"quote":"verbatim words from the transcript, 25 words or fewer","gloss":"one plain sentence on what it means"}]}
Rules: quote only words that appear in the window, never paraphrase inside "quote"; prefer the speaker's own
claims and numbers; include every place the speaker says something is unsolved, future work, or a limitation;
skip pleasantries; 3 to 10 items per window; "t" is the timestamp of the line the quote starts on."""

TEMPLATE = """# {title}

Speaker: {speaker}. Apart Research AI Collusion Research Sprint, {day}. Source: {url}
Recording and transcript: `talks/{slug}/`. Machine transcript; every quote below was string-checked
against it ({ok} of {n} matched verbatim; the rest are marked CHECK and must be heard before use).

## Lines to use (verbatim, with time)

| Time | Kind | Quote | Gloss |
|---|---|---|---|
{rows}

## Open problems the speaker named

{open}

## How it bears on our paper

(Arty writes this. One or two sentences per line that changes Related Work or Discussion. Prefer the paper over the talk when both say it.)

## Citation stubs

In text: ({cite_short}, talk, {year}, mm:ss).
Reference: {speaker} ({year}). *{title}.* Talk at the Apart Research AI Collusion Research Sprint, {day}. {url}
"""


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("’", "'")).strip()


def windows(cues, size, overlap):
    if not cues:
        return
    t0 = cues[0][0]
    end = cues[-1][1]
    while t0 < end:
        chunk = [c for c in cues if c[1] >= t0 and c[0] < t0 + size]
        if chunk:
            yield t0, chunk
        t0 += size - overlap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--window", type=int, default=480); ap.add_argument("--overlap", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--speaker", default="SPEAKER")
    ap.add_argument("--title", default=None); ap.add_argument("--url", default="(Discord recording link)")
    ap.add_argument("--day", default="October 2026")
    a = ap.parse_args()
    tdir = ROOT / "talks" / a.slug
    cues = list(parse((tdir / "transcript.srt").read_text(encoding="utf-8")))
    full = norm(" ".join(c[2] for c in cues))
    items = []
    for i, (t0, chunk) in enumerate(windows(cues, a.window, a.overlap)):
        text = "\n".join(f"[{mmss(s)}] {t}" for s, e, t in chunk)
        user = f"Window {i + 1}, starts {mmss(t0)}.\n\n{text}"
        if a.dry_run:
            p = tdir / "prompts"; p.mkdir(exist_ok=True)
            (p / f"window-{i + 1:02d}.txt").write_text(SYSTEM + "\n\n---\n\n" + user)
            continue
        r = complete("talk_notes", user, system=SYSTEM, note=f"{a.slug} w{i + 1}")
        m = re.search(r"\{.*\}", r.text, re.S)
        try:
            items += json.loads(m.group(0))["items"] if m else []
        except json.JSONDecodeError:
            print(f"window {i + 1}: unparseable reply, skipped")
    if a.dry_run:
        print(f"dry run: prompts in {tdir / 'prompts'}"); return
    seen, rows, ok, opens = set(), [], 0, []
    for it in items:
        q = (it.get("quote") or "").strip()
        if not q or norm(q) in seen:
            continue
        seen.add(norm(q))
        verified = norm(q) in full
        ok += verified
        flag = "" if verified else " **CHECK**"
        rows.append(f"| {it.get('t', '?')} | {it.get('kind', '')} | \"{q}\"{flag} | {it.get('gloss', '')} |")
        if it.get("kind") == "open_problem":
            opens.append(f"- [{it.get('t', '?')}] \"{q}\"{flag}")
    title = a.title or a.slug.replace("-", " ")
    out = ROOT / "notes" / "talks" / f"{a.slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.format(title=title, speaker=a.speaker, day=a.day, url=a.url, slug=a.slug, ok=ok,
                                   n=len(rows), rows="\n".join(rows) or "| | | (none) | |",
                                   open="\n".join(opens) or "(none named)", cite_short=a.speaker.split(" and ")[0].split()[-1],
                                   year=date.today().year))
    print(f"wrote {out.relative_to(ROOT)}: {len(rows)} lines, {ok} verified verbatim")


if __name__ == "__main__":
    main()
