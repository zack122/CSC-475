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
    rms_norm = normalize_feature(features["rms"])
    centroid_norm = normalize_feature(features["spectral_centroid"])
    onset_norm = normalize_feature(features["onset_strength"])

    lighting_frames = []

    for i in range(len(features["times"])):
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