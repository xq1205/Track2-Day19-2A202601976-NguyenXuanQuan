# Day 19 Lab — CHECKLIST (Vector Store + Feature Store)
**Nguyễn Xuân Quân · 2A202601976 · Track 2**

> Checklist này bám **100% vào rubric.md và README.md**. Không bịa thêm yêu cầu nào.
> Điểm: 100 pts core (NB1–NB4) + 50 pts nâng cao (NB5–NB8) + 20 pts bonus (optional).

---

## Phase 0 — Environment Setup

- [x] **0.1** Kiểm tra Python version (`python3 --version` phải là 3.10–3.14)
- [x] **0.2** `cd` vào thư mục lab: `cd ~/vinai/labs/Track2-Day19-2A202601976-NguyenXuanQuan`
- [x] **0.3** Chạy `bash setup-lite.sh` — chờ báo `All checks passed` (~60 giây)
- [x] **0.4** `.env` được tạo tự động từ `.env.example` (QDRANT_MODE=memory, EMBEDDING_BACKEND=fastembed)
- [x] **0.5** Corpus 1000 docs + 50 golden queries đã được seed (`data/` có file)
- [x] **0.6** Smoke test `scripts/verify_lite.py` pass (xanh)
- [x] **0.7** Activate venv: `source .venv/bin/activate`
- [x] **0.8** Chạy `make api &` — FastAPI lên port :8000
- [x] **0.9** Chạy `make lab` — JupyterLab lên port :8888

---

## Phase 1 — NB1: Embeddings & Index (20 pts)

**File:** `notebooks/01_embeddings_index.ipynb`

- [x] **1.1** Mở NB1 tại `http://localhost:8888/lab/tree/01_embeddings_index.ipynb`
- [x] **1.2** Chạy hết tất cả cells theo thứ tự (Run All)
- [x] **1.3** ✅ **[5 pts]** `client.count("lab19").count == 1000` — xác nhận đúng 1000 vectors đã index
- [x] **1.4** ✅ **[5 pts]** Top-5 results hiển thị cho keyword query (output cell §5)
- [x] **1.5** ✅ **[10 pts]** Paraphrase query (không có từ "cloud") vẫn trả về top-5 thuộc topic `cloud`
- [x] **1.6** Save notebook (giữ output cells)
- [ ] **1.7** Chụp screenshot: indexed 1000 vectors + top-5 paraphrase query → lưu vào `submission/screenshots/nb1_*.png`

---

## Phase 2 — NB2: Hybrid Search + RRF (25 pts)

**File:** `notebooks/02_hybrid_search_rrf.ipynb`

- [x] **2.1** Mở NB2 tại `http://localhost:8888/lab/tree/02_hybrid_search_rrf.ipynb`
- [x] **2.2** Implement `search_hybrid` theo đúng RRF formula: `score = 1/(k + rank)`, **rank 1-based**
- [x] **2.3** ✅ **[10 pts]** `search_hybrid` implemented đúng RRF formula
- [x] **2.4** Chạy evaluation Precision@10 trên 50 golden queries
- [x] **2.5** ✅ **[10 pts]** Bảng Avg Precision@10: `hybrid > keyword` VÀ `hybrid > semantic` (78.6% > 77.8% > 73.2%)
- [x] **2.6** ✅ **[5 pts]** Bảng slice theo query type: hybrid wins trên `mixed` (100%), vector wins `paraphrase`, BM25 wins `exact`
- [x] **2.7** Save notebook (giữ output cells)
- [x] **2.8** Chụp screenshot: bảng Precision@10 (3 modes) → lưu vào `submission/screenshots/nb2_*.png`

---

## Phase 3 — NB3: Search API + Latency Benchmark (25 pts)

**File:** `notebooks/03_search_api_benchmark.ipynb`

