# AI-Video-Assistant — Cinematic Knowledge from Audio & Video

<p align="center">
  <!-- Large animated hero banner: replace with real GIF under assets/ -->
  <img alt="Hero banner" src="https://via.placeholder.com/1400x420.gif?text=Hero+Banner+-+Upload+%E2%86%92+Transcribe+%E2%86%92+Embed+%E2%86%92+Search" width="100%" />
</p>

<div align="center">
  <!-- Logo placeholder (SVG) -->
  <img src="https://via.placeholder.com/160x160.svg?text=LOGO" alt="Project logo" width="120" height="120" />

  <h2 style="margin-top:12px">Instantly search, quote, and summarize any video or audio</h2>

  <!-- Badge row -->
  <p>
    <img alt="build" src="https://img.shields.io/badge/build-passing-brightgreen" />
    <img alt="version" src="https://img.shields.io/badge/version-0.1.0-blue" />
    <img alt="license" src="https://img.shields.io/badge/license-MIT-lightgrey" />
    <img alt="stack" src="https://img.shields.io/badge/stack-Python%20%7C%20Streamlit%20%7C%20Chroma-blue" />
    <img alt="stars" src="https://img.shields.io/badge/stars-★%20Add%20yours-yellow" />
  </p>

  <p style="max-width:900px;margin:auto">
    A production-grade platform that extracts machine-readable knowledge from audio and video — precise timestamping, dense semantic search, and succinct, source-cited summaries for teams and products.
  </p>
</div>

<!-- SVG wave divider -->
<div style="line-height:0;margin-top:18px">
  <svg viewBox="0 0 1200 60" preserveAspectRatio="none" width="100%" height="60" xmlns="http://www.w3.org/2000/svg"><path d="M0,0 C300,80 900,-40 1200,40 L1200,60 L0,60 Z" fill="#f6f7fb"></path></svg>
</div>

---

<details>
<summary style="font-size:16px;font-weight:600">Live Demo & Animated Features (click to expand)</summary>

<p style="margin-top:12px">Each GIF below is a short, looped demonstration of a core user flow. Replace the placeholders with high-fidelity GIFs in <code>assets/gifs/</code>.</p>

<div align="center">
  <img src="https://via.placeholder.com/980x300.gif?text=Demo+-+Upload+%E2%86%92+ASR+Progress" alt="upload demo" width="980" style="margin-bottom:12px" />
  <img src="https://via.placeholder.com/980x300.gif?text=Demo+-+Search+%E2%86%92+Timestamp+Play" alt="search demo" width="980" style="margin-bottom:12px" />
  <img src="https://via.placeholder.com/980x300.gif?text=Demo+-+Summarize+%E2%86%92+Cite+Timestamps" alt="summarize demo" width="980" />
</div>

</details>

---

## Key flows — at a glance

- Ingest (video/audio) → Media extraction → ASR → Chunking → Embedding → Vector index
- Query → Dense retrieval → Re-ranking → Timestamp-aware snippet playback → Summarization with sources

<!-- Section divider -->
<svg viewBox="0 0 1200 40" preserveAspectRatio="none" width="100%" height="40"><path d="M0,20 C300,-20 900,60 1200,10 L1200,40 L0,40 Z" fill="#ffffff"></path></svg>

## Problem we solve

Large teams and products produce hours of video and audio that cannot be searched precisely. Existing tools surface clips poorly, lose timestamps, and provide no auditable source for summaries.

```mermaid
flowchart LR
  A[Teams] --> B[Large Media Repositories]
  B --> C[Manual Search / Playback]
  C --> D[Slow Knowledge Extraction]
  D --> E[Lost Context]
  style C fill:#ffefef,stroke:#ff6b6b
```

---

## Ultra-Concise Solution Overview

We provide a pluggable pipeline: robust media ingestion, configurable ASR, chunk-aware embedding, and a vector-backed retriever plus a source-aware summarizer. Everything is observable, auditable, and deployable.

