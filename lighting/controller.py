import numpy as np


def normalize_feature(values):
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return np.zeros(0, dtype=float)

    min_val = np.min(values)
    max_val = np.max(values)

    if max_val - min_val < 1e-8:
        return np.zeros_like(values)

    return (values - min_val) / (max_val - min_val)


def smooth_feature(values, alpha=0.2):
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return values

    out = np.zeros_like(values)
    out[0] = values[0]
    for i in range(1, len(values)):
        out[i] = alpha * values[i] + (1.0 - alpha) * out[i - 1]
    return out


def make_fixture_state(brightness, warm, cool, strobe):
    return {
        "brightness": int(np.clip(brightness, 0, 255)),
        "warm": int(np.clip(warm, 0, 255)),
        "cool": int(np.clip(cool, 0, 255)),
        "strobe": bool(strobe),
    }


def get_palette(state, palette_cycle):
    palettes = {
        "breakdown": {
            "outer": {"warm": 0, "cool": 140},
            "inner": {"warm": 10, "cool": 190},
        },
        "buildup": {
            "outer": {"warm": 15, "cool": 180},
            "inner": {"warm": 0, "cool": 230},
        },
        "drop": {
            "outer": {"warm": 230, "cool": 10},
            "inner": {"warm": 20, "cool": 230},
        },
        "normal_a": {
            "outer": {"warm": 220, "cool": 20},
            "inner": {"warm": 20, "cool": 170},
        },
        "normal_b": {
            "outer": {"warm": 30, "cool": 220},
            "inner": {"warm": 220, "cool": 20},
        },
        "normal_c": {
            "outer": {"warm": 255, "cool": 0},
            "inner": {"warm": 0, "cool": 255},
        },
        "normal_d": {
            "outer": {"warm": 160, "cool": 40},
            "inner": {"warm": 0, "cool": 220},
        },
        "normal_e": {
            "outer": {"warm": 40, "cool": 200},
            "inner": {"warm": 180, "cool": 30},
        },
    }

    if state in ("breakdown", "buildup", "drop"):
        return palettes[state]

    normal_keys = ["normal_a", "normal_b", "normal_c", "normal_d", "normal_e"]
    return palettes[normal_keys[palette_cycle % len(normal_keys)]]


