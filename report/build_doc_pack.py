"""The Google Doc fallback: split the draft into paste-ready pieces, one file per section, plus captions and figures.

Sprint work, Sat Oct 24 2026 night. If the official Google Doc is used instead of the typeset PDF, each file here is
pasted with Command-Shift-V under the template's own heading. Tables come as tab-separated rows for Table > Convert.

    .venv/bin/python report/build_doc_pack.py   -> report/final/doc-paste/
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT = ROOT / "report/draft/report-draft.md"
OUT = ROOT / "report/final/doc-paste"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    md = DRAFT.read_text()
    body = md[md.index("## Abstract"):]
    parts = re.split(r"\n(?=## )", body)
    for i, part in enumerate(parts):
        head = part.split("\n", 1)[0].lstrip("# ").strip()
        slug = re.sub(r"[^a-z0-9]+", "-", head.lower()).strip("-")[:40]
        text = part.split("\n", 1)[1] if "\n" in part else ""
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # the Doc keeps bold badly on paste; re-bold by hand
        (OUT / f"{i:02d}-{slug}.txt").write_text(text.strip() + "\n")
    t2 = (ROOT / "report/draft/table2.md").read_text()
    rows = [r for r in t2.split("\n") if r.startswith("|") and not set(r) <= set("|-: ")]
    (OUT / "table2.tsv").write_text("\n".join("\t".join(c.strip() for c in r.strip("|").split("|")) for r in rows) + "\n")
    figs = ROOT / "report/final/figures"
    if figs.exists():
        for f in figs.glob("*.png"):
            shutil.copy(f, OUT / f.name)
    from report.build_final import CAPTIONS, APPENDIX_FIGS  # noqa: E402
    cap = ["Figure captions (paste under each figure):", ""]
    for n, (path, _, c) in CAPTIONS.items():
        cap.append(f"Figure {n} ({path}). {c.replace(chr(92) + '$', '$')}")
    for lab, (path, _, c) in APPENDIX_FIGS.items():
        cap.append(f"Figure {lab} ({path}). {c.replace(chr(92) + '$', '$')}")
    (OUT / "captions.txt").write_text("\n\n".join(cap) + "\n")
    print("wrote", OUT.relative_to(ROOT), ":", len(list(OUT.iterdir())), "files")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    main()
