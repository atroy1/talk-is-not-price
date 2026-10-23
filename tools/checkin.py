#!/usr/bin/env python3
"""Scheduled check-in: health, relaunch, pull, analyse, summarise. Safe to run more than once. See docs/CHECKIN.md.

    .venv/bin/python -m tools.checkin            # full check-in (relaunches what stopped early)
    .venv/bin/python -m tools.checkin --report   # look only: no relaunch, no wave 2

Sprint plumbing, Fri Oct 23 2026. Runs on the laptop; drives the Studio over ssh. Writes the whole transcript to
runs/derived/checkin-<date>-<time>.txt and ends with a SUMMARY block for the scheduled session to log and send.
Safety rules: never starts a queue that is already running; never removes runs/STOP (Arty's stop switch); never
relaunches a queue whose log ends in an account-limit stop; wave 2 only when config/wave2/READY exists.
"""
import argparse
import datetime
import glob
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDIO = "arthurs-mac-studio.local"
SDIR = "Developer/AMER/apart-collusion-sprint"
API_QUEUES = ["config/queue-honest-explicit-a.toml", "config/queue-honest-explicit-b.toml",
              "config/queue-costshock-explicit.toml", "config/queue-compete-to10.toml", "config/queue-crossmodel-or.toml",
              "config/queue-costshock12-explicit.toml", "config/queue-haiku-chat-more.toml"]
QWEN_QUEUE = "config/queue-qwen.toml"
LINES = []


def say(msg=""):
    print(msg, flush=True)
    LINES.append(str(msg))


def ssh(cmd, timeout=180):
    try:
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", STUDIO, f"cd {SDIR} && {cmd}"],
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def local(cmd, timeout=900):
    try:
        r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def launch(queue):
    name = Path(queue).stem
    code, out, err = ssh(f"nohup caffeinate -is .venv-tools/bin/python -m tools.run_queue {queue} "
                         f"--log runs/live/{name}.log.md > runs/live/{name}.out 2>&1 < /dev/null & echo launched")
    return code == 0 and "launched" in out


def limit_stopped(queue):
    name = Path(queue).stem
    code, out, _ = ssh(f"tail -n 3 runs/live/{name}.log.md 2>/dev/null")
    return "ACCOUNT LIMIT" in out


