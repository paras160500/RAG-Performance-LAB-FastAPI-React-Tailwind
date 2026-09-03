<div align="center">

# ⚡ RAG Performance LAB

### Brute-force NumPy vs. FAISS `IndexFlatIP` — the same query, two engines, millisecond-level receipts.



[![Live Demo](https://img.shields.io/badge/🚀_LIVE_DEMO-Run_a_benchmark_now-6366f1?style=for-the-badge)](https://rag-performance-lab-fastapi-react-0gdq.onrender.com)
[![Backend API](https://img.shields.io/badge/⚙️_API-Online-10b981?style=for-the-badge)](https://rag-performance-lab-fastapi-react.onrender.com)
[![Repo](https://img.shields.io/badge/📦_Source-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/paras160500/RAG-Performance-LAB-FastAPI-React-Tailwind)

![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_19-61DAFB?style=flat-square&logo=react&logoColor=black)
![Tailwind](https://img.shields.io/badge/TailwindCSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-4B32C3?style=flat-square&logo=meta&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white)




</div>

### 🔗 Live Preview

| | Link | Notes |
|---|---|---|
| 🚀 **App (Frontend)** | [rag-performance-lab-fastapi-react-0gdq.onrender.com](https://rag-performance-lab-fastapi-react-0gdq.onrender.com) | No signup — click **"Run Benchmark"** to fire a live query |
| ⚙️ **API (Backend)** | [rag-performance-lab-fastapi-react.onrender.com](https://rag-performance-lab-fastapi-react.onrender.com) | FastAPI service the frontend talks to; `/api/health` for a quick liveness check |
| 📦 **Source Code** | [github.com/paras160500/RAG-Performance-LAB-FastAPI-React-Tailwind](https://github.com/paras160500/RAG-Performance-LAB-FastAPI-React-Tailwind) | Full backend + frontend source |

> Every RAG engineer eventually asks: *"At what point does my brute-force cosine similarity loop stop being good enough?"*
> This lab answers it empirically — with seeded, reproducible 1536‑dimensional vectors (`text-embedding-3-small` dimensionality) — instead of by folklore.

<div align="center">



</div>

---

## 📖 Contents

- [What it does](#-what-it-does)
- [The race, visualized](#-the-race-visualized)
- [Architecture](#️-architecture)
- [Benchmark sequence](#-benchmark-sequence)
- [Speed vs. accuracy trade-off](#-speed-vs-accuracy-trade-off)
- [Tech stack](#️-tech-stack)
- [Sample output](#-sample-output)
- [Repository layout](#-repository-layout)
- [Run it locally](#️-run-it-locally)
- [Roadmap](#️-roadmap)
- [References & credits](#-references--credits)

---

## 🔍 What it does

Every RAG engineer eventually asks: *"At what point does my brute-force cosine similarity loop stop being good enough?"*

This lab answers it empirically instead of by folklore. It generates reproducible, seeded **1536-dimensional embeddings** (the same dimensionality as `text-embedding-3-small`), then races two retrieval strategies against each other on identical queries:

| | Strategy | Guarantee |
|---|---|---|
| 🐢 | **NumPy** — vectorized cosine similarity (`@` matmul) against the full matrix | Exact, always correct, gets slower as the corpus grows |
| 🚀 | **FAISS** `IndexFlatIP` — inner-product search on unit-normalized vectors | Near-identical accuracy, built for scale via SIMD & optimized memory access |

Every run is logged to Supabase, so you can watch the speedup trend accumulate across sessions instead of trusting a single lucky measurement.

---

## 🏁 The race, visualized

<img src="./assets/latency-chart.svg" width="100%" alt="Illustrative latency comparison chart: NumPy latency rises steeply with corpus size while FAISS stays flat"/>

The bigger the haystack, the more this gap matters — NumPy pays for every extra vector, FAISS barely notices.

---

## 🏗️ Architecture

Decoupled by design: a React SPA that only speaks HTTP to a FastAPI service, which pre-loads both engines into memory at startup via a lifespan context manager — no cold-start tax on the first request.

```mermaid
graph TD
    classDef frontend fill:#6366f1,stroke:#4338ca,color:#fff,stroke-width:2px
    classDef backend fill:#0ea5e9,stroke:#0369a1,color:#fff,stroke-width:2px
    classDef storage fill:#f59e0b,stroke:#b45309,color:#fff,stroke-width:2px
    classDef engine fill:#1e1b4b,stroke:#818cf8,color:#fff,stroke-width:2px,stroke-dasharray: 3 2

    subgraph Frontend["🖥️ React + Tailwind UI"]
        Dashboard[Dashboard Component]
        VectorGen[Vector Generator Util]
        APIClient[Axios API Client]
    end

    subgraph Backend["⚙️ FastAPI Server"]
        Main[main.py — lifespan startup]
        Router[API Routers]
        BenchSvc[Benchmark Service]
        RetSvc[Retrieval Service]
        NumPyE["🐢 NumPy Engine"]
        FAISSE["🚀 FAISS Engine"]
    end

    subgraph Storage["💾 Data Layer"]
        Embeddings[("embeddings_10k_1536.npy")]
        Index[("faiss_10k_1536.index")]
        Supabase[("Supabase · Postgres")]
    end

    Dashboard --> VectorGen --> APIClient
    APIClient -- "POST /api/benchmark/run" --> Router
    Router --> BenchSvc --> RetSvc
    RetSvc --> NumPyE
    RetSvc --> FAISSE
    NumPyE --> Embeddings
    FAISSE --> Index
    BenchSvc -- "log run + speedup" --> Supabase

    class Dashboard,VectorGen,APIClient frontend
    class Main,Router,BenchSvc,RetSvc backend
    class NumPyE,FAISSE engine
    class Embeddings,Index,Supabase storage
```

---

## 🎬 Benchmark sequence

Same seeded query vector, dispatched to both engines back-to-back, so the comparison is never apples-to-oranges.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as 🖥️ Frontend
    participant API as ⚙️ FastAPI
    participant NP as 🐢 NumPy
    participant FS as 🚀 FAISS
    participant DB as 💾 Supabase

    User->>UI: Click "Run Benchmark"
    UI->>UI: Generate seeded query vector
    UI->>API: POST /api/benchmark/run
    par Exact search
        API->>NP: Cosine similarity (full matmul)
        NP-->>API: Top-K results + latency
    and Approximate search
        API->>FS: IndexFlatIP search
        FS-->>API: Top-K results + latency
    end
    API->>API: Compute speedup = t(NumPy) / t(FAISS)
    API->>DB: Persist query + latencies + speedup
    DB-->>API: ack
    API-->>UI: Results payload
    UI-->>User: 📊 Render charts + speedup badge
```

---

## 🎯 Speed vs. accuracy trade-off

```mermaid
quadrantChart
    title Where each engine lands
    x-axis Slower --> Faster
    y-axis Approximate --> Exact
    quadrant-1 Best of both
    quadrant-2 Precise, doesn't scale
    quadrant-3 Avoid
    quadrant-4 Fast, slightly approximate
    NumPy (exact): [0.22, 0.95]
    FAISS (IndexFlatIP): [0.88, 0.9]
```

FAISS's `IndexFlatIP` is a rare case where you barely give up accuracy for a huge speed win — normalized inner product *is* cosine similarity, so there's no approximation error from the math itself, only from the search structure.

---

## 🛠️ Tech stack

| Layer | Stack |
|---|---|
| 🎨 Frontend | React 19 · Vite · Tailwind CSS · Axios · Lucide Icons |
| ⚙️ Backend | FastAPI · Python 3.12 · Uvicorn (lifespan-managed startup) |
| 🔎 Retrieval | FAISS `IndexFlatIP` · NumPy vectorized cosine similarity |
| 💾 Persistence | Supabase (Postgres) |
| ☁️ Deployment | Render — separate web service (API) + static site (UI) |

---

## 💻 Sample output

What a single benchmark run returns from the API:

```json
{
  "query_id": "run_8f3a1c",
  "corpus_size": 10000,
  "dimensions": 1536,
  "results": {
    "numpy": { "latency_ms": 42.7, "top_k": 5 },
    "faiss": { "latency_ms": 1.3, "top_k": 5 }
  },
  "speedup": "32.8x",
  "logged_to_supabase": true
}
```

---

## 📂 Repository layout

```
.
├── backend
│   ├── app
│   │   ├── api            # FastAPI route definitions
│   │   ├── core           # Configuration & security
│   │   ├── db             # Supabase client integration
│   │   ├── retrieval      # FAISS & NumPy engine implementations
│   │   ├── schemas        # Pydantic models for validation
│   │   └── services       # Business logic & benchmarking
│   └── data               # Vector embeddings & FAISS indexes
├── frontend
│   ├── src
│   │   ├── components     # Reusable UI components
│   │   ├── pages          # Dashboard & view logic
│   │   ├── services       # API communication layer
│   │   └── utils          # Vector generation & math helpers
│   └── public             # Static assets
└── .gitignore
```

---

## ⚙️ Run it locally

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
# add Supabase credentials to .env
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
# set VITE_API_URL in .env
npm run dev
```

> 🔑 You'll need a free [Supabase](https://supabase.com) project, plus the pre-generated `embeddings_10k_1536.npy` and `faiss_10k_1536.index` files under `backend/data`.

---

## 🗺️ Roadmap

```mermaid
timeline
    title Where the lab is headed
    section Shipped
        NumPy exact engine : done
        FAISS IndexFlatIP : done
        Live benchmark dashboard : done
        Supabase persistence : done
    section In progress
        HNSW & IVF indexes : planned
        Configurable corpus sizes (1K–1M) : planned
    section On the horizon
        Recall@K accuracy metrics : idea
        CSV / JSON export of history : idea
```

---

## 📝 References & credits

1. [GitHub Repository](https://github.com/paras160500/RAG-Performance-LAB-FastAPI-React-Tailwind)
2. [FastAPI Documentation](https://fastapi.tiangolo.com/)
3. [FAISS Documentation](https://github.com/facebookresearch/faiss)
4. [Supabase Documentation](https://supabase.com/docs)

<div align="center">

---

**Built by [Paras Patel](https://github.com/paras160500)** · assisted by Manus AI

⭐ **Star the repo** if the turtle made you smile.

</div>
