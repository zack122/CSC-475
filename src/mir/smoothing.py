"""Feature smoothing and normalization utilities."""

from src.models import FeatureFrame


class FeatureSmoother:
    """Applies EMA and optional median filtering to stabilize feature values."""

    def __init__(self, config: dict):
        self._ema_alpha = config.get("ema_alpha", 0.3)
        self._median_window = config.get("median_window", 5)
        self._history: list[FeatureFrame] = []

    def smooth(self, frame: FeatureFrame) -> FeatureFrame:
        """Return a smoothed copy of the feature frame."""
        # TODO: apply EMA across successive frames, optional median filter
        raise NotImplementedError
