"""Orchestrates all MIR feature extractors into a single pipeline."""

import numpy as np

from src.models import FeatureFrame
from src.mir.rhythm import RhythmExtractor
from src.mir.spectral import SpectralExtractor
from src.mir.structural import StructuralExtractor
from src.mir.smoothing import FeatureSmoother


class FeaturePipeline:
    """Runs rhythm, spectral, and structural extractors on each audio frame
    and returns a unified FeatureFrame."""

    def __init__(self, config: dict):
        self._config = config
        self._rhythm = RhythmExtractor(config)
        self._spectral = SpectralExtractor(config)
        self._structural = StructuralExtractor(config)
        self._smoother = FeatureSmoother(config.get("smoothing", {}))

    def extract(self, frame: np.ndarray, sr: int, timestamp_s: float = 0.0) -> FeatureFrame:
        """Extract and smooth all MIR features from a single audio frame."""
        # TODO: run extractors, combine into FeatureFrame, apply smoothing
        raise NotImplementedError
