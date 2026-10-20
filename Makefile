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
help:
	@grep -E '^[a-z-]+:.*##' Makefile | sed 's/:.*##/  /'
.PHONY: g0 ping self-test ledger talk notes figs mock queue queue-dry queue-fake help
