#!/usr/bin/env python3
"""Where each queue stands: runs finished, unfinished, and whether its run_queue process is alive.

Sprint plumbing, Fri Oct 23 2026, for the scheduled check-ins (docs/CHECKIN.md). Runs on the machine that holds
runs/live (the Studio). Prints one JSON object: {queue_path: {"total", "done", "unfinished", "running", "next"}}.

    .venv-tools/bin/python -m tools.queue_state config/queue-qwen.toml config/queue-honest-explicit-a.toml ...
"""
import json
import subprocess
import sys
import tomllib
from pathlib import Path

from tools.run_queue import LIVE, rounds_done


def state(queue):
    q = tomllib.load(open(queue, "rb"))
    rounds_default = q.get("defaults", {}).get("rounds", 30)
    done, unfinished = [], []
    for r in q.get("runs", []):
        need = r.get("rounds", rounds_default)
        (done if rounds_done(LIVE / r["tag"] / "run" / "auction_results.md") >= need else unfinished).append(r["tag"])
    alive = subprocess.run(["pgrep", "-f", f"run_queue {queue}"], capture_output=True, text=True).stdout.split()
    return {"total": len(done) + len(unfinished), "done": len(done), "unfinished": len(unfinished),
            "running": bool(alive), "next": unfinished[:3]}


if __name__ == "__main__":
    print(json.dumps({q: state(q) for q in sys.argv[1:] if Path(q).exists()}, indent=1))
