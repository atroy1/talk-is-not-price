#!/usr/bin/env python3
"""Read the Qwen sellers' internal state, turn by turn, from finished runs. Runs on the Mac Studio (MLX).

    .venv-tools/bin/python -m tools.extract_activations runs/live/<tag> [more run folders]
        [--model ~/.lmstudio/models/local-sprint/Qwen3.5-9B-stock-MLX-4bit] [--layers 8,16,24,31] [--limit N]

For every seller turn it rebuilds what the model read (the prompt through the same chat template, thinking
off) followed by what it answered, runs one forward pass with the same weights that played the run, and keeps
two summaries per layer:
  last_prompt  the hidden state at the last prompt token, the moment before the model starts answering
  resp_mean    the mean hidden state over the answer's tokens
Output: runs/derived/acts/<tag>.npz (float16 arrays [turns, layers, 4096]) plus a meta list (seller, round, tokens).

Plumbing only: it records representations and computes no score. The probe that reads them is built in the sprint.
Caveat to state in Methods: the transcript stores the parsed reply re-serialised as JSON, so the answer tokens
are a faithful but not byte-identical copy of what was generated.
"""
import argparse
import glob
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TURN = re.compile(r"\n(?=## (?:Prompt|Response): Round \d+ - )")
HEAD = re.compile(r"## (Prompt|Response): Round (\d+) - [^\n]*\n")
JSON_BLOCK = re.compile(r"````json\n(.*?)\n````", re.S)
DEFAULT_MODEL = os.path.expanduser("~/.lmstudio/models/local-sprint/Qwen3.5-9B-stock-MLX-4bit")
WEIGHTS = {  # queue model id -> the MLX weights that served it (same conversion command for both)
    "local/qwen35-9b-stock": DEFAULT_MODEL,
    "local/qwen35-9b-abl": os.path.expanduser("~/.lmstudio/models/local-sprint/Qwen3.5-9B-abliterated-MLX-4bit"),
    "local/qwen35-35b-stock": os.path.expanduser("~/.lmstudio/models/local-sprint/Qwen3.5-35B-A3B-stock-MLX-4bit"),
    "local/qwen35-35b-abl": os.path.expanduser("~/.lmstudio/models/local-sprint/Qwen3.5-35B-A3B-abliterated-MLX-4bit"),
}


def seller_turns(run_dir):
    """Yield (seller, round, prompt_text, response_text) from the starter's Seller*.md transcripts."""
    for f in sorted(glob.glob(os.path.join(run_dir, "Seller*.md"))):
        seller = Path(f).stem
        prompts, responses = {}, {}
        for blk in TURN.split("\n" + open(f, encoding="utf-8").read()):
            m = HEAD.match(blk.lstrip("\n"))
            if not m:
                continue
            body = blk.lstrip("\n")[m.end():]
            if m.group(1) == "Prompt":
                prompts[int(m.group(2))] = body.strip()
            else:
                j = JSON_BLOCK.search(body)
                responses[int(m.group(2))] = (j.group(1) if j else body).strip()
        for rnd in sorted(prompts):
            if rnd in responses:
                yield seller, rnd, prompts[rnd], responses[rnd]


def load_model(path):
    import mlx.nn as nn
    from mlx_lm import load
    model, tok = load(path)
    inner = model
    for attr in ("language_model", "model"):
        if hasattr(inner, attr):
            inner = getattr(inner, attr)
    if hasattr(inner, "model"):
        inner = inner.model
    captured = {}

    class Tap(nn.Module):
        def __init__(self, layer, idx):
            super().__init__()
            self.layer, self.idx = layer, idx
            self.is_linear = getattr(layer, "is_linear", False)  # Qwen3.5 mixes linear and full attention

        def __call__(self, x, *a, **k):
            out = self.layer(x, *a, **k)
            captured[self.idx] = out[0] if isinstance(out, tuple) else out
            return out

    for i in range(len(inner.layers)):
        inner.layers[i] = Tap(inner.layers[i], i)
    return model, tok, captured, len(inner.layers)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", help="run folders (runs/live/<tag>) or their run/ subfolders")
    ap.add_argument("--model", default="auto", help="MLX weights that played the run; auto reads the run's spec.json")
    ap.add_argument("--layers", default="auto", help="comma list, or auto: a quarter, half, three quarters and the last layer")
    ap.add_argument("--limit", type=int, default=0, help="first N turns per run only (for a quick check)")
    a = ap.parse_args()
    import mlx.core as mx
    import numpy as np

    out_dir = ROOT / "runs" / "derived" / "acts"
    out_dir.mkdir(parents=True, exist_ok=True)
    loaded = {}
    for run in a.runs:
        weights = a.model
        if weights == "auto":
            spec_path = os.path.join(run.rstrip("/").removesuffix("/run"), "spec.json")
            seller = json.load(open(spec_path))["seller_model"] if os.path.exists(spec_path) else ""
            weights = WEIGHTS.get(seller, DEFAULT_MODEL)
        weights = os.path.expanduser(weights)
        if weights not in loaded:
            loaded.clear()
            loaded[weights] = load_model(weights)
        model, tok, captured, n_layers = loaded[weights]
        layers = ([n_layers // 4, n_layers // 2, 3 * n_layers // 4, n_layers - 1] if a.layers == "auto"
                  else [int(x) for x in a.layers.split(",") if int(x) < n_layers])
        run_dir = run if os.path.exists(os.path.join(run, "auction_results.md")) else os.path.join(run, "run")
        tag = Path(run.rstrip("/")).name if not run.rstrip("/").endswith("/run") else Path(run.rstrip("/")).parent.name
        last_prompt, resp_mean, meta = [], [], []
        t0 = time.time()
        for i, (seller, rnd, prompt, response) in enumerate(seller_turns(run_dir)):
            if a.limit and i >= a.limit:
                break
            try:
                ptxt = tok.apply_chat_template([{"role": "user", "content": prompt}], add_generation_prompt=True,
                                               tokenize=False, enable_thinking=False)
            except TypeError:
                ptxt = tok.apply_chat_template([{"role": "user", "content": prompt}], add_generation_prompt=True, tokenize=False)
            p_ids, r_ids = tok.encode(ptxt), tok.encode(response)
            captured.clear()
            mx.eval(model(mx.array([p_ids + r_ids])), *captured.values())
            n_p = len(p_ids)
            last_prompt.append(np.stack([np.array(captured[L][0, n_p - 1].astype(mx.float32)) for L in layers]).astype(np.float16))
            resp_mean.append(np.stack([np.array(captured[L][0, n_p:].astype(mx.float32).mean(axis=0)) for L in layers]).astype(np.float16))
            meta.append({"seller": seller, "round": rnd, "prompt_tokens": n_p, "response_tokens": len(r_ids)})
        dest = out_dir / f"{tag}.npz"
        np.savez_compressed(dest, last_prompt=np.stack(last_prompt), resp_mean=np.stack(resp_mean),
                            layers=np.array(layers), meta=np.array(json.dumps(meta)), model=np.array(weights))
        print(f"{tag}: {len(meta)} seller turns, layers {layers}, {time.time() - t0:.0f}s -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