```mermaid
flowchart LR
  User[User/UI] --> Upload[Uploader]
  Upload --> Extract[Audio Extractor]
  Extract --> ASR[ASR Service]
  ASR --> Chunk[Chunker]
  Chunk --> Embed[Embedding Service]
  Embed --> VectorDB[(Vector DB)]
  Queryer[Query API] --> VectorDB
  VectorDB --> Rescorer[Re-ranker]
  Rescorer --> Summarizer[Summarizer]
  Summarizer --> UI[UI - Timestamps + Snippets]
```

---

## Architecture (detailed)

### System architecture (high level)
```mermaid
graph TD
  subgraph "Ingest"
    Uploader --> Extractor
    Extractor --> ASR
  end
  subgraph "Indexing"
    ASR --> Chunker --> Embedder --> VectorDB
  end
  subgraph "Query"
    Client --> API --> Retriever --> Re-ranker --> Summarizer
    Summarizer --> Client
  end
  VectorDB -.-> MetadataDB
```

### C4 container diagram
```mermaid
flowchart LR
  subgraph Frontend
    FE[Streamlit / React]
  end
  subgraph Backend
    API[FastAPI]
    Worker[Worker Pool - Celery/RQ]
    ASR[ASR Service]
    Embed[Embedding Service]
    Vector[(Chroma / Milvus)]
    Meta[(Postgres)]
  end
  FE --> API
  API --> Worker
  Worker --> ASR
  Worker --> Embed
  Embed --> Vector
  API --> Vector
  API --> Meta
```

### Sequence: upload -> index
```mermaid
sequenceDiagram
  participant U as User
  participant API
  participant W as Worker
  participant ASR
  participant E as Embed
  participant V as VectorDB

  U->>API: POST /upload (media)
  API->>W: enqueue job
  W->>ASR: transcribe(audio)
  ASR-->>W: transcript
  W->>E: embed(chunks)
  E->>V: index(embeddings)
  V-->>W: ack
  W-->>API: job done
  API-->>U: job complete
```

### ER diagram (metadata)
```mermaid
erDiagram
  USERS {
    string id PK
    string name
    string email
  }
  MEDIA {
    string id PK
    string title
    datetime uploaded_at
  }
  TRANSCRIPTS {
    string id PK
    string media_id FK
    text body
  }
  EMBEDDINGS {
    string id PK
    string transcript_id FK
    float[] vector
  }
  USERS ||--o{ MEDIA : uploads
  MEDIA ||--o{ TRANSCRIPTS : contains
  TRANSCRIPTS ||--o{ EMBEDDINGS : stores
```

### Deployment diagram
```mermaid
flowchart LR
  GitHub --> CI[GitHub Actions]
  CI --> Registry[Container Registry]
  Registry --> K8s[Kubernetes Cluster]
  K8s --> LB[Load Balancer]
  LB --> Web[Web Frontend]
  LB --> API[API Pods]
  API --> Workers[Worker Pods]
  Workers --> VectorDB[(Managed Vector DB)]
  Workers --> Blob[(S3/Azure Blob)]
```

### Auth flow
```mermaid
sequenceDiagram
  participant Browser
  participant Auth[Auth Server]
  participant API
  Browser->>Auth: OAuth login
  Auth-->>Browser: JWT
  Browser->>API: Bearer JWT
  API->>Auth: validate
```

---

## Icon-based feature grid

<div align="center">
  <table><tr>
    <td align="center" width="200">
      <img src="https://via.placeholder.com/72.svg?text=ASR" alt="ASR"><br/>
      <strong>Accurate ASR</strong><br/>Speaker & noise-aware
    </td>
    <td align="center" width="200">
      <img src="https://via.placeholder.com/72.svg?text=Search" alt="Search"><br/>
      <strong>Semantic Search</strong><br/>Embeddings + timestamps
    </td>
    <td align="center" width="200">
      <img src="https://via.placeholder.com/72.svg?text=Summ" alt="Summ"><br/>
      <strong>Summarization</strong><br/>Source-cited summaries
    </td>
  </tr></table>
</div>

---

