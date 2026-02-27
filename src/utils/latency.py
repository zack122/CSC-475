"""Per-stage latency tracker for the processing pipeline."""

import time
from collections import deque
from dataclasses import dataclass


@dataclass
class LatencyStats:
    mean_ms: float
    p95_ms: float
    max_ms: float


class LatencyTracker:
    """Records timestamps at each pipeline stage and computes rolling statistics."""

    def __init__(self, window_size: int = 100):
        self._window_size = window_size
        self._records: deque[float] = deque(maxlen=window_size)

    def start(self) -> float:
        """Return a high-resolution start timestamp."""
        return time.perf_counter()

    def record(self, start: float) -> float:
        """Record elapsed time since ``start`` and return it in milliseconds."""
        # TODO: compute elapsed, append to _records, warn if > 20ms
        raise NotImplementedError

    def stats(self) -> LatencyStats:
        """Return rolling latency statistics."""
        # TODO: compute mean, p95, max from _records
        raise NotImplementedError
