# Scheduled check-ins (Sat Oct 24, 5 AM and 10 AM ET)

Written Fri Oct 23 for the two scheduled runs. Each run starts with no memory of the Friday session, so this page is
the whole brief. Arty is at work 7 AM to noon Saturday; the 10 AM run reaches him on his phone.

## What to do, in order

1. `cd ~/Developer/AMER/apart-collusion-sprint`, then read the last 40 lines of `notes/log.md` for the state of play.
2. Run the check-in script. It is safe to run more than once:

   ```bash
   .venv/bin/python -m tools.checkin
   ```

   It checks the Studio is reachable, syncs code, reads every queue, relaunches any queue that stopped with runs
   unfinished, restarts the Qwen servers and queue if they died, launches `config/wave2/*.toml` only if
   `config/wave2/READY` exists, pulls results, labels new seller messages, runs the price check and both detector
   tables, totals spend, and ends with a SUMMARY block. Transcript: `runs/derived/checkin-<date>-<time>.txt`.
3. Append one entry to `notes/log.md`: the time, the SUMMARY lines, and the headline numbers from the detector table
   with the explicit reference (catch rates for words, deeds, fused and the judge on the 2025 headline set; the
   cost-shock false alarms; the price-check decision). Mark numbers PROVISIONAL while any queue is unfinished.
4. Send Arty one push notification, under 200 characters, leading with anything he must act on, then progress,
   for example: "Sprint 5 AM: all queues healthy; Qwen 9/15 done; 0 failures; Claude $48 of $100. Nothing needed."
5. Stop. Do not wait for queues to finish.

## Rules

- Never commit, push, or edit `notes/preregistration.md`. Log entries only.
- Never remove `runs/STOP` on the Studio. It is Arty's stop switch; the script leaves it alone and says so.
- No new runs beyond relaunching queued ones and a wave 2 that Friday's session marked READY. No design changes.
- If a queue stopped on an account limit (its log says ACCOUNT LIMIT, or the API says "usage limits" or "credit
  balance"), do not try to get around it: report it in the notification. Raising a limit is Arty's step in the
  Claude Console (platform.claude.com/settings/billing, Spend limits) or OpenRouter (Credits).
- If the Studio is unreachable, say so in the notification and stop: the laptop may be off the home network.
- Keys live in `.env`; never print them.

## Where things are

| What | Where |
|---|---|
| Queues (API) | `config/queue-honest-explicit-a.toml`, `-b`, `config/queue-costshock-explicit.toml`, `config/queue-compete-to10.toml`, `config/queue-crossmodel-or.toml`, `config/queue-costshock12-explicit.toml`, `config/queue-haiku-chat-more.toml` |
| Qwen arm | `config/queue-qwen.toml`, servers on Studio ports 8083/8084 (`make studio-mlx-up`) |
| Run outputs | Studio `~/Developer/AMER/apart-collusion-sprint/runs/live/<tag>/`, pulled to the laptop by `make studio-pull` |
| Detector | `analysis/detect.py` (headline: `--chat-reference explicit`, declared deviation 3) |
| Decisions | `notes/preregistration.md` (locked claim, predictions, deviations 1-3), `notes/log.md` |
