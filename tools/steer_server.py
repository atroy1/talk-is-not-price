#!/usr/bin/env python3
"""A steered copy of a local Qwen model, behind the same /v1/completions API the starter already uses.

    .venv-tools/bin/python -m tools.steer_server --vector runs/derived/steer/collusion_L20.npy --layer 20 \
        --alpha 4.0 [--model ~/.lmstudio/models/local-sprint/Qwen3.5-35B-A3B-stock-MLX-4bit] [--port 8085]

While it generates, it adds alpha * v to the output of one decoder layer at every position. v is a direction in
that layer's hidden space (unit length; derived in the sprint from activations, e.g. mean collusive turn minus
mean compete turn). alpha = 0 reproduces the unsteered model exactly; a dose-response sweep runs one server per
alpha, or restarts it. Requests are handled one at a time and seeded, so steered runs replay exactly too.

Reserve plumbing, built 2026-10-22: no direction exists before the sprint (`--vector random` is for the
mechanism check only). The starter reaches it as "local/qwen35-35b-steer" (config/local-models.json).
"""
import argparse
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import mlx.core as mx
import mlx.nn as nn
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

DEFAULT_MODEL = os.path.expanduser("~/.lmstudio/models/local-sprint/Qwen3.5-35B-A3B-stock-MLX-4bit")


class Steer(nn.Module):
    def __init__(self, layer, vec, alpha):
        super().__init__()
        self.layer, self.vec, self.alpha = layer, vec, alpha
        self.is_linear = getattr(layer, "is_linear", False)  # Qwen3.5 mixes linear and full attention

    def __call__(self, x, *a, **k):
        out = self.layer(x, *a, **k)
        if self.alpha == 0.0:
            return out
        if isinstance(out, tuple):
            return (out[0] + self.alpha * self.vec.astype(out[0].dtype),) + tuple(out[1:])
        return out + self.alpha * self.vec.astype(out.dtype)


def decoder(model):
    inner = model
    for attr in ("language_model", "model"):
        if hasattr(inner, attr):
            inner = getattr(inner, attr)
    return inner.model if hasattr(inner, "model") else inner


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--vector", required=True, help=".npy unit vector, or 'random' for the mechanism check")
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--alpha", type=float, default=0.0)
    ap.add_argument("--port", type=int, default=8085)
    ap.add_argument("--host", default="0.0.0.0")
    a = ap.parse_args()

    model, tok = load(os.path.expanduser(a.model))
    layers = decoder(model).layers
    hidden = None
    if a.vector == "random":
        mx.random.seed(0)
        probe = layers[a.layer]
        hidden = model.args.hidden_size if hasattr(model, "args") and hasattr(model.args, "hidden_size") else None
        if hidden is None:
            hidden = decoder(model).embed_tokens.weight.shape[-1] if hasattr(decoder(model).embed_tokens, "weight") else 2048
        v = mx.random.normal((hidden,))
    else:
        import numpy as np
        v = mx.array(np.load(a.vector).astype("float32"))
    v = v / mx.linalg.norm(v)
    layers[a.layer] = Steer(layers[a.layer], v, a.alpha)
    lock = threading.Lock()
    info = {"model": a.model, "layer": a.layer, "alpha": a.alpha, "vector": a.vector, "dims": int(v.shape[0])}
    print("steer server ready:", json.dumps(info), flush=True)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, code, obj):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self._send(200, {"object": "list", "data": [{"id": "default_model", "object": "model", "steering": info}]})

        def do_POST(self):
            if not self.path.endswith("/completions"):
                return self._send(404, {"error": "only /v1/completions"})
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            prompt, stops = req.get("prompt", ""), req.get("stop") or []
            stops = [stops] if isinstance(stops, str) else stops
            with lock:  # one at a time, like the seeded mlx_lm server
                if req.get("seed") is not None:
                    mx.random.seed(int(req["seed"]))
                sampler = make_sampler(temp=float(req.get("temperature", 0.7)), top_p=float(req.get("top_p", 1.0)))
                text, n_out, finish = "", 0, "length"
                n_in = len(tok.encode(prompt))
                for resp in stream_generate(model, tok, prompt, max_tokens=int(req.get("max_tokens", 4000)), sampler=sampler):
                    text += resp.text
                    n_out += 1
                    hit = next((s for s in stops if s in text), None)
                    if hit:
                        text, finish = text.split(hit, 1)[0], "stop"
                        break
                    if getattr(resp, "finish_reason", None) == "stop":
                        finish = "stop"
                        break
            self._send(200, {"id": f"steer-{time.time():.0f}", "object": "text_completion", "model": "default_model",
                             "choices": [{"index": 0, "text": text, "finish_reason": finish}],
                             "usage": {"prompt_tokens": n_in, "completion_tokens": n_out, "total_tokens": n_in + n_out},
                             "steering": info})

    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
