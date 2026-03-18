import librosa
import numpy as np


def load_audio(file_path: str, sr: int = 22050):
    """
    Load an audio file (wav, mp3, etc.) as mono.
    """
    y, sr = librosa.load(file_path, sr=sr, mono=True)
    return y, sr


def extract_features(y, sr, hop_length: int = 512):
    """
    Extract a small set of simple MIR features.
    Returns a dictionary of frame-based features.
    """
    # RMS energy
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]

    # Spectral centroid (brightness / sharpness of sound)
    spectral_centroid = librosa.feature.spectral_centroid(
        y=y, sr=sr, hop_length=hop_length
    )[0]

    # Onset strength envelope
    onset_strength = librosa.onset.onset_strength(
        y=y, sr=sr, hop_length=hop_length, aggregate=np.median
    )

    # Beat tracking
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)

    # Frame timestamps
    times = librosa.frames_to_time(
        np.arange(len(rms)), sr=sr, hop_length=hop_length
    )

    return {
        "times": times,
        "rms": rms,
        "spectral_centroid": spectral_centroid,
        "onset_strength": onset_strength,
        "tempo": float(np.atleast_1d(tempo)[0]),
        "beat_frames": beat_frames,
    }