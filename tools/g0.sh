#!/usr/bin/env bash
# Gate G0 readiness check (PLAYBOOK section 3). Run any time: `make g0`. Prints one line per item, green or red.
cd "$(dirname "$0")/.."
PY=.venv-tools/bin/python
ok(){ printf '  \033[32mOK  \033[0m %s\n' "$*"; }; bad(){ printf '  \033[31mRED \033[0m %s\n' "$*"; }
set -a; [ -f .env ] && . ./.env; set +a
echo "G0 readiness, $(date '+%a %b %d %H:%M')"
[ -n "${ANTHROPIC_API_KEY:-}" ]  && ok "ANTHROPIC_API_KEY set in .env"  || bad "ANTHROPIC_API_KEY empty: claude.ai > Settings > Billing > API credits, then a key at platform.claude.com, paste into .env"
case "${ANTHROPIC_API_KEY:-}" in sk-ant-usr*|sk-ant-admin*) [ -n "${ANTHROPIC_WORKSPACE_ID:-}" ] && ok "ANTHROPIC_WORKSPACE_ID set (organisation-level key)" || bad "Anthropic key is organisation-level: set ANTHROPIC_WORKSPACE_ID in .env (Console > Settings > Workspaces, the wrkspc_ id) or make a workspace-scoped key; until then Claude runs go through OpenRouter";; esac
[ -n "${OPENROUTER_API_KEY:-}" ] && ok "OPENROUTER_API_KEY set in .env" || bad "OPENROUTER_API_KEY empty: openrouter.ai > Keys, prepay \$20, paste into .env"
[ -n "${LMSTUDIO_BASE_URL:-}" ]  && ok "LMSTUDIO_BASE_URL set"          || bad "LMSTUDIO_BASE_URL empty"
if [ -n "${ANTHROPIC_API_KEY:-}" ] || [ -n "${OPENROUTER_API_KEY:-}" ]; then
  $PY -m tools.llm --ping 2>&1 | sed 's/^/     /'
fi
if curl -s --max-time 3 "${LMSTUDIO_BASE_URL:-http://arthurs-mac-studio.local:1234/v1}/models" | grep -q '"id"'; then
  ok "LM Studio server answers: $(curl -s --max-time 3 "${LMSTUDIO_BASE_URL:-http://arthurs-mac-studio.local:1234/v1}/models" | python3 -c 'import json,sys; print(", ".join(m["id"] for m in json.load(sys.stdin)["data"])[:120])')"
else bad "LM Studio server not reachable on the Studio (Developer tab: start server, serve on local network, port 1234)"; fi
ssh -o BatchMode=yes -o ConnectTimeout=3 arthurs-mac-studio.local true 2>/dev/null && ok "ssh to the Studio works" || bad "ssh to the Studio refused (System Settings > General > Sharing > Remote Login)"
ssh -o BatchMode=yes -o ConnectTimeout=3 arthurs-mac-studio.local 'cd Developer/AMER/apart-collusion-sprint && test -x .venv/bin/python && test -x .venv-tools/bin/python && test -f .env' 2>/dev/null && ok "Studio has the repo, both Python environments and .env (make studio-sync before launching)" || bad "Studio copy missing: make studio-sync && make studio-setup"
[ -x .venv/bin/python ] && WANDB_MODE=disabled .venv/bin/python -c "import src.continuous_double_auction.simulation" 2>/dev/null && ok "starter imports in .venv" || bad "starter does not import"
$PY -m tools.llm --self-test >/dev/null 2>&1 && ok "router self-test" || bad "router self-test failed"
$PY -m tools.run_queue config/queue-friday.toml --dry-run >/dev/null 2>&1 && ok "Friday queue parses ($($PY -m tools.run_queue config/queue-friday.toml --dry-run | tail -1))" || bad "Friday queue does not parse"
[ -d runs/live/fake-check/run ] && ok "fake-server market check done earlier" || bad "run: make queue-fake"
[ -f talks/test-sample/transcript.md ] && ok "talk pipeline checked on a clip" || bad "run: tools/talks.sh test-sample <clip>"
for t in ffmpeg yt-dlp typst caffeinate; do command -v $t >/dev/null && ok "$t present" || bad "$t missing"; done
free=$(df -g / | awk 'NR==2{print $4}'); [ "$free" -ge 10 ] && ok "disk ${free} GB free" || bad "disk ${free} GB free: clear space"
echo "  by hand: survey filled, Discord joined, Luma RSVPs for both Friday talks, Google Doc copy made from the Guidelines tab, framing chosen"
