import numpy as np


def normalize_feature(values):
    values = np.asarray(values, dtype=float)
    min_val = np.min(values)
    max_val = np.max(values)

    if max_val - min_val < 1e-8:
        return np.zeros_like(values)

    return (values - min_val) / (max_val - min_val)


def map_features_to_lighting(features):
    rms = np.asarray(features["rms"], dtype=float)
    times = np.asarray(features["times"], dtype=float)
    n = len(times)

    rms_norm = normalize_feature(rms)
    centroid_norm = normalize_feature(features["spectral_centroid"])
    onset_norm = normalize_feature(features["onset_strength"])

    if "spectral_flux" in features and len(features["spectral_flux"]) == n:
        flux_norm = normalize_feature(features["spectral_flux"])
    else:
        flux_norm = np.zeros_like(rms_norm)

    # PI3: local tempo normalised to [0,1]
    if "local_tempo" in features:
        lt = np.asarray(features["local_tempo"], dtype=float)
        lt = lt[:n] if len(lt) >= n else np.pad(lt, (0, n - len(lt)), mode='edge')
        local_tempo_norm = normalize_feature(lt)
    else:
        local_tempo_norm = np.ones(n)

    # PI4: pulse clarity
    if "plp" in features:
        plp = np.asarray(features["plp"], dtype=float)
        plp = plp[:n] if len(plp) >= n else np.pad(plp, (0, n - len(plp)), mode='edge')
        plp_norm = normalize_feature(plp)
    else:
        plp_norm = np.ones(n)

    lighting_frames = []
    prev_brightness = 0
    prev_white = 0

    # Silence gate
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

    for i in range(len(times)):
        is_gated = bool(gate[i]) if i < len(gate) else False

        if is_gated:
            brightness = 0
            red = 0
            green = 0
            blue = 0
            white = 0
            strobe = False
        else:
            clarity = float(plp_norm[i])   # PI4: 0 = unclear beat, 1 = steady beat
            smooth = 1.0 - float(local_tempo_norm[i])

            # PI4: scale contrast by pulse clarity
            raw_brightness = int((0.3 + 0.7 * clarity) * rms_norm[i] * 255)
            raw_white = int((0.3 + 0.7 * clarity) * ((onset_norm[i] * 0.6) + (rms_norm[i] * 0.4)) * 255)
            
            brightness = int(smooth * prev_brightness + (1.0 - smooth) * raw_brightness)
            white = int(smooth * prev_white + (1.0 - smooth) * raw_white)

            red = int((1.0 - centroid_norm[i]) * 255)
            blue = int(centroid_norm[i] * 255)
            green = int(flux_norm[i] * 255)

            strobe = onset_norm[i] > 0.4 and brightness > 80

        prev_brightness = brightness
        prev_white = white

        lighting_frames.append({
            "time": float(times[i]),
            "brightness": brightness,
            "red": red,
            "green": green,
            "blue": blue,
            "white": white,
            "strobe": strobe,
            "gated": is_gated,
        })

    return lighting_frames


def print_preview(lighting_frames, step=5):
    print("\nLighting Preview:")
    strobe_count = sum(1 for frame in lighting_frames if frame["strobe"])
    print(f"Total frames: {len(lighting_frames)}")
    print(f"Total strobe frames: {strobe_count}\n")

    for i in range(0, len(lighting_frames), step):
        frame = lighting_frames[i]
        print(
            f"t={frame['time']:.2f}s | "
            f"brightness={frame['brightness']:3d} | "
            f"red={frame['red']:3d} | "
            f"green={frame['green']:3d} | "
            f"blue={frame['blue']:3d} | "
            f"white={frame['white']:3d} | "
            f"strobe={frame['strobe']}"
        )