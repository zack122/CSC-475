"""Feature-to-DMX mapping engine.

Owner: Leo DeRosa
"""

from src.models import FeatureFrame, DMXFrame


class Mapper:
    """Maps MIR FeatureFrames to DMX channel values using configurable curves."""

    def __init__(self, config: dict):
        self._config = config

    def map(self, features: FeatureFrame) -> DMXFrame:
        """Convert a FeatureFrame into a DMXFrame.

        Mapping rules:
        - rms_energy   -> dimmer   (linear / gamma / sigmoid curve)
        - spectral_centroid -> RGB color palette
        - chroma       -> mood-based hue shift
        - onset_strength -> strobe_rate trigger
        - hpss_harmonic_ratio -> fixture group selection
        """
        # TODO: implement mapping curves
        raise NotImplementedError
