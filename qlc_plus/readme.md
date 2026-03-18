# 🎵 Music-to-DMX Lighting System (QLC+ v4.14 Setup Guide)

This guide walks you through setting up **QLC+ v4.14.4** and connecting it to the web server so your **audio-driven lighting system** works correctly.

---

# 🚀 Overview

This project converts audio into lighting in real time:

```text
Audio → MIR Features → Lighting Mapping → OSC → QLC+ → Lights
```

QLC+ receives OSC messages from the server and controls:

* Brightness
* Warm color
* Cool color
* Strobe

---

# 🧰 Requirements

## Software

* **QLC+ v4.14.4**
* **Python 3.8+**
* Required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

## Ports

* OSC runs on:

  ```text
  127.0.0.1:7700
  ```

---

# 🎛️ QLC+ Setup (v4.14.4)

---

## 1. Open the provided workspace

1. Launch **QLC+ v4.14.4**
2. Go to:

   ```text
   File → Open
   ```
3. Open the provided:

   ```text
   .qxw file
   ```

---

## 2. Enable OSC input

1. Go to:

   ```text
   Inputs/Outputs tab
   ```

2. Under **Universe 1**:

   * Set **Input** to:

     ```text
     OSC
     ```
   * Check the enable box ✅

3. Ensure:

   ```text
   Port: 7700
   ```

---

## 3. Verify Virtual Console layout

Go to:

```text
Virtual Console tab
```

You should see **4 controls**:

| Control    | Type   | Purpose        |
| ---------- | ------ | -------------- |
| Brightness | Slider | Main intensity |
| Warm       | Slider | Warm color     |
| Cool       | Slider | Cool color     |
| Strobe     | Button | Strobe effect  |

---

## 4. Verify OSC mappings

Each widget should already be mapped to these OSC paths:

```text
/mir/brightness
/mir/warm
/mir/cool
/mir/strobe
```

### To check:

1. Right-click a widget
2. Click:

   ```text
   Assign Input
   ```
3. Confirm it shows:

   ```text
   Universe 1 → OSC → /mir/...
   ```

---

## 5. Test QLC+ manually

Before using the server:

* Move sliders manually
* Press strobe button

👉 This confirms QLC+ is working correctly

---

# 🖥️ Running the Server

---

## 1. Navigate to project

```bash
cd CSC-475
```

---

## 2. Activate virtual environment

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start the server

```bash
python ui/server.py
```

You should see:

```text
Running on http://127.0.0.1:5000
```

---

## 5. Open the web app

Go to:

```text
http://localhost:5000
```

---

# 🎵 Using the System

---

## 1. Upload an audio file

Supported formats:

* `.wav`
* `.mp3`
* `.flac`
* `.ogg`
* `.m4a`

---

## 2. Watch the system run

The system will:

1. Extract audio features
2. Map them to lighting values
3. Send OSC messages to QLC+
4. Update lighting in real time

---

## 🎯 Expected Behavior

In QLC+:

* **Brightness slider** moves with energy (RMS)
* **Warm/Cool sliders** change with spectral content
* **Strobe button** activates on strong onsets

In the browser:

* Live progress updates
* Current time
* Lighting values

---

# 🔌 How the Connection Works

The server sends OSC messages like:

```text
/mir/brightness → 0–255
/mir/warm       → 0–255
/mir/cool       → 0–255
/mir/strobe     → 0 or 255
```

QLC+ receives these and updates the mapped widgets.

---

# 🚨 Troubleshooting

---

## ❌ QLC+ not responding

Check:

* OSC input enabled
* Port = 7700
* QLC+ running BEFORE server

---

## ❌ Widgets not moving

Check:

* Correct OSC mapping (`/mir/...`)
* Re-run Auto Detect if needed

---

## ❌ Server stuck at 80%

Fixed by:

* ensuring correct data types
* verifying playback loop

---

## ❌ No connection

Make sure:

```text
IP: 127.0.0.1
Port: 7700
```

---

# 🧠 Notes

* QLC+ v4 is required (v5 UI is different)
* This project uses **Virtual Console mapping**, not direct DMX paths
* OSC must match exactly between server and QLC+

---

# 🎉 Done

Once everything is set up:

```text
Upload audio → Lights respond in real-time 🎵💡
```

---

# 🚀 Optional Improvements

* Smooth lighting transitions
* Sync audio playback with lights
* Add more fixture channels (RGB, movement)
* Expand UI controls

---

Enjoy the light show 🔥
