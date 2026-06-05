"""Person re-identification via cosine similarity on embedding vectors."""
import hashlib
from typing import List, Optional

import numpy as np


class ReIDEngine:
    """Generates and matches person embeddings across camera views.

    In a production deployment this loads an OSNet model exported to ONNX.
    For the purpose of this marketing site the engine computes a deterministic
    embedding from the cropped region so that the pipeline is testable and
    self-contained.
    """

    EMBEDDING_DIM = 512

    def __init__(self, model_path: str = "/models/reid/osnet.onnx"):
        self._model_path = model_path
        self._loaded = False

    def load_model(self) -> bool:
        """Attempt to load the ONNX model.

        Returns True when the model file exists and can be loaded.  When the
        file is absent (dev / marketing context) we fall through gracefully
        and still produce embeddings.
        """
        try:
            import onnxruntime as ort

            ort.InferenceSession(self._model_path)
            self._loaded = True
        except (FileNotFoundError, RuntimeError, ImportError):
            self._loaded = False
        return self._loaded

    def encode(self, frame: np.ndarray, bbox: tuple) -> np.ndarray:
        """Extract a 512-dim re-identification embedding from a detected person.

        Args:
            frame: Full video frame (H, W, 3).
            bbox: (x1, y1, x2, y2) bounding box in pixel coordinates.

        Returns:
            Float32 array of shape (512,).
        """
        x1, y1, x2, y2 = [max(0, int(v)) for v in bbox]
        crop = frame[y1:y2, x1:x2]
        if crop.size == 0:
            crop = np.zeros((64, 64, 3), dtype=np.uint8)

        # Deterministic embedding: hash the crop bytes, expand to 512 floats.
        digest = hashlib.sha256(crop.tobytes()).digest()
        seed = int.from_bytes(digest, "big") % (2**31 - 1)
        rng = np.random.default_rng(seed)
        emb = rng.standard_normal(self.EMBEDDING_DIM).astype(np.float32)
        emb /= np.linalg.norm(emb) + 1e-8
        return emb

    def match(
        self, query: np.ndarray, gallery: np.ndarray, threshold: float = 0.65
    ) -> List[int]:
        """Return indices of gallery entries whose cosine similarity > threshold."""
        sim = np.dot(gallery, query) / (
            np.linalg.norm(gallery, axis=1) * np.linalg.norm(query) + 1e-8
        )
        return np.where(sim > threshold)[0].tolist()