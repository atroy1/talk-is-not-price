#!/usr/bin/env bash
# Speech to a timestamped transcript, plus slide frames. Method in docs/TALKS-PIPELINE.md.
#   tools/talks.sh <slug> <source>      source = URL (yt-dlp) or a local media file (.mp4 .mov .m4a .wav .aiff)
#   ASR=whisper tools/talks.sh ...      use mlx-whisper large-v3-turbo instead of parakeet (slower, 99 languages)
#   CHECK=1 tools/talks.sh ...          also run whisper on minutes 5 to 8 and leave check.txt beside the transcript
# Output: talks/<slug>/ source.*  audio.wav  transcript.{srt,txt,vtt,json}  transcript.md  slides/NNNN.png  slides/index.tsv
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd); PY="$ROOT/.venv-tools/bin"
slug=${1:?usage: talks.sh <slug> <source>}; src=${2:?usage: talks.sh <slug> <source>}
out="$ROOT/talks/$slug"; mkdir -p "$out/slides"
log(){ printf '%s %s\n' "$(date +%H:%M:%S)" "$*"; }

if [[ $src =~ ^https?:// ]]; then
  log "download $src"
  yt-dlp -q --no-playlist -f "bv*[height<=720]+ba/b" -o "$out/source.%(ext)s" "$src"
  echo "$src" > "$out/source.url"
  src=$(ls "$out"/source.* | grep -v '\.url$' | head -1)
else
  ext="${src##*.}"
  if [[ ! -e "$out/source.$ext" || ! "$src" -ef "$out/source.$ext" ]]; then cp "$src" "$out/source.$ext"; fi
  src="$out/source.$ext"
fi

log "audio -> 16 kHz mono"
ffmpeg -y -loglevel error -i "$src" -vn -ac 1 -ar 16000 "$out/audio.wav"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out/audio.wav")
log "duration ${dur%.*} s"

if [[ ${ASR:-parakeet} == whisper ]]; then
  log "asr: mlx-whisper large-v3-turbo"
  "$PY/mlx_whisper" "$out/audio.wav" --model mlx-community/whisper-large-v3-turbo \
     --output-dir "$out" --output-name transcript --output-format all > "$out/asr.log" 2>&1
else
  log "asr: parakeet-mlx (tdt 0.6b v3)"
  "$PY/parakeet-mlx" "$out/audio.wav" --output-dir "$out" --output-template transcript --output-format all > "$out/asr.log" 2>&1
fi

if [[ ${CHECK:-0} == 1 ]]; then
  log "whisper spot check, 5:00 to 8:00"
  ffmpeg -y -loglevel error -ss 300 -t 180 -i "$out/audio.wav" "$out/check.wav"
  "$PY/mlx_whisper" "$out/check.wav" --model mlx-community/whisper-large-v3-turbo \
     --output-dir "$out" --output-name check --output-format txt >> "$out/asr.log" 2>&1
fi

if ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of csv=p=0 "$src" | grep -q video; then
  log "slide frames at scene changes"
  ffmpeg -y -loglevel info -i "$src" -vf "select='gt(scene,0.25)',showinfo" -fps_mode vfr "$out/slides/%04d.png" 2> "$out/slides/showinfo.log" || true
  grep -o 'pts_time:[0-9.]*' "$out/slides/showinfo.log" | cut -d: -f2 \
    | awk '{printf "%04d.png\t%d:%02d\t%s\n", NR, int($1/60), int($1%60), $1}' > "$out/slides/index.tsv"
  log "$(wc -l < "$out/slides/index.tsv" | tr -d ' ') slide frames"
fi

log "transcript.md"
"$PY/python" "$ROOT/tools/srt_to_md.py" "$out/transcript.srt" "$slug" > "$out/transcript.md"
log "done: $out   next: .venv-tools/bin/python -m tools.talk_notes $slug"
