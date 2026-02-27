"""File-based audio source using librosa.stream for chunked reading."""

from typing import Iterator

import numpy as np

from src.audio.base import AudioSource


class FileSource(AudioSource):
    """Reads an audio file in overlapping chunks via librosa.stream."""

    def __init__(self, path: str, sr: int = 22050, frame_length: int = 2048, hop_length: int = 512):
        self._path = path
        self._sr = sr
        self._frame_length = frame_length
        self._hop_length = hop_length

    def sample_rate(self) -> int:
        return self._sr

    def frames(self) -> Iterator[np.ndarray]:
        # TODO: implement chunked streaming via librosa.stream
        raise NotImplementedError
