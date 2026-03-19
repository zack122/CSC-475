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
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]

    spectral_centroid = librosa.feature.spectral_centroid(
        y=y, sr=sr, hop_length=hop_length
    )[0]
    mean_spectral_centroid = float(np.mean(spectral_centroid)) if spectral_centroid.size else 0.0

    onset_strength = librosa.onset.onset_strength(
        y=y, sr=sr, hop_length=hop_length, aggregate=np.median
    )

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)

    # Spectral flux (positive differences of L2-normalized magnitude spectrum)
    n_fft = 2048
    S = np.abs(
        librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, window="hann", center=True)
    )
    if S.shape[1] > 0:
        denom = np.linalg.norm(S, axis=0) + 1e-12
        S_norm = S / denom
        D = np.diff(S_norm, axis=1)
        D[D < 0] = 0.0
        spectral_flux = np.concatenate([[0.0], np.sum(D, axis=0)])
    else:
        spectral_flux = np.zeros(0, dtype=float)
    mean_spectral_flux = float(np.mean(spectral_flux)) if spectral_flux.size else 0.0

    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    return {
        "times": times,
        "rms": rms,
        "spectral_centroid": spectral_centroid,
        "mean_spectral_centroid": mean_spectral_centroid,
        "spectral_flux": spectral_flux,
        "mean_spectral_flux": mean_spectral_flux,
        "onset_strength": onset_strength,
        "tempo": float(np.atleast_1d(tempo)[0]),
        "beat_frames": beat_frames,
    }
