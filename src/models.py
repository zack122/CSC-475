"""Shared data structures for the MIR-to-DMX pipeline."""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class FeatureFrame:
    """MIR features extracted from a single audio chunk."""

    timestamp_s: float = 0.0
    tempo_bpm: float = 0.0
    beat_phase: float = 0.0           # 0.0-1.0, position within current beat
    onset_strength: float = 0.0       # 0.0-1.0
    pulse_clarity: float = 0.0        # 0.0-1.0, rhythmic steadiness
    rms_energy: float = 0.0           # 0.0-1.0
    spectral_centroid: float = 0.0    # 0.0-1.0, normalized brightness
    spectral_flux: float = 0.0        # 0.0-1.0
    hpss_harmonic_ratio: float = 0.0  # 0.0-1.0
    chroma: np.ndarray = field(default_factory=lambda: np.zeros(12))
    is_silent: bool = True
    segment_label: str = "unknown"


@dataclass
class DMXFrame:
    """DMX channel values produced by the mapping engine."""

    dimmer: int = 0      # 0-255
    red: int = 0         # 0-255
    green: int = 0       # 0-255
    blue: int = 0        # 0-255
    strobe_rate: int = 0 # 0-255
    scene_id: int = 0
    pan: int = 0         # 0-255
    tilt: int = 0        # 0-255