def qwen_servers_up():
    code, out, _ = ssh("for p in 8083 8084; do curl -s -m 3 localhost:$p/v1/models >/dev/null && printf up || printf down; printf ' '; done")
    return out.split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="look only: no relaunch, no wave 2")
    a = ap.parse_args()
    stamp = datetime.datetime.now()
    say(f"check-in {stamp:%a %b %d %H:%M} ({'report only' if a.report else 'full'})")
    actions, problems = [], []

    code, _, _ = ssh("true", timeout=20)
    if code != 0:
        say("STUDIO UNREACHABLE: the laptop is off the home network, or the Studio is asleep. Nothing checked or relaunched.")
        finish(stamp, ["Studio unreachable; nothing checked"], [], {})
        return 2

    local("make studio-sync")
    wave2 = sorted(glob.glob(str(ROOT / "config/wave2/*.toml")))
    wave2 = [str(Path(w).relative_to(ROOT)) for w in wave2]
    queues = API_QUEUES + [QWEN_QUEUE] + wave2
    code, out, err = ssh(".venv-tools/bin/python -m tools.queue_state " + " ".join(queues))
    try:
        state = json.loads(out)
    except json.JSONDecodeError:
        say(f"could not read queue state: {err[-300:]}")
        state = {}
    stop_file = ssh("test -f runs/STOP && echo yes")[1].strip() == "yes"
    if stop_file:
        problems.append("runs/STOP is set on the Studio (Arty's stop switch): nothing relaunched")

    say("\nqueues (done/total, running):")
    for q in queues:
        s = state.get(q)
        if not s:
            continue
        say(f"  {Path(q).stem:<32} {s['done']:>2}/{s['total']:<2} {'running' if s['running'] else 'stopped'}"
            + (f"  next: {', '.join(s['next'])}" if s["unfinished"] else ""))

    if not a.report and not stop_file:
        for q in API_QUEUES:
            s = state.get(q)
            if not s or s["unfinished"] == 0 or s["running"]:
                continue
            if limit_stopped(q):
                problems.append(f"{Path(q).stem} stopped on an account spending/credit limit: not relaunched")
                continue
            ok = launch(q)
            actions.append(f"relaunched {Path(q).stem} ({s['unfinished']} runs left)" if ok else f"FAILED to relaunch {Path(q).stem}")
        s = state.get(QWEN_QUEUE)
        if s and s["unfinished"] and not s["running"]:
            servers = qwen_servers_up()
            if servers != ["up", "up"]:
                local("make studio-mlx-up")
                for _ in range(30):
                    time.sleep(10)
                    if qwen_servers_up() == ["up", "up"]:
                        break
                actions.append(f"restarted Qwen servers (were {' '.join(servers)})")
            if qwen_servers_up() == ["up", "up"]:
                ok = launch(QWEN_QUEUE)
                actions.append(f"relaunched Qwen queue ({s['unfinished']} runs left)" if ok else "FAILED to relaunch Qwen queue")
            else:
                problems.append("Qwen servers would not come up; Qwen queue not relaunched")
        if wave2 and (ROOT / "config/wave2/READY").exists():
            for q in wave2:
                s = state.get(q)
                if s and s["unfinished"] and not s["running"]:
                    ok = launch(q)
                    actions.append(f"launched wave 2 {Path(q).stem} ({s['unfinished']} runs)" if ok else f"FAILED to launch {Path(q).stem}")

    say("\nactions: " + ("; ".join(actions) if actions else "none needed"))
    if problems:
        say("problems: " + "; ".join(problems))

    say("\npulling results and labelling new messages ...")
    local("make studio-pull", timeout=1200)
    code, out = local(".venv/bin/python -m analysis.labels --live --workers 6", timeout=1800)
    say("  labels: " + (out.strip().splitlines()[-1] if out.strip() else f"exit {code}"))

    analyses = {}
    for label, cmd in [("price check, explicit runs", ".venv/bin/python -m analysis.compete_check explicit"),
                       ("detector, explicit reference (headline)", ".venv/bin/python -m analysis.detect --chat-reference explicit"),
                       ("detector, compete reference (pre-registered)", ".venv/bin/python -m analysis.detect --chat-reference compete")]:
        code, out = local(cmd, timeout=900)
        analyses[label] = out.strip()
        say(f"\n== {label} (exit {code})\n{out.strip()[-2500:]}")

    spend = spend_now()
    say(f"\nspend: {spend}")
    finish(stamp, actions, problems, analyses, spend)
    return 0


def spend_now():
    price = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
    month = datetime.date.today().strftime("%Y-%m")
    claude = 0.0
    for f in glob.glob(str(ROOT / "runs/live/**/usage.*.jsonl"), recursive=True):
        for line in open(f):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = d.get("model")
            if m in price and d.get("route") == "anthropic" and \
                    datetime.datetime.fromtimestamp(d.get("t", 0)).strftime("%Y-%m") == month:
                i = (d.get("input_tokens") or 0) + (d.get("cache_creation_input_tokens") or 0) + (d.get("cache_read_input_tokens") or 0)
                claude += i / 1e6 * price[m][0] + (d.get("output_tokens") or 0) / 1e6 * price[m][1]
    orr = "unknown"
    code, out = local("set -a && . ./.env && set +a && curl -s -m 10 https://openrouter.ai/api/v1/credits -H \"Authorization: Bearer $OPENROUTER_API_KEY\"")
    try:
        d = json.loads(out)["data"]
        orr = f"${d['total_credits'] - d['total_usage']:.2f} left"
    except Exception:  # noqa: BLE001
        pass
    return f"Claude this month about ${claude:.2f} of the $100 limit; OpenRouter {orr}"


def finish(stamp, actions, problems, analyses, spend=""):
    out = ROOT / "runs/derived" / f"checkin-{stamp:%Y%m%d-%H%M}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    say("\nSUMMARY")
    say(f"  when: {stamp:%a %H:%M}")
    say(f"  actions: {'; '.join(actions) if actions else 'none'}")
    say(f"  problems: {'; '.join(problems) if problems else 'none'}")
    if spend:
        say(f"  spend: {spend}")
    out.write_text("\n".join(LINES) + "\n")
    print(f"transcript -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
