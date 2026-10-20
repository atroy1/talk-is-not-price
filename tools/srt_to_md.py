#!/usr/bin/env python3
"""SRT -> readable Markdown with a [mm:ss] mark at the start of each paragraph.
Paragraphs break every ~60 s of speech or at a silence longer than 2 s.
    python tools/srt_to_md.py talks/<slug>/transcript.srt <slug> > transcript.md
"""
import re
import sys
from datetime import date

CUE = re.compile(r"(\d+)\s+(\d\d):(\d\d):(\d\d)[,.](\d{3}) --> (\d\d):(\d\d):(\d\d)[,.](\d{3})\s+(.*?)(?=\n\n|\Z)", re.S)


def parse(text):
    for m in CUE.finditer(text):
        g = m.groups()
        start = int(g[1]) * 3600 + int(g[2]) * 60 + int(g[3]) + int(g[4]) / 1000
        end = int(g[5]) * 3600 + int(g[6]) * 60 + int(g[7]) + int(g[8]) / 1000
        yield start, end, " ".join(g[9].split())


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    path, slug = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "talk"
    cues = list(parse(open(path, encoding="utf-8").read()))
    print(f"# Transcript: {slug}\n")
    print(f"Machine transcript ({date.today()}), unedited. Timestamps are approximate to a few seconds. "
          f"Check any quote against the audio before it goes in the report.\n")
    para, p_start, last_end = [], None, None
    for start, end, text in cues:
        if para and (start - p_start > 60 or start - last_end > 2):
            print(f"**[{mmss(p_start)}]** " + " ".join(para) + "\n")
            para, p_start = [], None
        if p_start is None:
            p_start = start
        para.append(text)
        last_end = end
    if para:
        print(f"**[{mmss(p_start)}]** " + " ".join(para) + "\n")


if __name__ == "__main__":
    main()
