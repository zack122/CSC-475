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

## 3. Timeline
| Date | Milestone |
| :--- | :--- |
| **Late Feb** | Design Specification & Literature Review Submission |
| **Mid March** | Initial Feature Extraction Pipeline & DMX Linkage |
| **Early April** | Final Logic Mapping & System Testing |
| **Late April** | Final Report Submission (ISMIR LaTeX Format) |

## 4. Team Roles
* **Blake Stewart (Team Lead & Integration):** Overall project oversight, pipeline management from audio input to QLC+ output.
* **Leo DeRosa (DMX Mapping & Final Editing):** Logic for turning MIR features into lighting commands; final report polishing.
* **Zachary Zhao (MIR Feature Extraction & Implementation):** Implementation of tempo, beat, and spectral feature extraction.
* **Tom Yasinchuk (MIR Feature Extraction & Testing):** MIR component implementation and end-to-end system testing.

---

## 5. Personal Objectives & Performance Indicators

## Blake Stewart
### Objective 1: System Integration and Real-Time Pipeline.
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
## 6. Related Work
*(This section summarizes the 15-20 references required for the project. A full bibliography is provided at the end of this document.)*

Current research in music-to-light mapping often focuses on low-level features like RMS. Our project seeks to integrate higher-level structural analysis. We are referencing state-of-the-art methods in beat tracking (e.g., Böck et al.) and spectral analysis to ensure the lighting feels "intelligent" rather than random. We are exploring how Chroma features can represent harmonic "warmth" through colour temperature and how onset detection can drive percussive lighting elements.

## 7. References

1. G. Tzanetakis, *Music Information Retrieval Book – Companion Code Repository*, GitHub repository, https://github.com/gtzan/mir_book, accessed Feb 2026.
2. MusicInformationRetrieval.com contributors, “Symbolic Representations,” *Music Information Retrieval*, https://musicinformationretrieval.com/content/2_music_representations/symbolic_representations.html, accessed Feb. 2026.
3. Roland, *VC-1-DMX Video Lighting Converter Product Page*, https://proav.roland.com/global/products/vc-1-dmx, accessed Feb. 2026
4. MaestroDMX, *MaestroDMX: Intelligent Music-Driven Lighting Controller*, https://maestrodmx.com, accessed Feb. 2026
5. D. M. McDermott, “Seeing Harmony, Hearing Color,” *Data Science by Design* (blog), https://datasciencebydesign.org/blog/seeing-harmony-hearing-color, accessed Feb 2026.
6. Ellis, D. P. W. (2007). Beat Tracking by Dynamic Programming. Journal of New Music Research, 36(1), 51–60. https://doi.org/10.1080/09298210701653344
7. J. P. Bello, L. Daudet, S. Abdallah, C. Duxbury, M. Davies and M. B. Sandler, "A tutorial on onset detection in music signals," in IEEE Transactions on Speech and Audio Processing, vol. 13, no. 5, pp. 1035-1047, Sept. 2005, doi: 10.1109/TSA.2005.851998.
8. Python Software Foundation. (n.d.). Python documentation – Release 3.14.3. https://docs.python.org/3/ accessed Feb 2026.
9. McFee, B., Raffel, C., Liang, D., Ellis, D. P., McVicar, M., Battenberg, E., & Nieto, O. (2015). librosa: Audio and music signal analysis in Python (Version 0.11.0). https://librosa.org/doc/latest/ accessed Feb 2026.
10. Bogdanov, D., Wu, H., Gómez, E., Herrera, P., Mayor, O., Nayak, R., & Serra, X. (2013). Essentia: A C++ library for audio and music analysis. https://essentia.upf.edu/ accessed Feb 2026.
11. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., … & Chintala, S. (2019). PyTorch: An imperative style, high‑performance deep learning library. https://pytorch.org/docs/stable/ accessed Feb 2026.
12. Gorski, M., & QLC+ Developers. (n.d.). QLC+ documentation. https://www.qlcplus.org/docs/ accessed Feb 2026.
13. Wright, M., Freed, A., & Momeni, A. (2002). Open Sound Control 1.0 specification. https://opensoundcontrol.org/specification/ accessed Feb 2026.
14. Howell, W., & Artistic Licence Holdings Ltd. (2019). Art‑Net 4 specification. https://artisticlicence.com/WebSiteMaster/ProtocolDownloads/art-net.pdf accessed Feb 2026.
15. Vall, A., Ferraro, E., & Montoliu, R. (2020). Music4All: A large‑scale dataset for music information retrieval. https://sites.google.com/upf.edu/music4all accessed Feb 2026.
16. Tzanetakis, G., & Cook, P. (2002). Musical genre classification of audio signals. https://urosevic.net/df/gtzan/ accessed Feb 2026.
