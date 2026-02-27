"""Structural analysis: chroma, silence gate, segment boundaries.

Owner: Tom Yasinchuk
"""

import numpy as np


class StructuralExtractor:
    """Extracts structural features from an audio frame."""

    def __init__(self, config: dict):
        self._config = config
        self._silence_threshold_db = config.get("silence_threshold_db", -40)

    def extract_chroma(self, frame: np.ndarray, sr: int) -> np.ndarray:
        """Return 12-dimensional chroma vector."""
        # TODO: librosa.feature.chroma_stft
        raise NotImplementedError

    def detect_silence(self, frame: np.ndarray, sr: int) -> bool:
        """Return True if the frame is below the silence threshold."""
        # TODO: RMS check against silence_threshold_db
        raise NotImplementedError

    def detect_segment(self, frame: np.ndarray, sr: int) -> str:
        """Return segment label: 'verse', 'chorus', 'bridge', or 'unknown'."""
        # TODO: spectral novelty / self-similarity boundary detection
        raise NotImplementedError
