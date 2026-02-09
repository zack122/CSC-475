# Project Design Specification: Music-Driven DMX Lighting Control System

## 1. Project Description
We propose a music-driven lighting control system that maps audio features extracted from musical recordings to DMX lighting parameters in real-time. The system performs Music Information Retrieval (MIR) to estimate rhythmic and structural cues (e.g., beat/onset strength, energy, spectral brightness, and harmonic descriptors) and translates these cues into stable, musically meaningful lighting changes. 

The goal is to move beyond simple "sound-to-light" triggers and create a system that understands musicality—adjusting intensity, colour, strobe rate, and scene transitions based on the audio's actual characteristics.

System performance will be evaluated based on latency, feature stability, and subjective user feedback on musical coherence and the responsiveness of the lighting output.


## 2. Tools, Datasets, and Literature
* **Software & Libraries:** Python, `Librosa` (Feature Extraction), `Essentia`, `PyTorch`, `QLC+` (Lighting Control), and `OSC/Art-Net` protocols.
* **Data Sets:** * **Music4All:** Used for offline experiments to test genre- and mood-informed mapping strategies.
    * **GTZAN:** Used for baseline rhythmic and spectral feature validation.
    * **Custom Live Recordings:** For testing real-time latency and onset accuracy.
* **Literature:** Grounded in MIR research regarding beat tracking, onset detection, and cross-modal mapping (Audio-to-Visual).

## 3. Related Work
*(This section summarizes the 15-20 references required for the project. A full bibliography is provided at the end of this document.)*

Current research in music-to-light mapping often focuses on low-level features like RMS. Our project seeks to integrate higher-level structural analysis. We are referencing state-of-the-art methods in beat tracking (e.g., Böck et al.) and spectral analysis to ensure the lighting feels "intelligent" rather than random. We are exploring how Chroma features can represent harmonic "warmth" through colour temperature and how onset detection can drive percussive lighting elements.

## 4. Timeline
| Date | Milestone |
| :--- | :--- |
| **Late Feb** | Design Specification & Literature Review Submission |
| **Mid March** | Initial Feature Extraction Pipeline & DMX Linkage |
| **Early April** | Final Logic Mapping & System Testing |
| **Late April** | Final Report Submission (ISMIR LaTeX Format) |

## 5. Team Roles
* **Blake Stewart (Team Lead & Integration):** Overall project oversight, pipeline management from audio input to QLC+ output.
* **Leo DeRosa (DMX Mapping & Final Editing):** Logic for turning MIR features into lighting commands; final report polishing.
* **Zachary Zhao (MIR Feature Extraction & Implementation):** Implementation of tempo, beat, and spectral feature extraction.
* **Tom Yasinchuk (MIR Feature Extraction & Testing):** MIR component implementation and end-to-end system testing.

---

## 6. Personal Objectives & Performance Indicators

## Blake Stewart
### Objective 1: System Integration and Real-Time Pipeline
* **PI1 (basic):** Set up the project repository and basic environment requirements.
* **PI2 (basic):** Ensure audio can be streamed into the system via file buffer or live input.
* **PI3 (expected):** Integrate all MIR scripts from team members into a single, unified control loop.
* **PI4 (expected):** Create a latency-monitoring tool to ensure lighting stays synced with audio within 20ms.
* **PI5 (advanced):** Implement a GUI or dashboard to monitor extracted features and DMX output values in real-time.

## Leo DeRosa
### Objective 1: DMX Mapping Logic and Scene Management
* **PI1 (basic):** Establish a functional connection between Python and QLC+ via OSC.
* **PI2 (basic):** Map audio energy (RMS) to a single DMX dimmer channel.
* **PI3 (expected):** Create a mapping logic where spectral centroid changes the colour palette of the lights.
* **PI4 (expected):** Implement a "strobe" trigger based on onset strength or percussive peaks.
* **PI5 (advanced):** Develop scene transition logic that detects structural changes (verse to chorus) to trigger DMX scene swaps.

## Zachary Zhao
### Objective 1: Rhythmic Feature Extraction
* **PI1 (basic):** Implement basic tempo (BPM) estimation using Librosa.
* **PI2 (basic):** Extract rhythmic onsets from various music genres.
* **PI3 (expected):** Implement real-time beat tracking that adjusts to local tempo drift.
* **PI4 (expected):** Extract "pulse clarity" to determine how "steady" the light movement should be.
* **PI5 (advanced):** Implement a multi-band onset detector to separate "kick drum" flashes from "snare" flashes.

## Tom Yasinchuk
### Objective 1: Spectral & Structural Analysis
* **PI1 (basic):** Calculate Mean Spectral Centroid and Flux for an audio stream.
* **PI2 (basic):** Implement a "Silence detection" gate to turn off lights when audio stops.
* **PI3 (expected):** Implement Harmonic/Percussive Source Separation (HPSS) to drive different light groups.
* **PI4 (expected):** Conduct "User-in-the-loop" testing to calibrate the "aggressiveness" of the lighting behaviour.
* **PI5 (advanced):** Use Chroma features to map musical keys to specific "mood-based" colour temperatures.

---

## 7. References
1. A. Author and B. Author, “The title of the conference paper,” in Proc. of the 18th Int. Society for Music Information Retrieval Conf., Suzhou, China, 2017, pp. 111–117.
2. George Tzanetakis. mir_book: Companion Code for Music Information Retrieval. GitHub repository, 2020. Accessed February 2026. https://github.com/gtzan/mir_book

4. [Reference 3]
5. [Reference 4]
6. [Reference 5]
7. [Reference 6]
8. [Reference 7]
9. [Reference 8]
10. [Reference 9]
11. [Reference 10]
12. [Reference 11]
13. [Reference 12]
14. [Reference 13]
15. [Reference 14]
16. [Reference 15]
