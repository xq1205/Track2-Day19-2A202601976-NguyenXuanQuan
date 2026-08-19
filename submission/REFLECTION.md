# Reflection — Lab 19

**Tên:** Nguyễn Xuân Quân
**Cohort:** A20-2A202601976
**Path đã chạy:** lite (fastembed + Qdrant in-memory + SQLite Feast)

---

## Câu hỏi (≤ 200 chữ)

Trên golden set 50 queries, mỗi mode thắng ở loại query khác nhau: **BM25 (keyword)** thắng trên `exact` queries (96.7%) vì corpus có verbatim term match — đây là điểm mạnh của TF-IDF; **Vector (semantic)** thắng nhỉnh hơn BM25 trên `mixed` (98.5% vs 97%) nhờ hiểu nghĩa, nhưng bị yếu trên `paraphrase` (24%) vì model `bge-small-en-v1.5` là English-focused, kém hiệu quả với tiếng Việt; **Hybrid (RRF k=60)** thắng tổng thể (78.6%) và **thắng rõ trên `mixed`** (100%), đây là pattern production-relevant nhất.

**Khi không dùng hybrid:** (1) Corpus thuần keyword-based (văn bản pháp luật, mã SKU) → BM25 đủ mạnh, hybrid thêm overhead không cần thiết; (2) Low-latency strict SLA < 5ms → tránh double-retrieval; (3) Corpus đơn ngôn ngữ đơn style → pure semantic với model multilingual đủ; (4) Budget hạn chế (chi phí embedding inference).

---

## Điều ngạc nhiên nhất khi làm lab này

Embedding model choice (`bge-small-en` vs `bge-m3`) ảnh hưởng dramaticaly đến recall trên tiếng Việt paraphrase — 24% vs dự đoán ~60%+ với multilingual model. Query embedding caching với LRU giảm hybrid P99 từ 86ms → 3.4ms.

---

## Bonus challenge

- [ ] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: _không có_