- [x] **3.1** Đảm bảo FastAPI đang chạy (`make api &`)
- [x] **3.2** Mở NB3 tại `http://localhost:8888/lab/tree/03_search_api_benchmark.ipynb`
- [x] **3.3** ✅ **[5 pts]** `/search?q=...&mode=...` trả về `SearchResponse` hợp lệ, có trường `latency_ms`
- [x] **3.4** Chạy 10 warmup queries trước khi đo latency (tránh cold-start P99 > 50ms)
- [x] **3.5** ✅ **[10 pts]** Bảng P50/P95/P99 latency cho 3 modes (kw/sem/hyb) được in ra
- [x] **3.6** ✅ **[10 pts]** Hybrid P99 server-side **3.4ms** (< 50ms threshold) PASS
- [x] **3.7** Save notebook (giữ output cells)
- [ ] **3.8** Chụp screenshot: API response sample + bảng latency → lưu vào `submission/screenshots/nb3_*.png`

---

## Phase 4 — NB4: Feast Feature Store (25 pts)

**File:** `notebooks/04_feast_feature_store.ipynb`

- [x] **4.1** Mở NB4 tại `http://localhost:8888/lab/tree/04_feast_feature_store.ipynb`
- [x] **4.2** Không cần xóa `registry.db` (feast apply đã idempotent)
- [x] **4.3** ✅ **[5 pts]** `feast apply` thành công — `feature-views list` hiện đủ 3 feature views
- [x] **4.4** ✅ **[5 pts]** `materialize-incremental` thành công — log hiện rows materialized vào online store
- [x] **4.5** ✅ **[5 pts]** `get_online_features()` trả về dict hợp lệ cho `user_id=u_001`
- [x] **4.6** ✅ **[5 pts]** 100-call online lookup P99 = 0.48ms (< 10ms = full credit)
- [x] **4.7** ✅ **[5 pts]** PIT join qua `get_historical_features()` trả về **3 rows × 4 features**
- [x] **4.8** Save notebook (giữ output cells)
- [ ] **4.9** Chụp screenshot: `feast apply` STDOUT + online lookup result + PIT join DF → lưu vào `submission/screenshots/nb4_*.png`

---

## Phase 5 — Validation & Benchmark (5 pts)

- [x] **5.1** Chạy `make test` — **41/41 tests PASS** (~13 giây)
- [x] **5.2** Chạy `make benchmark` — in ra bảng Precision@10 + P99 latency
- [x] **5.3** Chạy `make verify-lite` — 5-second smoke test **All checks passed**
- [x] **5.4** ✅ **[5 pts]** Reproducible từ `bash setup-lite.sh && make benchmark` trên máy sạch

---

## Phase 6 — Advanced Notebooks NB5–NB8 (50 pts)

> Bắt buộc NB1–NB4 xong trước. NB5–NB8 dùng lại index đã có, không phải embed lại.

### NB5: Filtered Search (10 pts)
**File:** `notebooks/05_filtered_search.ipynb`

- [x] **6.1** Mở NB5 và chạy hết cells
- [x] **6.2** ✅ **[5 pts]** Bảng recall theo độ chọn lọc: post-filter = 0.00 khi acme AND ≥2026 (3.8%), filtered-ANN giữ recall = 1.00
- [x] **6.3** ✅ **[5 pts]** Over-fetch ladder: `fetch_k` phải ≈ 50% corpus (500/1000) mới cứu được recall về 1.00
- [x] **6.4** Save notebook + chụp screenshot

### NB6: Agentic Retrieval (12 pts)
**File:** `notebooks/06_agent_retrieval.ipynb`

- [x] **6.5** Chạy `make gen-advanced` đã tạo data từ setup
- [x] **6.6** Mở NB6 và chạy hết cells
- [x] **6.7** ✅ **[5 pts]** Bảng 3 chiến lược: agentic recall=0.906 > single-shot 0.526; balance=0.93 > 0.08
- [x] **6.8** ✅ **[4 pts]** agentic+filter (0.823) thấp hơn agentic-no-filter (0.906) vì filter quá chặt loại bỏ kết quả đúng
- [x] **6.9** ✅ **[3 pts]** `build_context()` in ra features (Feast) lẫn `doc_ids`
- [x] **6.10** Save notebook + chụp screenshot

### NB7: Semantic Cache (12 pts)
**File:** `notebooks/07_semantic_cache.ipynb`

