import os
import sys

# allow imports from sibling folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mir.features import load_audio, extract_features
from lighting.controller import map_features_to_lighting, print_preview


def main():
    file_path = input("Enter path to audio file (.mp3, .wav, etc.): ").strip()

    if not os.path.isfile(file_path):
        print("Error: file not found.")
        return

    print("Loading audio...")
    y, sr = load_audio(file_path)

    print("Extracting MIR features...")
    features = extract_features(y, sr)

    print(f"Estimated tempo: {features['tempo']:.2f} BPM")
    print(f"Detected beats: {len(features['beat_frames'])}")
    if 'mean_spectral_centroid' in features:
        print(f"Mean spectral centroid: {features['mean_spectral_centroid']:.2f} Hz")
    if 'mean_spectral_flux' in features:
        print(f"Mean spectral flux: {features['mean_spectral_flux']:.3f}")

    print("Mapping features to lighting...")
    lighting_frames = map_features_to_lighting(features)

    print_preview(lighting_frames, step=20)


if __name__ == "__main__":
    main()
