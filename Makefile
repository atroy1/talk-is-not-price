# Sprint shortcuts. Everything here is plumbing; results code lives in analysis/ and starts Friday.
PY=.venv-tools/bin/python

ping:        ## one tiny call per lane that has a key
	$(PY) -m tools.llm --ping
self-test:   ## router against a fake server, no keys
	$(PY) -m tools.llm --self-test
ledger:      ## spend so far by lane and task
	$(PY) -m tools.llm --ledger
talk:        ## make talk SLUG=anwar SRC=<url or file>
	tools/talks.sh $(SLUG) $(SRC)
notes:       ## make notes SLUG=anwar SPEAKER="Usman Anwar" TITLE="..." URL=...
	$(PY) -m tools.talk_notes $(SLUG) --speaker "$(SPEAKER)" --title "$(TITLE)" --url "$(URL)"
figs:        ## layout-proof figures (synthetic numbers)
	.venv/bin/python report/fig_proof.py
mock:        ## the page-budget mock-up of the report
	typst compile --font-path report/fonts report/mock/report.typ report/mock/mock.pdf && pdfinfo report/mock/mock.pdf | grep Pages
queue-dry:   ## print the Friday queue's commands and cost, run nothing
	$(PY) -m tools.run_queue config/queue-friday.toml --dry-run
queue:       ## run the Friday queue unattended (caffeinate keeps the Mac awake); touch runs/STOP to stop after the current run
	caffeinate -is $(PY) -m tools.run_queue config/queue-friday.toml
queue-fake:  ## 2-round plumbing check against the built-in fake server, no keys
	$(PY) -m tools.run_queue config/queue-fake.toml --fake
g0:          ## gate G0 readiness check, one line per item
	tools/g0.sh
# ---- Mac Studio: code goes laptop -> Studio, results come Studio -> laptop (never the other way)
STUDIO=arthurs-mac-studio.local
SDIR=Developer/AMER/apart-collusion-sprint
studio-sync: ## copy code, config, .env and the starter to the Studio (results and media stay put)
	rsync -az --delete --exclude .venv/ --exclude .venv-tools/ --exclude 'runs/live/' --exclude 'talks/' \
	  --exclude 'vendor/*' --include 'vendor/llm-agent-collusion/***' --exclude '__pycache__/' --exclude '.git/' \
	  --exclude 'report/mock/*.png' ./ $(STUDIO):$(SDIR)/
	rsync -az --delete --exclude '__pycache__/' --exclude 'results/' vendor/llm-agent-collusion/ $(STUDIO):$(SDIR)/vendor/llm-agent-collusion/
studio-setup: ## one-off: build the two Python environments on the Studio
	ssh $(STUDIO) 'cd $(SDIR) && ~/.local/bin/uv venv -q --python 3.12 .venv && ~/.local/bin/uv pip install -q --python .venv/bin/python -r config/starter-requirements.lock && ~/.local/bin/uv pip install -q --python .venv/bin/python -e vendor/llm-agent-collusion && ~/.local/bin/uv venv -q --python 3.12 .venv-tools && ~/.local/bin/uv pip install -q --python .venv-tools/bin/python openai anthropic && echo studio envs ok'
QUEUE ?= config/queue-friday.toml
studio-queue: ## launch a queue on the Studio, detached and kept awake (default the Friday one; QUEUE=... ARGS=--fake to test)
	$(MAKE) studio-sync
	ssh $(STUDIO) 'cd $(SDIR) && rm -f runs/STOP && mkdir -p runs/live && nohup caffeinate -is .venv-tools/bin/python -m tools.run_queue $(QUEUE) $(ARGS) --log runs/live/queue-log.md > runs/live/queue.out 2>&1 < /dev/null & echo launched $(QUEUE)'
studio-status: ## what the Studio queue is doing: last log lines, live process, spend so far
	ssh $(STUDIO) 'cd $(SDIR) && tail -n 8 runs/live/queue-log.md 2>/dev/null; pgrep -fl "tools.run_queue|continuous_double_auction" | cut -c1-90 || echo "queue not running"; tail -c 300 runs/live/queue.out 2>/dev/null'
studio-stop: ## finish the current run, then stop
	ssh $(STUDIO) 'cd $(SDIR) && touch runs/STOP && echo "STOP set: the queue ends after the current run"'
studio-pull: ## bring finished runs and the queue log back to the laptop
	rsync -az $(STUDIO):$(SDIR)/runs/live/ runs/live/
	@ls runs/live | grep -v -E 'queue' | wc -l | xargs echo "run folders here:"
help:
	@grep -E '^[a-z-]+:.*##' Makefile | sed 's/:.*##/  /'
.PHONY: studio-sync studio-setup studio-queue studio-status studio-stop studio-pull g0 ping self-test ledger talk notes figs mock queue queue-dry queue-fake help
