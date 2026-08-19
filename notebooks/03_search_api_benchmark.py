# ---
# jupyter:
#   jupytext:
#     formats: py:percent
# ---

# %% [markdown]
# # NB3 — FastAPI `/search` Endpoint + Latency Benchmark
#
# **Stack:** FastAPI + Starlette TestClient + Searcher từ `app/search.py`.
# Maps to slide §7 (Production Patterns) + deliverable bullets 1, 4.
#
# > Mục tiêu: bọc `Searcher` thành REST API, đo P50/P95/P99 latency, đảm bảo
# > P99 < 50 ms cho hybrid mode (rubric threshold).

# %%
import _setup  # noqa: F401
import statistics
import time
import json
from pathlib import Path

# %% [markdown]
# ## 1. Khởi động API server (in-process TestClient)
#
# Dùng Starlette TestClient để test FastAPI app in-process. Searcher được build
# 1 lần rồi tái dùng toàn bộ benchmark — cùng behavior như production.

# %%
ROOT = Path(_setup.__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT))

from starlette.testclient import TestClient
from app.main import app

print("Building Searcher (embeds 1000 docs, may take ~5 min on CPU)...")
t_start = time.perf_counter()
# TestClient's context manager triggers lifespan startup (Searcher.from_corpus)
client = TestClient(app)
client.__enter__()
build_time = time.perf_counter() - t_start
print(f"Searcher ready in {build_time:.1f}s")

r = client.get("/healthz")
print("healthz:", r.json())

# %% [markdown]
# ## 2. Single query — kiểm tra response shape

# %%
r = client.get("/search", params={"q": "cloud computing tự động mở rộng", "mode": "hybrid"})
r.raise_for_status()
body = r.json()
print(f"latency_ms: {body['latency_ms']:.1f}")
print(f"top-3 hits:")
for h in body["hits"][:3]:
    print(f"  {h['doc_id']:>14}  score={h['score']:.4f}  {h['title']}")

# %% [markdown]
# ## 3. Latency benchmark (100 queries × 3 modes)
#
# 50 golden queries × 2 reps = 100 calls/mode. Latency từ `body["latency_ms"]`
# (server-side measurement, không tính TestClient overhead).

# %%
DATA = ROOT / "data"
golden = [json.loads(l) for l in (DATA / "golden_set.jsonl").open(encoding="utf-8")]

# Warmup: 10 queries per mode per README troubleshooting tip
# "Bình thường ở cold start. Chạy 10 query warmup trước rồi đo lại."
print("Running warmup (10 queries each mode)...")
for mode in ("keyword", "semantic", "hybrid"):
    for q in golden[:10]:
        client.get("/search", params={"q": q["query"], "mode": mode})
print("Warmup done.")


def percentile(values: list[float], p: float) -> float:
    n = len(values)
    if n == 0:
        return 0.0
    return sorted(values)[min(int(n * p), n - 1)]


def benchmark_mode(mode: str, reps: int = 2) -> dict[str, float]:
    server_latencies: list[float] = []
    wall_latencies: list[float] = []
    for _ in range(reps):
        for q in golden:
            t0 = time.perf_counter()
            r = client.get("/search", params={"q": q["query"], "mode": mode})
            wall_latencies.append((time.perf_counter() - t0) * 1000)
            server_latencies.append(r.json()["latency_ms"])
    return {
        "p50_server": percentile(server_latencies, 0.50),
        "p95_server": percentile(server_latencies, 0.95),
        "p99_server": percentile(server_latencies, 0.99),
        "p99_wall":   percentile(wall_latencies, 0.99),
    }


print(f"  {'mode':10}  {'P50':>7}  {'P95':>7}  {'P99':>7}  {'P99(wall)':>9}")
results = {}
for mode in ("keyword", "semantic", "hybrid"):
    res = benchmark_mode(mode)
    results[mode] = res
    print(f"  {mode:10}  {res['p50_server']:>5.1f}ms  {res['p95_server']:>5.1f}ms  "
          f"{res['p99_server']:>5.1f}ms  {res['p99_wall']:>7.1f}ms")

# %% [markdown]
# ## 4. Rubric assertion — hybrid P99 server-side < 50ms

# %%
hybrid_p99 = results["hybrid"]["p99_server"]
print(f"Hybrid P99 server-side: {hybrid_p99:.1f}ms")
if hybrid_p99 < 50:
    print(f"PASS — hybrid P99 < 50ms ({hybrid_p99:.1f}ms)")
else:
    print(f"WARN — hybrid P99 >= 50ms ({hybrid_p99:.1f}ms)")
    print("  Possible causes: cold cache, fastembed model not warm yet")

# %% [markdown]
# ## 5. Cleanup

# %%
client.__exit__(None, None, None)
print("API TestClient closed")

# %% [markdown]
# ## Deliverable evidence
#
# 1. Output cell 2: healthz ready + single hybrid query response with `top-3 hits`.
# 2. Output cell 3: latency table P50/P95/P99 for keyword/semantic/hybrid.
# 3. Output cell 4: hybrid P99 < 50ms PASS.
#
# ---
#
# ## Vibe-coding callout
#
# **Delegate freely:** FastAPI scaffolding, Pydantic response model, lifespan
# handler. AI generates this perfectly from spec.
#
# **Think hard yourself:** what to measure — server-side vs wall-clock, P99 vs P50.
# These are judgement decisions; don't ask AI to pick the metric.
