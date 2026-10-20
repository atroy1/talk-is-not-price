# Talks: from speech to a line we can cite

Written 2026-10-18. Tested the same day on this laptop end to end (synthetic clip: audio, scene frames, transcript, prompts). The point is narrow: by Friday 4 PM, have the two Friday talks as timestamped transcripts and a one-page note each, so the Related Work paragraph can quote the speakers accurately and the lock meeting knows what they called unsolved.

## 1. Facts that shape it

- The sprint FAQ: "Recordings are shared on Discord after the event." After the event is too late for the report. Friday's talks have to be captured live.
- Thursday's two talks (Velja 10:15 AM, Motwani 1:15 PM) collide with the Wegmans shift and the 1 PM interview in DC. They are Track 3 material anyway. If a recording turns up on Discord over the weekend, run it through the same pipeline; otherwise their papers stand in.
- Zoom links come from the Luma RSVPs (calendar entries carry them). The host may or may not allow local recording; the capture plan does not depend on it.
- Talks are public events. The pipeline runs on our own machines; nothing leaves the LAN unless the slide-OCR fallback to Claude is used.

## 2. The chain

```
Zoom (live)  ──record──▶ source.mov/.mp4 ─┐
Discord recording ──download (yt-dlp or the attachment)──┤
                                          ▼
                     ffmpeg: audio.wav (16 kHz mono)   +   slides/NNNN.png at scene changes, index.tsv with mm:ss
                                          ▼
          parakeet-mlx (tdt 0.6b v3, English, fast) ──▶ transcript.srt/.json/.txt
          mlx-whisper large-v3-turbo on minutes 5 to 8 as a spot check (CHECK=1), or the whole talk (ASR=whisper)
                                          ▼
          srt_to_md.py ──▶ transcript.md  (paragraphs with [mm:ss], readable, greppable)
                                          ▼
          talk_notes.py ──▶ local model reads 8-minute windows ──▶ JSON items (quote, time, kind, gloss)
                            every quote string-checked against the transcript; failures flagged CHECK
                                          ▼
          notes/talks/<slug>.md: lines to use, open problems named, your "how it bears on our paper", citation stubs
```

Commands:

```bash
tools/talks.sh anwar talks/raw/anwar.mov                      # or a URL
.venv-tools/bin/python -m tools.talk_notes anwar --speaker "Usman Anwar" \
    --title "Steganography detection and CoT monitorability" --url "<Discord or Zoom link>" --day "October 23, 2026"
```

`make talk SLUG=anwar SRC=...` and `make notes SLUG=anwar SPEAKER=... TITLE=... URL=...` are the same thing.

## 3. Capturing the live talk (Friday, both talks)

Primary: the Screenshot toolbar. Press Shift-Command-5, choose "Record Selected Portion" around the Zoom window, open **Options** and turn on system audio (the option that records what the Mac plays; on macOS 26 it sits in that menu). Click Record ten minutes before 1:15 PM. Stop after the Q&A. The file lands on the Desktop as a .mov. Microphone off: we want the speaker, not the room.

Fallback A: Zoom's own "Record on this Computer" if the host has enabled it (the Record button is live). Zoom writes an .mp4 to ~/Documents/Zoom after the meeting ends.

Fallback B: if the toolbar has no system-audio option on this Mac, install BlackHole (`brew install blackhole-2ch`), make a Multi-Output Device in Audio MIDI Setup (speakers + BlackHole), set it as output, and record BlackHole as the input in QuickTime. Twenty minutes of setup; do it Thursday if the primary route shows no audio in a test.

Test on Thursday evening with any Zoom or YouTube video: record 30 seconds, run `tools/talks.sh test-live ~/Desktop/<file>.mov`, confirm words come out. The synthetic test passed 10/18, so the only unknown is the audio capture route.

Keep both talks in one recording if they run back to back, then split with `ffmpeg -ss <start> -to <end> -c copy` before transcribing, so each slug has its own clock starting at 0:00 and timestamps map to the recording the organisers post later. Note the wall-clock start time of each talk in `notes/log.md` so the Discord recording's clock can be reconciled.

## 4. Speech to text

