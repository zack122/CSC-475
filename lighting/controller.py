import numpy as np


def normalize_feature(values):
    """
    Normalize a feature array to the range [0, 1].
    """
    values = np.asarray(values, dtype=float)
    min_val = np.min(values)
    max_val = np.max(values)

    if max_val - min_val < 1e-8:
        return np.zeros_like(values)

    return (values - min_val) / (max_val - min_val)


def map_features_to_lighting(features):
    rms = np.asarray(features["rms"], dtype=float)
    times = np.asarray(features["times"], dtype=float)

    rms_norm = normalize_feature(rms)
    centroid_norm = normalize_feature(features["spectral_centroid"])
    onset_norm = normalize_feature(features["onset_strength"])

    lighting_frames = []

    # Silence gate: detect sustained low-RMS regions and force blackout
    if len(times) > 1 and len(rms) == len(times):
        hop_sec = float(times[1] - times[0]) if times[1] > times[0] else 0.0
        min_silence_sec = 0.5
        min_frames = int(np.ceil(min_silence_sec / max(hop_sec, 1e-9))) if hop_sec > 0 else 1
        max_r = float(np.max(rms))
        if max_r <= 1e-12:
            silent = np.ones_like(rms, dtype=bool)
        else:
            thr = max_r * 0.02
            silent = rms <= thr
        if silent.any():
            pad = np.concatenate(([0], silent.astype(int), [0]))
            diff = np.diff(pad)
            starts = np.where(diff == 1)[0]
            ends = np.where(diff == -1)[0]
            gate = np.zeros_like(silent, dtype=bool)
            for s, e in zip(starts, ends):
                if (e - s) >= min_frames:
                    gate[s:e] = True
        else:
            gate = np.zeros_like(silent, dtype=bool)
    else:
        gate = np.zeros_like(rms_norm, dtype=bool)

    for i in range(len(features["times"])):
        is_gated = bool(gate[i]) if i < len(gate) else False
        if is_gated:
            brightness = 0
            warm = 0
            cool = 0
            strobe = False
        else:
            brightness = int(rms_norm[i] * 255)
            warm = int((1.0 - centroid_norm[i]) * 255)
            cool = int(centroid_norm[i] * 255)
            strobe = onset_norm[i] > 0.4 and brightness > 80

        lighting_frames.append({
            "time": float(features["times"][i]),
            "brightness": brightness,
            "warm": warm,
            "cool": cool,
            "strobe": strobe,
            "gated": is_gated,
        })

    return lighting_frames


def print_preview(lighting_frames, step=5):
    """
    Print a simplified preview of lighting states.
    """
    print("\nLighting Preview:")
    strobe_count = sum(1 for frame in lighting_frames if frame["strobe"])
    print(f"Total frames: {len(lighting_frames)}")
    print(f"Total strobe frames: {strobe_count}\n")

    for i in range(0, len(lighting_frames), step):
        frame = lighting_frames[i]
        print(
            f"t={frame['time']:.2f}s | "
            f"brightness={frame['brightness']:3d} | "
            f"warm={frame['warm']:3d} | "
            f"cool={frame['cool']:3d} | "
            f"strobe={frame['strobe']}"
        )
