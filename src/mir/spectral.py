"""Spectral feature extraction: centroid, flux, HPSS.

Owner: Tom Yasinchuk
"""

import numpy as np


class SpectralExtractor:
    """Extracts spectral features from an audio frame."""

    def __init__(self, config: dict):
        self._config = config

    def extract_centroid(self, frame: np.ndarray, sr: int) -> float:
        """Return normalized spectral centroid (0.0-1.0)."""
        # TODO: librosa.feature.spectral_centroid
        raise NotImplementedError

    def extract_flux(self, frame: np.ndarray, sr: int) -> float:
        """Return normalized spectral flux (0.0-1.0)."""
        # TODO: onset_strength or manual flux computation
        raise NotImplementedError

    def extract_hpss_ratio(self, frame: np.ndarray, sr: int) -> float:
        """Return harmonic-to-percussive energy ratio (0.0-1.0)."""
        # TODO: librosa.effects.hpss
        raise NotImplementedError