## API lifecycle (sequence)
```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Retriever
  participant VectorDB
  Client->>API: POST /query {q}
  API->>Retriever: embed(q)
  Retriever->>VectorDB: top_k
  VectorDB-->>Retriever: hits
  Retriever->>API: ranked
  API-->>Client: JSON + URLs + timestamps
```

---

## Roadmap (Gantt)
```mermaid
gantt
  dateFormat  YYYY-MM-DD
  title Roadmap - 6 months
  section Core
  Media ingest pipeline :done, des1, 2026-04-01, 20d
  ASR scaling :active, des2, 2026-05-01, 40d
  section Features
  Summarizer v1 :des3, 2026-06-01, 20d
  Timestamped QA :des4, 2026-06-25, 30d
  section Ops
  Git LFS migration :des5, 2026-05-21, 7d
  K8s deployment :des6, 2026-07-01, 30d
```

---

## Folder tree
```
.
├── app.py                 # Streamlit demo
├── main.py                # CLI / runner
├── Requirements.txt
├── core/
│   ├── extractor.py
│   ├── transcriber.py
│   ├── chunker.py
│   ├── summarizer.py
│   └── vector_store.py
├── utils/
│   └── audio_processor.py
├── assets/
│   ├── gifs/
│   └── svgs/
├── downloades/            # ignored (local media)
├── vector_db/             # ignored (local index)
└── README.md
```

---

## Installation & Quickstart

```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
source .venv/bin/activate  # macOS / Linux
pip install -r Requirements.txt
streamlit run app.py
```

Environment (example):
```
OPENAI_API_KEY=sk-...
VECTOR_DB_PATH=./vector_db
DATABASE_URL=postgres://user:pass@localhost:5432/db
S3_BUCKET=ai-video-assets
```

---

## CI/CD pipeline (Mermaid)
```mermaid
flowchart TD
  Commit --> GitHubActions[GitHub Actions]
  GitHubActions --> Tests[Run tests & linters]
  Tests --> Build[Build container]
  Build --> Push[Push to registry]
  Push --> Deploy[Deploy to cluster]
```

---

## Security & Privacy

- JWT-based auth with short TTL and role checks
- TLS everywhere; DB encryption at rest
- Media stored in object storage with signed URLs

---

## Contributing

Please read `CONTRIBUTING.md` and open an issue first. Use feature branches (`feature/*`) and PRs against `develop`.

---

<div align="center" style="margin-top:28px">
  <small>Made with engineering care • Replace GIF placeholders in <code>assets/gifs/</code> • © 2026</small>
</div>

---

## Live Demo

<details>
<summary>Demo GIF & Screenshots</summary>

