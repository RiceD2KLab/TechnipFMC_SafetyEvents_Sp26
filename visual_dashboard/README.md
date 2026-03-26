# Visual Dashboard

Interactive dashboard for exploring the TechnipFMC safety knowledge graph. Two active
implementations: a FastAPI + React frontend, and a legacy Streamlit dashboard.

## Architecture

```
visual_dashboard/
├── backend/        FastAPI server — serves KG data via REST endpoints
├── frontend/       React/TypeScript SPA — production UI
└── dashboard/      Streamlit dashboard — legacy, functional
```

## Backend (FastAPI)

REST API serving knowledge graph data from pipeline parquet outputs.

```bash
cd visual_dashboard/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Endpoints:**

| Route | Description |
|-------|-------------|
| `GET /kg/incidents` | List incidents with optional filters |
| `GET /kg/entity-types` | Available entity types and counts |
| `GET /kg/search?q=` | Search entities by name |
| `GET /kg/subgraph/{incident_id}` | Subgraph around a specific incident |

**Files:**

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app with CORS, lifespan KG pre-loading |
| `kg_loader.py` | Loads parquets, builds NetworkX DiGraph, entity search |
| `graph_serializer.py` | Converts subgraph to JSON with spring layout positioning |
| `schemas.py` | Pydantic response models |
| `routers/kg.py` | API route definitions |

**Data source:** Reads from `pipeline/outputs/` (entities, relations, metadata parquets).

## Frontend (React + TypeScript)

Single-page application built with Vite, React, and shadcn/ui.

```bash
cd visual_dashboard/frontend
npm install
npm run dev
```

**Pages:**

| Page | Description |
|------|-------------|
| Main Dashboard | Incident overview with filters and statistics |
| Knowledge Graph Reasoning | Interactive graph exploration and subgraph visualization |
| Event Similarity Discovery | Similar incident retrieval |
| Data Extraction Quality | Pipeline quality metrics |

**Requires** the FastAPI backend running at `http://localhost:8000`.

## Dashboard (Streamlit) — Legacy

Standalone Streamlit dashboard with built-in data loading and visualization.

```bash
cd visual_dashboard/dashboard
streamlit run app.py
```

Provides filter-based incident exploration (status, impact type, risk, GBU, country),
statistical summaries, bar/pie/heatmap charts, word clouds, and temporal trend plots.

## Dependencies

- **Backend:** `requirements.txt` in `backend/` (FastAPI, pandas, networkx)
- **Frontend:** `package.json` in `frontend/` (React, Vite, shadcn/ui)
- **Dashboard:** Uses root `requirements.txt` (Streamlit, plotly, networkx)
