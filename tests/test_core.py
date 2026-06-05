"""VANTAGE test suite for core modules."""

import pytest
import numpy as np

from src.ingestion.stream_manager import StreamManager
from src.tracking.reid import ReIDEngine
from src.fusion import FusionEngine


# ── StreamManager ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_register_valid():
    mgr = StreamManager()
    sid = await mgr.register("rtsp://camera-01.local/stream")
    assert len(sid) == 12
    assert sid in mgr._streams


@pytest.mark.asyncio
async def test_register_invalid_scheme():
    mgr = StreamManager()
    with pytest.raises(ValueError, match="Unsupported URI scheme"):
        await mgr.register("ftp://bad/")


@pytest.mark.asyncio
async def test_start_stop():
    mgr = StreamManager()
    sid = await mgr.register("rtsp://cam/")
    assert await mgr.start(sid) is True
    assert mgr._streams[sid]["active"] is True
    assert await mgr.stop(sid) is True
    assert mgr._streams[sid]["active"] is False


@pytest.mark.asyncio
async def test_grab_frame():
    mgr = StreamManager()
    sid = await mgr.register("rtsp://cam/")
    await mgr.start(sid)
    frame = await mgr.grab_frame(sid)
    assert frame is not None
    assert frame.shape == (1080, 1920, 3)


@pytest.mark.asyncio
async def test_stats():
    mgr = StreamManager()
    await mgr.register("rtsp://cam-1/")
    await mgr.register("rtsp://cam-2/")
    s = mgr.stats()
    assert s["total"] == 2
    assert s["active"] == 0


# ── ReIDEngine ───────────────────────────────────────────────────────────────

def test_encode_output_shape():
    engine = ReIDEngine()
    frame = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
    bbox = (100, 100, 200, 300)
    emb = engine.encode(frame, bbox)
    assert emb.shape == (512,)
    assert emb.dtype == np.float32


def test_encode_deterministic():
    engine = ReIDEngine()
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    bbox = (10, 10, 50, 50)
    e1 = engine.encode(frame, bbox)
    e2 = engine.encode(frame, bbox)
    np.testing.assert_array_equal(e1, e2)


def test_encode_unit_norm():
    engine = ReIDEngine()
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    bbox = (10, 10, 50, 50)
    emb = engine.encode(frame, bbox)
    norm = np.linalg.norm(emb)
    assert abs(norm - 1.0) < 1e-6


def test_match_threshold():
    engine = ReIDEngine()
    query = np.array([1.0, 0.0, 0.0])
    gallery = np.array([[0.99, 0.0, 0.0], [0.0, 1.0, 0.0]])
    matches = engine.match(query, gallery, threshold=0.5)
    assert matches == [0]


def test_match_below_threshold():
    engine = ReIDEngine()
    query = np.array([1.0, 0.0, 0.0])
    gallery = np.array([[0.0, 1.0, 0.0]])
    matches = engine.match(query, gallery, threshold=0.9)
    assert matches == []


# ── FusionEngine ─────────────────────────────────────────────────────────────

def test_fusion_align():
    engine = FusionEngine()
    result = engine.align({"rgb": "frame_a", "thermal": "frame_b"})
    assert "rgb" in result
    assert "thermal" in result
    assert "aligned_at" in result