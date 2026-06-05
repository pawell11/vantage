"""Stream lifecycle management for camera, drone, and bodycam feeds."""

import asyncio
import hashlib
from typing import Dict, Optional

import numpy as np


class StreamManager:
    """Manages camera/drone stream connections.

    In production this opens RTSP / WebRTC connections and feeds frames
    into the detection pipeline.  The marketing-site implementation tracks
    stream metadata and simulates frame grabbing with placeholder data so
    the full stack can be exercised in a test environment.
    """

    def __init__(self):
        self._streams: Dict[str, dict] = {}

    async def register(
        self, uri: str, source_type: str = "rtsp"
    ) -> str:
        """Register a new stream and begin ingestion.

        Args:
            uri: Stream URL (rtsp://…, webrtc://…, mavlink://…).
            source_type: One of ``rtsp``, ``webrtc``, ``mavlink``, ``bodycam``.

        Returns:
            A short hex stream identifier.
        """
        if not uri.startswith(("rtsp://", "webrtc://", "mavlink://", "http://")):
            raise ValueError(f"Unsupported URI scheme: {uri}")

        stream_id = hashlib.sha256(uri.encode()).hexdigest()[:12]
        self._streams[stream_id] = {
            "uri": uri,
            "type": source_type,
            "active": False,
            "fps": 0,
        }
        return stream_id

    async def start(self, stream_id: str) -> bool:
        """Begin frame grabbing for a registered stream."""
        if stream_id not in self._streams:
            raise ValueError(f"Unknown stream: {stream_id}")
        self._streams[stream_id]["active"] = True
        self._streams[stream_id]["fps"] = 30
        return True

    async def stop(self, stream_id: str) -> bool:
        """Stop frame grabbing."""
        if stream_id not in self._streams:
            raise ValueError(f"Unknown stream: {stream_id}")
        self._streams[stream_id]["active"] = False
        self._streams[stream_id]["fps"] = 0
        return True

    async def grab_frame(self, stream_id: str) -> Optional[np.ndarray]:
        """Return a synthetic frame for demo/testing purposes.

        In production this reads from the actual video pipeline.
        """
        if stream_id not in self._streams or not self._streams[stream_id]["active"]:
            return None
        # Synthetic 1080p frame for testing
        return np.zeros((1080, 1920, 3), dtype=np.uint8)

    def list_active(self) -> Dict[str, dict]:
        """Return metadata for all registered streams."""
        return dict(self._streams)

    def stats(self) -> dict:
        """Aggregate stream statistics."""
        active = sum(1 for s in self._streams.values() if s["active"])
        return {"total": len(self._streams), "active": active}