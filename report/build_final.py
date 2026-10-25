"""Build the submission: report/draft/report-draft.md -> report/final/report.typ, in the official template's form.

Sprint work, Sat Oct 24 2026 night. The draft is Markdown (Arty's edits live there); this converts it deterministically
so the final session rebuilds after every change instead of hand-editing Typst. Geometry and type come from the
template replica (report/mock/report.typ): US Letter, 1 in margins, Old Standard TT 11 pt, 14 pt numbered headings.

    .venv/bin/python report/build_final.py            -> report/final/report.typ
    typst compile --font-path report/fonts report/final/report.typ report/final/report.pdf

What it does: title block and footnote 1; the abstract inset; "## N. Title" -> numbered level-1 headings, "### N.N Title"
-> level 2; "## Code and data" and the rest unnumbered; the **Pre-registration.** paragraph becomes the grey box; figures
are placed after the first paragraph that cites them (captions below, in CAPTIONS); Table 1 is built from
runs/derived/detect-results-explicit.csv and Table 2 from report/draft/table2.md; the appendix is reordered so that
"Limitations and Dual-Use / Ethical Considerations" is Appendix A and the LLM Usage Statement Appendix B; square-bracket
notes to Arty are rendered as orange marks so none survives unseen; dollars and underscores are escaped for Typst.
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DRAFT = ROOT / "report/draft/report-draft.md"
OUT = ROOT / "report/final/report.typ"
FIG = "figures"  # relative to report/final

CAPTIONS = {  # numbered in order of first citation: 1 dollars (Introduction), 2 instruction grid (4.1), 3 gag (4.3)
    1: ("fig_quadrant_dollars.png", "100%",
        "Each dot is one market. Horizontal: what buyers paid above the \\$90 competitive price over the whole market, in dollars (sum over trades). "
        "Vertical: share of the sellers' messages labelled collusive. Hollow dots are honest by design (no channel, or told the conduct is illegal); "
        "those above zero are the markets meant to be honest whose sellers coordinated anyway (Qwen told it is illegal, Haiku told not to discuss prices); "
        "crosses sent no message. Dashed lines mark the most expensive honest no-chat market of the two families with a price reference: for GPT-4.1 that "
        "honest market (\\$632) cost buyers more than any cartel. The chat monitor fires on every dot above zero; 16 of the 35 2025 cartels it flags sit left of zero."),
    2: ("fig2_instructions.png", "90%",
        "What the instruction sentences do, by seller model. Bars: share of messages labelled collusive. Dots: mean ask from round 6 (top axis, dollars); grey numbers: markets. "
        "\"Set your ask independently\" leaves coordination talk intact; adding \"coordinating prices is illegal\" ends Haiku's talk at no-chat prices, silences Sonnet, Opus and Luna, "
        "and is ignored by DeepSeek and Qwen; requiring an hourly market note beside it turns Sonnet's silence into honest talk; \"do not discuss prices\" produces no-undercut pacts without a number. "
        "Claude cells are 20-round samples plus the 30-round sets; Qwen faced algorithmic buyers (hollow dots)."),
    3: ("fig_gag.png", "86%",
        "The 2025 overseer's gag, in rounds relative to the gag (all 20 watched markets were gagged between rounds 1 and 7). Left: share of seller messages "
        "labelled collusive. Middle: share of the sellers' private strategy notebooks that coordinate (hold a common price or avoid undercutting). Right: mean ask. "
        "The talk ends in both conditions; without CEO pressure the notebooks fade and asks fall toward the competitive price, with it the notebooks hold and asks stay near \\$96.5."),
}
HONEST_TABLE = [None]
APPENDIX_FIGS = {
    "A1": ("fig_silent_pricing.png", "3.15in",
           "The one silent high-pricing market as an illustration: Opus 5.5 under \"set your ask independently\" sent no message in 20 rounds and held its asks within about "
           "\\$0.10 of each other, against the range of the honest Haiku markets over the same rounds and the price screen's bar."),
    "A2": ("fig_plan_message.png", "100%",
           "Private plans and notebooks against public messages, 2025 chat markets. (a) Seller turns by condition. (b) By round, the share of turns whose private notebook "
           "coordinates and whose public message is collusive, under the overseer with and without CEO pressure."),
}


def esc(t):
    """Escape Typst specials in prose, keeping inline code, bold and links."""
    t = t.replace("\\", "\\\\")
    # protect inline code
    codes = re.findall(r"`[^`]*`", t)
    for i, c in enumerate(codes):
        t = t.replace(c, f"\x00{i}\x00")
    t = t.replace("$", "\\$").replace("#", "\\#").replace("@", "\\@").replace("_", "\\_").replace("<", "\\<").replace(">", "\\>")
    t = re.sub(r"\*\*(.+?)\*\*", r"*\1*", t)  # bold
    t = re.sub(r"\[([^\]]*)\]", lambda m: "#mark[" + m.group(1) + "]", t)  # any bracketed note to Arty
    for i, c in enumerate(codes):
        t = t.replace(f"\x00{i}\x00", c)
    return t


def md_table_to_typst(md, caption, label=None, drop=(), strip_alarm=False, cols=None):
    rows = [r for r in md.strip().split("\n") if r.startswith("|")]
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    header, body = cells[0], [r for r in cells[1:] if not set("".join(r)) <= set("-: ")]
    keep = [i for i, h in enumerate(header) if h not in drop]
    header = [header[i] for i in keep]
    body = [[r[i] for i in keep] for r in body]
    if strip_alarm:
        body = [[re.sub(r";\s*r\d+\)", ")", c) for c in r] for r in body]
    ncol = len(header)
    cols = cols or ", ".join(["1.6fr"] + ["1fr"] * (ncol - 1))
    out = [f"#figure(table(columns: ({cols}), align: left,", "  table.hline(stroke: 0.6pt),",
           "  " + ", ".join(f"[*{esc(h)}*]" for h in header) + ",", "  table.hline(stroke: 0.4pt),"]
    for r in body:
        out.append("  " + ", ".join(f"[{esc(c)}]" for c in r) + ",")
    out.append("  table.hline(stroke: 0.6pt)),")
    out.append(f"  caption: [{caption}])" + (f" <{label}>" if label else ""))
    return "\n".join(out)


def table1():
    r = pd.read_csv(ROOT / "runs/derived/detect-results-explicit.csv")
    h = r[r["set"] == "2025 headline"].set_index("detector")
    k = r[r["set"] == "Haiku chat"].set_index("detector")
    rows = [("Chat and judge", "20 Haiku 5.5 markets told the conduct is illegal", int(h.loc["words_hard", "n_honest"]), f"{h.loc['words_hard', 'certified_fa']:.1%}"),
            ("Prices, 2025 markets", "10 GPT-4.1 markets with no channel", int(h.loc["deeds", "n_honest"]), f"{h.loc['deeds', 'certified_fa']:.1%}"),
            ("Prices, 2026 markets", "20 Haiku no-chat plus the 20 illegal-sentence markets (price rule)", int(k.loc["deeds", "n_honest"]), f"{k.loc['deeds', 'certified_fa']:.1%}")]
    out = ["#figure(table(columns: (1.2fr, 2.6fr, 0.5fr, 0.9fr), align: (left, left, right, right),", "  table.hline(stroke: 0.6pt),",
           "  [*Monitor*], [*Honest reference*], [*n*], [*Certified rate*],", "  table.hline(stroke: 0.4pt)"]
    for a, b, n, c in rows:
        out.append(f"  , [{a}], [{b}], [{n}], [{c}]")
    out.append("  , table.hline(stroke: 0.6pt)),")
    out.append("  caption: [Honest references and the certified false-alarm rate of each monitor, k/(n+1) with k = max(1, floor(0.05 (n+1))).]) <tab1>")
    return "\n".join(out)


def figure(path, width, caption, label, float_=False):
    place = ", placement: auto" if float_ else ""
    return f"#figure(image(\"{FIG}/{path}\", width: {width}){place}, caption: [{caption}]) <{label}>"


HEAD = r'''// Built by report/build_final.py from report/draft/report-draft.md. Do not edit by hand; edit the draft and rebuild.
#let mark(body) = text(fill: rgb("#b4530a"), style: "italic")[\[#body\]]
#set page(paper: "us-letter", margin: 1in, numbering: "1", number-align: center)
#set text(font: "Old Standard TT", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.52em, spacing: 0.85em)
#set heading(numbering: (..n) => if n.pos().len() == 1 { str(n.pos().at(0)) + "." } else { n.pos().map(str).join(".") })
#show heading.where(level: 1): it => block(above: 1.3em, below: 0.7em)[#text(size: 14pt, weight: "bold")[#if it.numbering != none [#counter(heading).display() ] #it.body]]
#show heading.where(level: 2): it => block(above: 1em, below: 0.5em)[#text(size: 11pt, weight: "bold")[#if it.numbering != none [#counter(heading).display() ] #it.body]]
#show figure.caption: it => context [#align(left)[#text(size: 10pt)[*#it.supplement #it.counter.display(it.numbering).* #it.body]]]
#set figure(gap: 6pt)
#show table: set text(size: 8.5pt)
#show table: set par(justify: false)
#set table(stroke: none, inset: (x: 3.5pt, y: 2.5pt))
#show link: underline
'''


def main():
    md = DRAFT.read_text()
    lines = md.split("\n")
    # title: first "# " line
    title = next(l[2:].strip() for l in lines if l.startswith("# "))
    # strip the draft's preamble (everything before "## Abstract")
    body = md[md.index("## Abstract"):]
    # abstract text: between "## Abstract" and the next "## "
    abs_block = body[len("## Abstract"):body.index("\n## ", 1)]
    abs_paras = [p for p in abs_block.strip().split("\n\n") if p.strip() and not p.strip().startswith("[")]
    abstract = " ".join(p.replace("\n", " ") for p in abs_paras)
    rest = body[body.index("\n## ", 1):]

    out = [HEAD, "", "#line(length: 100%, stroke: 0.8pt)", "#v(6pt)",
           f"#align(center)[#text(size: 19pt, weight: \"bold\")[{esc(title.upper())}#footnote[Research conducted at the AI Collusion Research Sprint, October 2026.]]]",
           "#v(6pt)", "#line(length: 100%, stroke: 0.8pt)", "#v(10pt)",
           "#align(center)[Arthur Troy \\ Independent, Chantilly, Virginia #v(6pt) *With* \\ Apart Research]", "#v(10pt)",
           "#align(center)[#text(size: 14pt, weight: \"bold\")[Abstract]]",
           f"#block(inset: (x: 0.55in))[{esc(abstract)}]", ""]

    placed = set()
    in_appendix = False
    appendix_items = []  # (letter, title, text)
    refs_mode = False
    paras = re.split(r"\n\n+", rest.strip())
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if p.startswith("## "):
            h = p[3:].strip()
            if refs_mode:  # close the references block before the next heading
                out.append("]")
                out.append("#set par(justify: true, hanging-indent: 0pt)")
            refs_mode = False
            if re.match(r"^\d+\.\s", h):
                out.append(f"= {esc(re.sub(r'^\d+\.\s*', '', h))}")
            elif h.lower().startswith("appendix"):
                in_appendix = True
            elif h.lower() == "references":
                out.append("#heading(numbering: none)[References]")
                out.append("#set par(justify: false, hanging-indent: 1.2em)")
                out.append("#text(size: 10pt)[")
                refs_mode = True
            else:
                out.append(f"#heading(numbering: none)[{esc(h)}]")
            continue
        if p.startswith("### "):
            out.append(f"== {esc(re.sub(r'^\d+\.\d+\s*', '', p[4:].strip()))}")
            continue
        if refs_mode:
            if re.match(r"^\d+\.\s", p):
                for item in re.split(r"\n(?=\d+\.\s)", p):
                    out.append("+ " + esc(re.sub(r"^\d+\.\s*", "", item.replace("\n", " "))))
            elif p.startswith("["):
                out.append("#mark[" + esc(p.strip("[]")) + "]")
            continue
        if in_appendix:
            m = re.match(r"^\*\*([A-Z])\.\s*(.+?)\*\*\s*(.*)$", p, re.S)
            if m:
                appendix_items.append((m.group(1), m.group(2).rstrip("."), m.group(3)))
            elif appendix_items:
                appendix_items[-1] = (appendix_items[-1][0], appendix_items[-1][1], appendix_items[-1][2] + "\n\n" + p)
            continue
        # pre-registration grey box
        if p.startswith("**Pre-registration.**"):
            out.append("#block(width: 100%, fill: luma(245), stroke: 0.5pt + luma(150), inset: 8pt, radius: 2pt)[" + esc(p.replace("\n", " ")) + "]")
            continue
        # numbered list
        if re.match(r"^\d+\.\s", p):
            for item in re.split(r"\n(?=\d+\.\s)", p):
                out.append("+ " + esc(re.sub(r"^\d+\.\s*", "", re.sub(r"\n\s+", " ", item))))
            out.append("")
            continue
        if p.startswith("- "):
            for item in p.split("\n- "):
                out.append("- " + esc(item.lstrip("- ").replace("\n", " ")))
            out.append("")
            continue
        # a markdown table in the draft: "**Table N.** caption" on the first line, the rows beneath (the cast table in Methods)
        if p.startswith("**Table") and "\n|" in p:
            cap, tab = p.split("\n|", 1)
            cap = re.sub(r"^\*\*Table \d+\.\*\*\s*", "", cap.replace("\n", " "))
            out.append(md_table_to_typst("|" + tab, esc(cap), "tabcast", cols="1.45fr, 0.8fr, 0.3fr, 3.6fr")); out.append("")
            continue
        text = esc(p.replace("\n", " "))
        out.append(text)
        out.append("")
        # tables after the paragraph that first cites them (Table 1 is the cast table, written in the draft itself)
        if "Table 2" in p and "tab1" not in placed:
            out.append(table1()); out.append(""); placed.add("tab1")
        if "Table 3" in p and "tab2" not in placed:
            t2 = (ROOT / "report/draft/table2.md").read_text()
            main_tab = t2[:t2.index("**Honest markets**")]
            honest_tab = t2[t2.index("**Honest markets**"):]
            cap_main = re.search(r"\*\*Table 2\.\*\*\s*(.+?)\n\n", main_tab, re.S).group(1).replace("\n", " ")  # table2.md keeps its file name; it is Table 3 in the report
            cap_main = cap_main.replace("'Chat + prices' is the pre-registered comparison", "The chat-or-prices union equals chat in every row and is omitted; 'chat + prices' is the pre-registered comparison")
            cap_main = re.sub(r"r = median round of first alarm\.", "Median first alarm: round 1 for chat in every set (round 2 for Luna), round 6 for prices, round 2 to 24 for the judge.", cap_main)
            out.append(md_table_to_typst(main_tab, esc(cap_main), "tab2", drop=("Chat or prices",), strip_alarm=True)); out.append("")
            placed.add("tab2")
            HONEST_TABLE[0] = md_table_to_typst(honest_tab, esc("Honest markets (no collusive design): false alarms per monitor, reference runs scored leave-one-out."), "tab2b")
        for n, (path, width, cap) in CAPTIONS.items():
            if f"Figure {n}" in p and f"fig{n}" not in placed:
                out.append(figure(path, width, cap, f"fig{n}", float_=(n == 3))); out.append(""); placed.add(f"fig{n}")
    if refs_mode:
        out.append("]")
        out.append("#set par(justify: true, hanging-indent: 0pt)")
    # appendix, reordered: Limitations and Dual-Use first, LLM usage second, then the rest in draft order
    out.append("#counter(figure.where(kind: image)).update(0)")
    out.append("#set figure(numbering: n => \"A\" + str(n))")
    def key(item):
        t = item[1].lower()
        return (0 if "dual" in t else 1 if "usage" in t else 2, item[0])
    letters = "ABCDEFGHIJ"
    for i, (_, title, text) in enumerate(sorted(appendix_items, key=key)):
        tl = title.lower()
        shown = "Limitations and Dual-Use / Ethical Considerations" if "dual" in tl else ("LLM Usage Statement" if "usage" in tl else title)
        out.append(f"#heading(numbering: none)[Appendix {letters[i]}. {esc(shown)}]")
        for para in text.strip().split("\n\n"):
            out.append(esc(para.replace("\n", " ")))
            out.append("")
        if "honest markets" in tl and HONEST_TABLE[0]:
            out.append(HONEST_TABLE[0]); out.append("")
    leftover = [lab for lab in APPENDIX_FIGS if lab not in placed]
    if leftover:
        out.append(f"#heading(numbering: none)[Appendix {letters[len(appendix_items)]}. Additional figures]")
        for lab in leftover:
            path, width, cap = APPENDIX_FIGS[lab]
            out.append(figure(path, width, cap, lab)); out.append(""); placed.add(lab)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out) + "\n")
    print("wrote", OUT.relative_to(ROOT), f"({len(out)} lines); figures placed: {sorted(placed)}")


if __name__ == "__main__":
    main()
