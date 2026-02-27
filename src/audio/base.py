"""Abstract audio source interface."""

from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np


class AudioSource(ABC):
    """Base class for all audio input sources.

    Subclasses must implement ``frames()`` which yields fixed-size
    numpy arrays of audio samples (mono, float32).
    """

    @abstractmethod
    def frames(self) -> Iterator[np.ndarray]:
        """Yield successive audio frames for analysis."""
        ...

    @abstractmethod
    def sample_rate(self) -> int:
        """Return the sample rate of the audio stream."""
        ...