- [x] **6.11** Mở NB7 và chạy hết cells
- [x] **6.12** ✅ **[5 pts]** Bảng sweep threshold: có cả 2 cột — tiết kiệm VÀ trả lời sai
- [x] **6.13** ✅ **[4 pts]** Threshold hợp lý = 0.85 (0.75 sai 36% → NGUY HIỂM, không dùng được)
- [x] **6.14** ✅ **[3 pts]** Demo rò chéo tenant: GLOBEX đọc data ACME khi `namespaced=False`, MISS khi `True`
- [x] **6.15** Save notebook + chụp screenshot

### NB8: Feature Engineering (12 pts)
**File:** `notebooks/08_feature_engineering.ipynb`

- [x] **6.16** Data đã được gen từ setup (gen_spend.py)
- [x] **6.17** Mở NB8 và chạy hết cells
- [x] **6.18** ✅ **[4 pts]** Bảng leakage: target-naive gap = **0.477** > 0.30 trên `session_id`, in-fold ≈ -0.003 ≈ 0
- [x] **6.19** ✅ **[4 pts]** PIT vs latest join: 98.2% dòng rò, AUC chênh 0.120 (latest 0.715 vs PIT 0.595)
- [x] **6.20** ✅ **[4 pts]** ODFV: cùng user_000, hai `amount` → ratio 0.03 và 4.21 **khác nhau**
- [x] **6.21** Save notebook + chụp screenshot

### Validation Advanced
- [x] **6.22** ✅ **[4 pts]** `make test` xanh (41/41) + `make verify-lite` xanh (tính cho cả advanced)

---

## Phase 7 — Submission

- [x] **7.1** Điền `submission/REFLECTION.md` (≤ 200 chữ): mode nào wins trên query nào? Khi nào KHÔNG dùng hybrid?
- [x] **7.2** Kiểm tra `submission/screenshots/` có đủ ảnh: ≥ 1 ảnh mỗi notebook (NB1–NB4 bắt buộc)
- [x] **7.3** Chạy `make notebooks` để execute toàn bộ headless (kiểm tra output cells còn đủ)
- [x] **7.4** `git add -A`
- [x] **7.5** `git commit -m "Lab 19 submission — Nguyen Xuan Quan"`
- [ ] **7.6** Push lên public GitHub repo
- [ ] **7.7** Set repo **public** (grader không xem được repo private → 0 điểm)
- [ ] **7.8** Paste public GitHub URL vào ô submission Day 19 trên VinUni LMS

---

## Phase 8 — Bonus Challenge (optional, 20 pts)

> Không ảnh hưởng điểm core nếu bỏ qua. Xem `BONUS-CHALLENGE.md` để biết full brief.

- [ ] **8.1** ✅ **[3 pts]** `bonus/ARCHITECTURE.md` tồn tại, ≥ 600 chữ, có diagram kiến trúc
- [ ] **8.2** ✅ **[6 pts]** 3 architecture decisions với explicit tradeoff (X vs Y, tại sao chọn X)
- [ ] **8.3** ✅ **[2 pts]** Ít nhất 1 decision thể hiện nhận thức về Vietnamese context
- [ ] **8.4** ✅ **[2 pts]** Alternative bị reject được nêu rõ + lý do
- [ ] **8.5** ✅ **[4 pts]** `bonus/agent.py` chạy được (`HybridMemoryAgent.remember()` + `.recall()`)
- [ ] **8.6** ✅ **[3 pts]** `bonus/demo.py` exit 0, in ra 5 query outputs

---

## Score Tracker

| Phase | Pts Available | Pts Earned | Done? |
|-------|--------------|------------|-------|
| NB1 — Embeddings & Index | 20 | — | ☐ |
| NB2 — Hybrid Search RRF | 25 | — | ☐ |
| NB3 — Search API Benchmark | 25 | — | ☐ |
| NB4 — Feast Feature Store | 25 | — | ☐ |
| Reproducibility | 5 | — | ☐ |
| **Core Total** | **100** | **—** | ☐ |
| NB5 — Filtered Search | 10 | — | ☐ |
| NB6 — Agentic Retrieval | 12 | — | ☐ |
| NB7 — Semantic Cache | 12 | — | ☐ |
| NB8 — Feature Engineering | 12 | — | ☐ |
| Advanced Validation | 4 | — | ☐ |
| **Advanced Total** | **50** | **—** | ☐ |
| Bonus Challenge | 20 | — | ☐ |
| **GRAND TOTAL** | **170** | **—** | ☐ |