- **parakeet-mlx** (NVIDIA Parakeet TDT 0.6B v3 through Apple's MLX) is the default: English, fast (third-party tests put it several times faster than Whisper on Apple Silicon), good punctuation, timestamps per segment. A one-hour talk should take a few minutes on the Air and less on the Studio.
- **mlx-whisper large-v3-turbo** is the accuracy check. `CHECK=1` transcribes minutes 5 to 8 with it and leaves `check.txt`; read the two side by side once per talk. If Parakeet is dropping technical terms (names of papers, "steganography", "monitorability"), rerun the whole talk with `ASR=whisper`.
- Neither diarises. Talks are one speaker plus a Q&A, so the note's "Time" column is enough; mark questions from the floor by hand if quoted.
- Known weak spots: speaker names and arXiv numbers come out wrong; numbers said aloud ("point three eight") may be written either way. The paper is the source for any number the speaker also published.

## 5. Slides

`talks.sh` writes a frame at every scene change above a 0.25 threshold and `slides/index.tsv` with the time of each. Expect 40 to 80 frames for an hour of slides; a talk shot on a webcam alone will produce noise, which is harmless. Slide text is read on demand, not in bulk: when a note's line points at a slide, run the frame through `tools.llm.complete("slide_ocr", ...)` on the local vision model (Haiku fallback) and paste the text under the line. Slides that state a number not in the paper are cited as "(slide at mm:ss)".

## 6. From transcript to a note

`talk_notes.py` asks the local model, per window, for 3 to 10 items: a verbatim quote of 25 words or fewer, its time, a kind (finding, number, open_problem, method, definition, aside), a one-sentence gloss. Then it:

1. drops duplicate quotes across the overlapping windows,
2. checks each quote is a substring of the normalised transcript, and flags any that is not with **CHECK**,
3. writes `notes/talks/<slug>.md` with the table, the open problems, an empty "How it bears on our paper" section for you, and two citation stubs.

The model is a finder, not a source. Nothing it writes goes into the report; the quote does, after you hear it. A window is about 6,000 tokens; a one-hour talk is 8 to 9 windows, a minute or two on the Studio.

Dry run with no model: `python -m tools.talk_notes <slug> --dry-run` writes the exact prompts to `talks/<slug>/prompts/` so the prompt can be read before the Studio is up.

## 7. Citing a talk in the report

- In the text: one sentence per talk at most, in Related Work or Discussion, as a direct quote with its time: Bagdasarian said the mixed-model case was "left for future work" (talk, Oct 23, 2026, 41:12).
- In References, the FAQ's rule is any consistent style, so: *Bagdasarian, E. and Nakamura, M. (2026). Colosseum: auditing collusion in multi-agent systems. Talk at the Apart Research AI Collusion Research Sprint, October 23, 2026. Recording: URL (Discord, posted after the event).* Until the recording URL exists, cite the Luma page and say "recording to be posted on the sprint Discord".
- Prefer the paper when the paper says it. The talk earns a citation only for something newer than the paper, or for the speaker naming a gap in their own words.
- The LLM Usage Statement gets one line: transcripts were machine-generated locally and every quote was checked against the recording.

## 8. Timings on Friday

| Time | Step | Who |
|---|---|---|
| 1:05 PM | start the recording, confirm the level meter moves | Arty |
| 1:15 to 3:15 | talks; handwritten notes on "unsolved" | Arty |
| 3:15 | stop, split, `tools/talks.sh` on both (about 10 min) | lab session |
| 3:25 | `talk_notes.py` on both (a few minutes on the Studio) | lab session |
| 3:35 to 3:55 | read both notes, pick the lines, write "how it bears" | Arty |
| 4:00 | G2 lock meeting uses them | both |

If the capture fails, G1 fails cleanly: the Related Work cites the papers and nothing is lost but one sentence.

## 9. Files

- `tools/talks.sh`, `tools/srt_to_md.py`, `tools/talk_notes.py`; the ASR packages live in `.venv-tools` (parakeet-mlx 0.5.3, mlx-whisper 0.4.3), and `yt-dlp` and `ffmpeg` are Homebrew installs.
- `talks/<slug>/` holds media and transcripts (media is gitignored); `notes/talks/<slug>.md` holds the note (tracked).
- Listed in `notes/PRIOR-WORK.md` as plumbing: it reads talks, it computes nothing about the market.
