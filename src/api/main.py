"""VANTAGE API — health check and stream management endpoints."""

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.ingestion.stream_manager import StreamManager
from src.tracking.reid import ReIDEngine

app = FastAPI(title="VANTAGE API", version="0.1.0-dev")

stream_manager = StreamManager()
reid_engine = ReIDEngine()


# ── Schemas ──────────────────────────────────────────────────────────────────

class StreamRegister(BaseModel):
    uri: str = Field(..., description="Stream URL (rtsp://, webrtc://, …)")
    source_type: str = Field("rtsp", description="rtsp / webrtc / mavlink / bodycam")


class StreamOut(BaseModel):
    stream_id: str
    uri: str
    active: bool
    fps: int


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.1.0-dev",
        "streams": stream_manager.stats(),
    }


@app.post("/streams/register", response_model=StreamOut)
async def register_stream(body: StreamRegister):
    try:
        stream_id = await stream_manager.register(body.uri, body.source_type)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return StreamOut(
        stream_id=stream_id,
        uri=body.uri,
        active=False,
        fps=0,
    )


@app.post("/streams/{stream_id}/start")
async def start_stream(stream_id: str):
    try:
        ok = await stream_manager.start(stream_id)
    except ValueError:
        raise HTTPException(404, "Stream not found")
    return {"stream_id": stream_id, "started": ok}


@app.get("/reid/encode")
async def encode_embedding():
    """Return a sample 512-dim embedding vector (demo)."""
    synthetic_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    bbox = (100, 100, 300, 500)
    emb = reid_engine.encode(synthetic_frame, bbox)
    return {"embedding": emb.tolist(), "dim": int(emb.shape[0])}