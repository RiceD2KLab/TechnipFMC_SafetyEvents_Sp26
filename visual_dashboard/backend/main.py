"""FastAPI backend for the TechnipFMC Safety Dashboard."""

import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kg_loader import load_kg_data
from routers import kg, nlq
from schemas import HealthResponse

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load the Knowledge Graph on startup."""
    logger.info("Loading Knowledge Graph data...")
    G, entities_df, relations_df, metadata_df = load_kg_data()
    logger.info(
        "KG loaded: %d nodes, %d edges, %d metadata rows",
        G.number_of_nodes(),
        G.number_of_edges(),
        len(metadata_df),
    )
    yield


app = FastAPI(
    title="TechnipFMC Safety Dashboard API",
    description="Backend API for Knowledge Graph exploration and safety analytics.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kg.router, prefix="/api")
app.include_router(nlq.router, prefix="/api")


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    try:
        G, _, _, _ = load_kg_data()
        return HealthResponse(
            status="ok",
            graph_loaded=True,
            node_count=G.number_of_nodes(),
            edge_count=G.number_of_edges(),
        )
    except Exception:
        return HealthResponse(
            status="error",
            graph_loaded=False,
            node_count=0,
            edge_count=0,
        )
