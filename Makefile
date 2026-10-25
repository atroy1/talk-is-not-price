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
test:        ## synthetic tests for the scores, detector and labeller
	.venv/bin/python -m pytest -q tests
labels:      ## graded labels for every seller message (resumable); ARGS=--live adds finished new runs, ARGS=--check compares with the hand labels
	.venv/bin/python -m analysis.labels $(ARGS)
handlabel-check: ## the 40-message check: two blind Claude readers, the consensus, and the labeller (40 API calls)
	.venv/bin/python -m analysis.handlabel_check
reproduce:   ## every table and draft figure from the runs and the cached labels (no API calls): the freeze command
	.venv/bin/python -m analysis.controls
	.venv/bin/python -m analysis.compete_check explicit
	.venv/bin/python -m analysis.detect --chat-reference explicit
	.venv/bin/python -m analysis.detect --chat-reference compete
	.venv/bin/python -m analysis.flag_matrix
	.venv/bin/python -m analysis.message_taxonomy
	.venv/bin/python -m analysis.private_plan
	.venv/bin/python -m analysis.overcharge
	.venv/bin/python -m analysis.keyword_rule
	.venv/bin/python -m analysis.gag_timeline
	.venv/bin/python -m analysis.extras
	.venv/bin/python -m analysis.behaviour_screen
	.venv/bin/python -m analysis.tables
	for f in report/fig1_seen_missed.py report/fig2_quadrant.py report/fig_quadrant_dollars.py report/fig2_instructions.py report/fig_plan_message.py report/fig_silent_pricing.py report/fig_gag.py; do .venv/bin/python $$f || exit 1; done
	@echo "reproduced $$(date '+%Y-%m-%d %H:%M') from commit $$(git rev-parse --short HEAD)"
figures-final: ## the print figures: no DRAFT tag, 300 dpi, into report/final/figures/
	for f in report/fig_quadrant_dollars.py report/fig_gag.py report/fig2_instructions.py report/fig_silent_pricing.py report/fig_plan_message.py; do FINAL=1 .venv/bin/python $$f || exit 1; done
final:       ## the submission PDF: figures, report.typ from the draft, typst compile, page and font checks
	$(MAKE) figures-final
	.venv/bin/python report/build_final.py
	typst compile --font-path report/fonts report/final/report.typ report/final/report.pdf
	@pdfinfo report/final/report.pdf | grep -E "Pages|File size"; pdffonts report/final/report.pdf | grep -c "OldStandard" | xargs echo "Old Standard TT faces embedded:"
freeze:      ## make reproduce, then write notes/results-frozen.md (every citable number with its source file)
	$(MAKE) reproduce
	.venv/bin/python -m analysis.freeze
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
QNAME = $(notdir $(basename $(QUEUE)))
studio-queue: ## launch a queue on the Studio, detached and kept awake (default the Friday one; QUEUE=config/queue-qwen.toml for the Qwen arm; ARGS=--fake to test)
	$(MAKE) studio-sync
	ssh $(STUDIO) 'cd $(SDIR) && rm -f runs/STOP && mkdir -p runs/live && nohup caffeinate -is .venv-tools/bin/python -m tools.run_queue $(QUEUE) $(ARGS) --log runs/live/$(QNAME).log.md > runs/live/$(QNAME).out 2>&1 < /dev/null & echo launched $(QUEUE)'
studio-status: ## every Studio queue: last log lines, live processes
	ssh $(STUDIO) 'cd $(SDIR) && for f in runs/live/*.log.md; do [ -f "$$f" ] && echo "== $$f" && tail -n 4 "$$f"; done; echo "== running"; pgrep -fl "tools.run_queue" | sed "s/.*run_queue //" || echo "no queue running"'
QWEN ?= 35b
studio-mlx-up: ## start the seeded Qwen servers on the Studio: QWEN=35b (default; ports 8083/8084) or QWEN=9b (8081/8082)
	ssh $(STUDIO) 'cd $(SDIR) && mkdir -p runs/live && if [ "$(QWEN)" = 9b ]; then set -- 8081:9B-stock 8082:9B-abliterated; else set -- 8083:35B-A3B-stock 8084:35B-A3B-abliterated; fi; for spec in "$$@"; do port=$${spec%%:*}; name=$${spec##*:}; curl -s -m 2 localhost:$$port/v1/models >/dev/null && echo "$$port up" || { nohup .venv-tools/bin/python -m mlx_lm server --model ~/.lmstudio/models/local-sprint/Qwen3.5-$$name-MLX-4bit --host 0.0.0.0 --port $$port > runs/live/mlx-$$name.log 2>&1 < /dev/null & echo "$$port starting ($$name)"; }; done'
studio-mlx-down: ## stop all Qwen servers
	ssh $(STUDIO) 'pkill -f "mlx_lm server" && echo stopped || echo "none running"'
studio-qwen: ## sprint only (Friday 4:10 PM): free LM Studio's memory, start the two seeded 35B servers
	ssh $(STUDIO) '~/.lmstudio/bin/lms unload --all >/dev/null 2>&1; echo "LM Studio models unloaded"'
	$(MAKE) studio-mlx-up
studio-stop: ## finish the current run, then stop
	ssh $(STUDIO) 'cd $(SDIR) && touch runs/STOP && echo "STOP set: the queue ends after the current run"'
studio-pull: ## bring finished runs and the queue log back to the laptop
	rsync -az $(STUDIO):$(SDIR)/runs/live/ runs/live/
	@ls runs/live | grep -v -E 'queue' | wc -l | xargs echo "run folders here:"
compete-on:  ## Friday 4 PM lock: switch on the compete runs in both queues (refuses until the template exists)
	$(PY) tools/compete_on.py
help:
	@grep -E '^[a-z-]+:.*##' Makefile | sed 's/:.*##/  /'
.PHONY: studio-sync studio-setup studio-queue studio-status studio-stop studio-pull g0 ping self-test ledger talk notes figs mock queue queue-dry queue-fake help