def map_features_to_lighting(features):
    times = np.asarray(features["times"], dtype=float)
    rms = np.asarray(features["rms"], dtype=float)
    centroid = np.asarray(features["spectral_centroid"], dtype=float)
    onset = np.asarray(features["onset_strength"], dtype=float)
    flux = np.asarray(features["spectral_flux"], dtype=float)
    bass = np.asarray(features["bass_energy"], dtype=float)
    bass_flux = np.asarray(features["bass_flux"], dtype=float)

    n = min(len(times), len(rms), len(centroid), len(onset), len(flux), len(bass), len(bass_flux))
    times = times[:n]
    rms = rms[:n]
    centroid = centroid[:n]
    onset = onset[:n]
    flux = flux[:n]
    bass = bass[:n]
    bass_flux = bass_flux[:n]

    rms_n = smooth_feature(normalize_feature(rms), alpha=0.18)
    centroid_n = smooth_feature(normalize_feature(centroid), alpha=0.10)
    onset_n = smooth_feature(normalize_feature(onset), alpha=0.12)
    flux_n = smooth_feature(normalize_feature(flux), alpha=0.22)
    bass_n = smooth_feature(normalize_feature(bass), alpha=0.15)
    bass_flux_n = smooth_feature(normalize_feature(bass_flux), alpha=0.12)

    beat_frames = set(
        int(x) for x in np.asarray(features.get("beat_frames", []), dtype=int)
        if 0 <= int(x) < n
    )

    lighting_frames = []
    beat_count = 0
    buildup_counter = 0
    drop_flash_counter = 0
    pre_drop_blackout = 0
    strobe_hold = 0
    palette_cycle = 0

    for i in range(n):
        energy = rms_n[i]
        tone = centroid_n[i]
        hit = onset_n[i]
        motion = flux_n[i]
        low = bass_n[i]
        low_hit = bass_flux_n[i]

        is_beat = i in beat_frames
        if is_beat:
            beat_count += 1

            # change palette every 32 beats
            if beat_count % 32 == 0:
                palette_cycle += 1

        silent = energy < 0.025
        breakdown = energy < 0.18 and low < 0.16 and motion < 0.22
        buildup = motion > 0.42 and hit > 0.25 and low < 0.45 and energy > 0.10
        drop = low > 0.62 and low_hit > 0.30 and energy > 0.40

        if buildup:
            buildup_counter += 1
        else:
            buildup_counter = max(0, buildup_counter - 2)

        # Short blackout just before likely drop
        if buildup_counter > 10 and low_hit < 0.10 and motion > 0.50:
            pre_drop_blackout = max(pre_drop_blackout, 2)

        if drop:
            drop_flash_counter = 3

        if drop and low_hit > 0.30:
            strobe_hold = 3
        elif hit > 0.55 and low_hit > 0.35:
            strobe_hold = max(strobe_hold, 2)

        strobe_on = strobe_hold > 0
        strobe_hold = max(0, strobe_hold - 1)

        if pre_drop_blackout > 0:
            fixtures = {
                "f1": make_fixture_state(0, 0, 0, False),
                "f2": make_fixture_state(0, 0, 0, False),
                "f3": make_fixture_state(0, 0, 0, False),
                "f4": make_fixture_state(0, 0, 0, False),
            }
            pre_drop_blackout -= 1
            lighting_frames.append({
                "time": float(times[i]),
                "fixtures": fixtures,
                "state": "blackout",
            })
            continue

        if silent:
            fixtures = {
                "f1": make_fixture_state(0, 0, 0, False),
                "f2": make_fixture_state(0, 0, 0, False),
                "f3": make_fixture_state(0, 0, 0, False),
                "f4": make_fixture_state(0, 0, 0, False),
            }
            lighting_frames.append({
                "time": float(times[i]),
                "fixtures": fixtures,
                "state": "silent",
            })
            continue

        if breakdown:
            state = "breakdown"
        elif buildup:
            state = "buildup"
        elif drop or drop_flash_counter > 0:
            state = "drop"
        else:
            state = "normal"

        palette = get_palette(state, palette_cycle)

        # stronger beat pulse, weaker onset pulse
        pulse_outer = 70 if is_beat and beat_count % 2 == 1 else 0
        pulse_inner = 70 if is_beat and beat_count % 2 == 0 else 0
        onset_accent = int(12 * hit)

        # motion affects asymmetry more than flash
        left_offset = int(22 * motion)
        right_offset = int(8 * motion)

        base_brightness = 25 + int(95 * energy)
        bass_punch = int(115 * low)
        buildup_ramp = min(110, buildup_counter * 6)

        if state == "breakdown":
            fixtures = {
                "f1": make_fixture_state(8, palette["outer"]["warm"], palette["outer"]["cool"] // 2, False),
                "f2": make_fixture_state(35 + onset_accent, palette["inner"]["warm"], palette["inner"]["cool"], False),
                "f3": make_fixture_state(35 + onset_accent, palette["inner"]["warm"], palette["inner"]["cool"], False),
                "f4": make_fixture_state(8, palette["outer"]["warm"], palette["outer"]["cool"] // 2, False),
            }

        elif state == "buildup":
            fixtures = {
                "f1": make_fixture_state(
                    base_brightness + buildup_ramp + pulse_outer + left_offset,
                    palette["outer"]["warm"],
                    palette["outer"]["cool"],
                    False
                ),
                "f2": make_fixture_state(
                    base_brightness + buildup_ramp + pulse_inner + 18 + left_offset,
                    palette["inner"]["warm"],
                    palette["inner"]["cool"],
                    False
                ),
                "f3": make_fixture_state(
                    base_brightness + buildup_ramp + pulse_inner + 18 + right_offset,
                    palette["inner"]["warm"],
                    palette["inner"]["cool"],
                    False
                ),
                "f4": make_fixture_state(
                    base_brightness + buildup_ramp + pulse_outer + right_offset,
                    palette["outer"]["warm"],
                    palette["outer"]["cool"],
                    False
                ),
            }

        elif state == "drop":
            flash = 45 if drop_flash_counter > 0 else 0
            drop_flash_counter = max(0, drop_flash_counter - 1)

            fixtures = {
                "f1": make_fixture_state(
                    base_brightness + bass_punch + pulse_outer + flash + left_offset,
                    palette["outer"]["warm"],
                    palette["outer"]["cool"],
                    strobe_on
                ),
                "f2": make_fixture_state(
                    base_brightness + bass_punch + pulse_inner + flash,
                    palette["inner"]["warm"],
                    palette["inner"]["cool"],
                    strobe_on
                ),
                "f3": make_fixture_state(
                    base_brightness + bass_punch + pulse_inner + flash,
                    palette["inner"]["warm"],
                    palette["inner"]["cool"],
                    strobe_on
                ),
                "f4": make_fixture_state(
                    base_brightness + bass_punch + pulse_outer + flash + right_offset,
                    palette["outer"]["warm"],
                    palette["outer"]["cool"],
                    strobe_on
                ),
            }

        else:
            outer_warm = palette["outer"]["warm"]
            outer_cool = palette["outer"]["cool"]
            inner_warm = palette["inner"]["warm"]
            inner_cool = palette["inner"]["cool"]

            # very light tone influence so palette stays visible
            tone_shift = int((tone - 0.5) * 20)

            outer_warm = int(np.clip(outer_warm - tone_shift, 0, 255))
            outer_cool = int(np.clip(outer_cool + tone_shift, 0, 255))
            inner_warm = int(np.clip(inner_warm - tone_shift, 0, 255))
            inner_cool = int(np.clip(inner_cool + tone_shift, 0, 255))

            fixtures = {
                "f1": make_fixture_state(
                    base_brightness + pulse_outer + onset_accent + left_offset,
                    outer_warm,
                    outer_cool,
                    False
                ),
                "f2": make_fixture_state(
                    base_brightness + pulse_inner + onset_accent + 10 + left_offset,
                    inner_warm,
                    inner_cool,
                    False
                ),
                "f3": make_fixture_state(
                    base_brightness + pulse_inner + onset_accent + 10 + right_offset,
                    inner_warm,
                    inner_cool,
                    False
                ),
                "f4": make_fixture_state(
                    base_brightness + pulse_outer + onset_accent + right_offset,
                    outer_warm,
                    outer_cool,
                    False
                ),
            }

        lighting_frames.append({
            "time": float(times[i]),
            "fixtures": fixtures,
            "state": state,
            "beat": is_beat,
        })

    return lighting_frames


def print_preview(lighting_frames, step=10):
    print("\nLighting Preview:")
    print(f"Total frames: {len(lighting_frames)}\n")

    for i in range(0, len(lighting_frames), step):
        frame = lighting_frames[i]
        print(
            f"t={frame['time']:.2f}s | "
            f"state={frame.get('state', 'unknown')} | "
            f"f1={frame['fixtures']['f1']} | "
            f"f2={frame['fixtures']['f2']} | "
            f"f3={frame['fixtures']['f3']} | "
            f"f4={frame['fixtures']['f4']}"
        )