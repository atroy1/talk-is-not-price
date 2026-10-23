#!/usr/bin/env python3
"""Switch on the compete runs in both queues at the Friday 4 PM lock (make compete-on).

Refuses until the compete prompt template exists, then uncomments every commented [[runs]] block that uses the compete
template (compete and cost-shock runs) in config/queue-friday.toml and config/queue-qwen.toml. Idempotent. --check only reports.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "vendor/llm-agent-collusion/src/continuous_double_auction/prompt_templates/seller_prompt_compete.jinja2"
QUEUES = [ROOT / "config/queue-friday.toml", ROOT / "config/queue-qwen.toml"]
BLOCK = re.compile(r'(^# \[\[runs\]\]\n(?:^# [a-z_]+ = [^\n]*\n)+)', re.M)  # a whole commented run, every key


def wanted(block):
    """Compete and cost-shock runs go on at the lock; Saturday forks and branches stay off (they need picks)."""
    return "seller_prompt_compete" in block and not any(k in block for k in ("force_", "inject_", "think_prefill"))


def main():
    check = "--check" in sys.argv
    if not TEMPLATE.exists() and not check:
        sys.exit(f"refused: write {TEMPLATE.relative_to(ROOT)} first (the base seller prompt plus the compete sentence)")
    for q in QUEUES:
        s = q.read_text()
        blocks = [b for b in BLOCK.findall(s) if wanted(b)]
        live = len(re.findall(r'^tag = "[^"]*compete', s, re.M))
        if check:
            print(f"{q.name}: {live} compete runs on, {len(blocks)} waiting")
            continue
        for b in blocks:
            s = s.replace(b, re.sub(r"^# ", "", b, flags=re.M), 1)
        q.write_text(s)
        print(f"{q.name}: switched on {len(blocks)} compete runs ({live + len(blocks)} on now)")


if __name__ == "__main__":
    main()