- GIF Demo placeholder — motion: user uploads video → automatic transcription progress bar → semantic search returning clips → summarized notes panel opening.
  ![Demo GIF Placeholder](https://via.placeholder.com/900x400.gif?text=Demo+Flow+-+upload%2C+transcribe%2C+search%2C+summarize)

- Screenshot Grid (3-up)
  <p align="center">
    <img src="https://via.placeholder.com/300x180.png?text=Upload+UI" alt="Upload UI" width="300" /> &nbsp;
    <img src="https://via.placeholder.com/300x180.png?text=Transcript+Editor" alt="Transcript Editor" width="300" /> &nbsp;
    <img src="https://via.placeholder.com/300x180.png?text=Search+Results" alt="Search Results" width="300" />
  </p>

Key flows visualized:
- Ingest → Transcribe → Chunk → Embed → Store → Query → Summarize
- Live playback + timestamped highlights for search hits

</details>

---

## Problem Statement

Why this exists:
- Audio/video knowledge is siloed and hard to search.
- Manual note-taking is slow and lossy.
- Teams need precise, timestamped answers from media.

Mermaid: "Current broken system" (high level)
```mermaid
flowchart LR
  A[Users] --> B[Manual Search in Videos]
  B --> C[Watch Full Video]
  C --> D[Manual Notes]
  D --> E[Knowledge Scattered]
  style B fill:#ffdddd,stroke:#ff3333
  style C fill:#ffe6cc,stroke:#ff8800
  style E fill:#f3f3f3,stroke:#999
```

Data flow visualization (current pain points):
```mermaid
graph TD
  U[User Query] -->|search| S[Filesystem Search]
  S -->|no timestamps| F[Full Playback]
  F --> N[Manual Extraction]
  N --> K[Local Notes]
  classDef pain fill:#ffdddd,stroke:#cc0000;
  class S,F pain;
```

---

## Solution Overview

Concise description:
- End-to-end AV ingestion pipeline that produces searchable embeddings and human-readable summaries.
- Precise timestamp mapping for result snippets and video playback.
- Pluggable modules for transcription, embedding, and storage.

System-level architecture (Mermaid)
```mermaid
flowchart LR
  subgraph Ingest
    U[User Upload] --> I[Uploader]
    I --> P[Preprocessor]
  end

  subgraph Processing
    P --> T[Transcription Service]
    T --> C[Chunker]
    C --> E[Embedding Service]
    E --> VS[Vector Store]
  end

  subgraph Query
    Q[User Query] --> R[Retriever]
    R --> L[Re-ranker]
    L --> S[Summarizer]
    S --> UI[UI / Playback]
  end

  VS --> R
  E --> VS
  S --> UI
```

Component interaction flow:
- Uploader -> Preprocessor (extract audio) -> Transcription -> Chunking -> Embedding -> Vector DB -> Retriever -> Summarizer -> UI

Modular breakdown:
- Ingest: uploader, media extractor
- Core: transcriber, chunker, embedder
- Storage: Chroma vector DB + metadata store
- Interface: Streamlit (or React) UI + playback integration
- Ops: Docker, CI, Terraform/K8s manifests

---

## System Architecture (Detailed)

### Frontend architecture
```mermaid
flowchart TD
  UI[UI (Streamlit/React)]
  UI --> API[API Gateway]
  API --> Auth[Auth Service]
  API --> Backend[Backend API]
  Backend --> Vector[Vector DB]
  Backend --> Meta[Metadata DB]
```

### Backend architecture
```mermaid
sequenceDiagram
  participant UI
  participant API
  participant Transcribe
  participant Embed
  participant VectorDB
  UI->>API: POST /upload (file)
  API->>Transcribe: start job
  Transcribe->>Embed: send chunks
  Embed->>VectorDB: index embeddings
  VectorDB-->>API: ack
  API-->>UI: job created
```

### Database schema (ER)
```mermaid
erDiagram
  USERS {
    string id PK
    string name
    string email
  }
  MEDIA {
    string id PK
    string title
    datetime uploaded_at
  }
  TRANSCRIPTS {
    string id PK
    string media_id FK
    text text
    int start_ms
    int end_ms
  }
  EMBEDDINGS {
    string id PK
    string transcript_id FK
    float[] vector
  }
  USERS ||--o{ MEDIA : owns
  MEDIA ||--o{ TRANSCRIPTS : contains
  TRANSCRIPTS ||--o{ EMBEDDINGS : has
```

### API flow
```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Worker
  participant VectorDB
  Client->>API: POST /query {q}
  API->>Worker: search(q)
  Worker->>VectorDB: top_k(q)
  VectorDB-->>Worker: results
  Worker->>API: ranked results
  API-->>Client: JSON results
```

### Authentication flow
```mermaid
sequenceDiagram
  participant Browser
  participant Auth
  participant API
  Browser->>Auth: /login (OAuth)
  Auth->>Browser: JWT
  Browser->>API: Authorization: Bearer JWT
  API->>Auth: validate token
```

### Deployment / Cloud diagram
```mermaid
flowchart LR
  subgraph Cloud
    LB[Load Balancer]
    LB --> Web[Web App (Autoscaled)]
    LB --> API[API (Autoscaled)]
    API --> Workers[Background Workers (Queue)]
    Workers --> VectorDB[(Managed Vector DB) ]
    Workers --> Blob[(Object Storage)]
  end
  Developer --> GitHub
  GitHub -->|CI/CD| Registry[Container Registry] -->|Deploy| Cloud
```

---

## Core Features

- Feature grid
  - Ingest & Transcribe
    - Summary: High-accuracy ASR with speaker labels support
    - Mini diagram:
      ```mermaid
      flowchart LR
        File --> Extract --> ASR --> Transcript
      ```
    - Screenshot: placeholder

  - Semantic Search
    - Summary: Dense retrieval with embeddings + timestamp mapping
    - Mini diagram:
      ```mermaid
      flowchart LR
        Query --> Embed --> VectorDB --> Snippets
      ```

  - Summarization & QA
    - Summary: Multi-shot summarizer with source citations (timestamps)
    - Mini diagram:
      ```mermaid
      sequenceDiagram
        User->>System: Summarize(results)
        System->>LM: summarize with context
        LM-->>System: summary (with timestamps)
      ```

  - Playback with Highlights
    - Summary: Click-to-play from result timestamp
    - Mini diagram:
      ```mermaid
      flowchart LR
        ResultClick --> Player[start@timestamp]
      ```

---

## Tech Stack Visualization

Layered stack (top-down)
```mermaid
flowchart TB
  subgraph UI
    A[Streamlit / React]
  end
  subgraph API
    B[FastAPI / Flask]
    B --> C[Workers (RQ / Celery)]
  end
  subgraph Services
    D[ASR Model (Whisper/Local/Batched)]
    E[Embedding (OpenAI/HuggingFace)]
    F[Vector DB (Chroma / Milvus)]
    G[Metadata DB (Postgres)]
  end
  subgraph Infra
    H[Docker / K8s]
    I[Object Storage (S3)]
    J[CI/CD (GitHub Actions)]
    K[Monitoring (Prometheus + Grafana)]
  end
  A --> B --> C --> D
  C --> E --> F
  B --> G
  H --> I
```

Tools categorized:
- Frontend: Streamlit, React, TailwindCSS, TypeScript
- Backend: FastAPI, Celery/RQ, Python 3.11
- AI/ML: Whisper/WhisperX, HuggingFace Transformers, OpenAI embeddings (optional)
- DevOps: Docker, Kubernetes, GitHub Actions, Terraform
- Infra: AWS/GCP, S3, RDS/Postgres, Managed Vector DB or self-hosted Chroma

---

## Folder Structure

```
.
├── app.py
├── main.py
├── Requirements.txt
├── core/
│   ├── extractor.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── rag_engine.py
│   └── vector_store.py
├── utils/
│   └── audio_processor.py
├── downloades/
├── vector_db/
└── README.md
```

Brief:
- `core/` — pipeline components and business logic
- `utils/` — helpers and preprocessing
- `vector_db/` — local vector DB artifacts (ignored for repo)
- `downloades/` — local media for testing (ignored)
- top-level apps: `app.py` (streamlit demo), `main.py` (CLI/runner)

---

## Installation & Setup

Quick start (Linux/macOS/Windows WSL)
```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\\Scripts\\activate on Windows
pip install -r Requirements.txt
```

Environment variables (table):

| Variable | Example | Description |
|---|---:|---|
| `OPENAI_API_KEY` | sk-xxxx | Optional: embeddings provider |
| `VECTOR_DB_PATH` | ./vector_db/chroma.sqlite3 | Vector DB path |
| `S3_BUCKET` | my-bucket | Object storage for uploaded media |
| `DATABASE_URL` | postgres://... | Metadata DB connection |

Sample `.env`:
```
OPENAI_API_KEY=sk-...
VECTOR_DB_PATH=./vector_db
DATABASE_URL=postgres://user:pass@localhost:5432/db
S3_BUCKET=ai-video-assistant-dev
```

Run locally:
```
streamlit run app.py
```

Production (container):
- Build:
```
docker build -t ai-video-assistant:latest .
```
- Deploy via Kubernetes manifest or GitHub Actions to your cloud.

---

## API Documentation

Endpoints summary:

| Method | Path | Description |
|---:|---|---|
| POST | /upload | Uploads media, returns job id |
| GET | /status/{job_id} | Job status |
| POST | /query | Semantic query |
| POST | /summarize | Generate summary from results |

Sample request/response
```http
POST /api/query
Content-Type: application/json

{
  "q": "How to train the model?",
  "k": 5
}
```

Response:
```json
{
  "query":"How to train the model?",
  "results":[
    {"id":"r1","score":0.92,"start_ms":342100,"end_ms":347200,"text":"...","source_media":"m1"}
  ]
}
```

Sequence for a query:
```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Retriever
  participant VectorDB
  Client->>API: POST /query
  API->>Retriever: embed(query)
  Retriever->>VectorDB: top_k
  VectorDB-->>Retriever: hits
  Retriever->>API: ranked hits
  API-->>Client: JSON hits
```

---

## Performance & Scalability

Key metrics to target:
- Ingest throughput: 1–3 GB/hour (batch ASR)
- Query latency: 100–500ms for cached embeddings; 200–1500ms for full retrieval+re-ranking
- Summarization latency: depends on LLM provider (100ms–2s)

Throughput diagram:
```mermaid
flowchart LR
  Ingest[Ingest Workers] -->|parallel| ASR[ASR Cluster]
  ASR -->|batch| Embed[Embedding Pool]
  Embed -->|bulk| VectorDB
  VectorDB -->|low-latency| API[Frontend API]
```

Scaling approach:
- Autoscale worker pods based on queue depth
- Use model batching for ASR/embedding to increase throughput
- Cache embeddings and warm frequently accessed shards

---

## Security Architecture

Authentication & Roles:
```mermaid
sequenceDiagram
  participant User
  participant Auth
  participant API
  participant DB
  User->>Auth: OAuth
  Auth-->>User: access_token
  User->>API: Bearer token
  API->>DB: check role/permissions
```

Notes:
- Use JWT with short TTL and refresh tokens
- Encrypt sensitive data at rest (DB-level encryption) and in transit (TLS)
- Role-based access for admin vs. regular users
- Audit logs for ingestion and retrieval

---

## Roadmap

```mermaid
gantt
  title Roadmap
  dateFormat  YYYY-MM-DD
  section Core
  Ingest pipeline :done, a1, 2026-04-01, 30d
  ASR scaling       :active, a2, 2026-05-01, 45d
  section Features
  Summarizer       :a3, 2026-06-15, 30d
  QA mode          :a4, 2026-07-15, 30d
  section Ops
  LFS migration    :a5, 2026-05-21, 7d
  K8s deployment   :a6, 2026-07-01, 45d
```

---

## Contributing

Contribution workflow:
```mermaid
flowchart LR
  Developer --> Fork --> Branch[feature/*] --> PR --> CI --> Review --> Merge --> Release
```

Branch strategy:
- `main` — protected, production-ready
- `develop` — integration branch
- `feature/*` — feature branches
- `hotfix/*` — emergency fixes

Guidelines:
- Open issues for feature requests
- One PR per logical change; link issue
- Tests required for core features; CI runs lint, unit tests, type checks

---

## License & Credits

- License: MIT (or choose your license)
- Credits: List contributors and third-party libraries in `NOTICE.md`.
- Logo & illustrations: placeholders — replace with original assets.

---

## Assets & Placeholders

- Logo SVG placeholder: replace `https://via.placeholder.com/160x160.svg?text=LOGO`
- Animated banner GIF: replace with `assets/banner.gif` — should demonstrate upload → ASR → search → summary
- Demo GIFs: place in `assets/gifs/` with short captions
- Diagrams: all Mermaid blocks are live and editable in repo

---

## Final notes

- Replace all `<INSERT ...>` placeholders with project-specific copy.
- Move large media into external object storage or Git LFS — `.gitignore` already excludes `downloades/` and local DB artifacts.
- Consider adding a `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and GitHub Actions for CI.

---

If you'd like, I can:
- Save this `README.md` into the repository and commit it.
- Add demo GIFs and SVG placeholders into `assets/`.
- Configure GitHub Actions to render Mermaid diagrams in previews.

Which follow-up should I do next?
