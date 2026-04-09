from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import sys
import threading
import time

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mir.features import load_audio, extract_features
from lighting.controller import map_features_to_lighting
from lighting.qlc_sender import QLCController

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Playback control
playback_paused = threading.Event()
playback_paused.set()  # set = running, clear = paused

stop_requested = threading.Event()  # set = stop the current playback loop
current_filepath = None  # path of the most recently uploaded file

# Global state
current_status = {
    'state': 'idle',  # idle, processing, playing, error
    'message': 'Ready to upload audio file',
    'progress': 0,
    'tempo': None,
    'beats': None,
    'duration': None,
    'current_time': 0,
    'brightness': 0,
    'red': 0,
    'green': 0,
    'blue': 0,
    'white': 0,
    'strobe': False
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_status(state, message, progress=None, **kwargs):
    """Update status and broadcast to all connected clients"""

    def clean_value(v):
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return v
        try:
            # handle numpy scalar types
            if hasattr(v, "item"):
                return v.item()
        except Exception:
            pass
        return v

    current_status['state'] = state
    current_status['message'] = message

    if progress is not None:
        current_status['progress'] = int(progress)

    for key, value in kwargs.items():
        current_status[key] = clean_value(value)

    socketio.emit('status_update', current_status)

def process_and_play(filepath):
    """Process audio file and send OSC commands to QLC+"""
    global current_filepath
    current_filepath = filepath
    stop_requested.clear()
    playback_paused.set()  # ensure not stuck in paused state

    try:
        # Step 1: Load audio
        update_status('processing', 'Loading audio file...', 10)
        y, sr = load_audio(filepath)
        duration = float(len(y) / sr)

        # Step 2: Extract features
        update_status('processing', 'Extracting MIR features...', 30)
        features = extract_features(y, sr)

        # Step 3: Map to lighting
        update_status('processing', 'Mapping to lighting...', 50)
        lighting_frames = map_features_to_lighting(features)

        if not lighting_frames:
            update_status('error', 'No lighting frames were generated.', 0)
            return

        # Update with extracted info
        update_status(
            'processing',
            'Ready to send OSC commands',
            70,
            tempo=float(features['tempo']),
            beats=int(len(features['beat_frames'])),
            duration=duration,
            mean_spectral_centroid=float(features.get('mean_spectral_centroid', 0.0)),
            mean_spectral_flux=float(features.get('mean_spectral_flux', 0.0)),
            silent=False
        )

        time.sleep(1)

        # Step 4: Initialize QLC+
        update_status('playing', 'Sending OSC commands to QLC+...', 80)

        try:
            qlc = QLCController(ip="127.0.0.1", port=7700)
        except Exception as e:
            update_status('error', f'Could not connect to QLC+: {str(e)}', 0)
            return

        # Play the audio file
        audio_filename = os.path.basename(filepath)
        playback_paused.set()
        socketio.emit('start_playback', {'filename': audio_filename})

        start_time = time.time()
        frame_index = 0
        last_ui_emit = 0.0
        paused_offset = 0.0  # total time spent paused

        print(f"[PLAYBACK] Total frames: {len(lighting_frames)}")
        print(f"[PLAYBACK] Duration: {duration:.2f}s")

        while frame_index < len(lighting_frames):
            if stop_requested.is_set():
                break

            # If paused, block here and track how long we were paused
            if not playback_paused.is_set():
                pause_start = time.time()
                playback_paused.wait()  # blocks until resumed
                paused_offset += time.time() - pause_start

            elapsed = time.time() - start_time - paused_offset
            frame = lighting_frames[frame_index]
            frame_time = float(frame['time'])

            if elapsed >= frame_time:
                brightness = int(frame['brightness'])
                red = int(frame['red'])
                green = int(frame['green'])
                blue = int(frame['blue'])
                white = int(frame['white'])
                strobe = bool(frame['strobe'])
                strobe_value = 255 if strobe else 0
                
                # Send OSC commands
                for fixture in range(1, 5):
                    qlc.set_fixture(
                        fixture,
                        brightness=brightness,
                        red=red,
                        green=green,
                        blue=blue,
                        white=white,
                        strobe=strobe_value
                    )

                # Only emit UI updates every ~50ms to avoid spamming the browser
                if elapsed - last_ui_emit >= 0.05 or frame_index == len(lighting_frames) - 1:
                    progress = min(99, 80 + int((frame_time / max(duration, 0.001)) * 20))

                    update_status(
                        'playing',
                        f'Playing... {frame_time:.1f}s / {duration:.1f}s',
                        progress,
                        tempo=float(features['tempo']),
                        beats=int(len(features['beat_frames'])),
                        duration=duration,
                        mean_spectral_centroid=float(features.get('mean_spectral_centroid', 0.0)),
                        mean_spectral_flux=float(features.get('mean_spectral_flux', 0.0)),
                        silent=bool(frame.get('gated', False)),
                        current_time=frame_time,
                        brightness=brightness,
                        red=red,
                        green=green,
                        blue=blue,
                        white=white,
                        strobe=strobe
                    )

                    last_ui_emit = elapsed

                # Debug print every 20 frames
                if frame_index % 20 == 0:
                    print(
                        f"[FRAME {frame_index}] "
                        f"t={frame_time:.2f}s "
                        f"brightness={brightness} red={red} green={green} "
                        f"blue={blue} white={white} strobe={strobe}"
                    )

                frame_index += 1
            else:
                time.sleep(0.001)

        # Turn lights off after playback ends (or was stopped)
        time.sleep(0.1)
        qlc.blackout(4)  # Wasn't working when sent once; delay + second send fixed it
        time.sleep(0.05)
        qlc.blackout(4)


        if stop_requested.is_set():
            update_status(
            'idle',
            'Playback complete!',
            100,
            silent=False,
            current_time=duration,
            brightness=0,
            red=0,
            green=0,
            blue=0,
            white=0,
            strobe=False
        )
        else:
            update_status(
            'idle',
            'Playback complete!',
            100,
            silent=False,
            current_time=duration,
            brightness=0,
            red=0,
            green=0,
            blue=0,
            white=0,
            strobe=False
        )

        print("[PLAYBACK] Complete")

    except Exception as e:
        import traceback
        traceback.print_exc()
        update_status('error', f'Error: {str(e)}', 0)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use .wav, .mp3, .flac, .ogg, or .m4a'}), 400
    
    # Save file
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    # Process in background thread
    thread = threading.Thread(target=process_and_play, args=(filename,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

@app.route('/status', methods=['GET'])
def get_status():
    """Get current status"""
    return jsonify(current_status)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status_update', current_status)
    print('Client connected')

@socketio.on('toggle_pause')
def handle_toggle_pause():
    """Toggle pause/resume for playback"""
    if playback_paused.is_set():
        playback_paused.clear()
        print('[PLAYBACK] Paused')
        # Turn lights off while paused
        try:
            qlc = QLCController(ip="127.0.0.1", port=7700)
            qlc.blackout(4)
        except Exception:
            pass
        socketio.emit('playback_paused', {'paused': True})
    else:
        playback_paused.set()
        print('[PLAYBACK] Resumed')
        socketio.emit('playback_paused', {'paused': False})

@socketio.on('stop_playback')
def handle_stop_playback():
    """Stop current playback and reset state"""
    stop_requested.set()
    playback_paused.set()  # unblock any paused thread so it can see the stop flag
    try:
        qlc = QLCController(ip="127.0.0.1", port=7700)
        qlc.blackout(4)
    except Exception:
        pass
    print('[PLAYBACK] Stopped by user')
    # State reset is handled by process_and_play once the loop exits;
    # emit immediately so the UI updates right away.
    socketio.emit('status_update', {
        **current_status,
        'state': 'idle',
        'message': 'Playback stopped.',
        'progress': 0,
        'brightness': 0,
        'warm': 0,
        'cool': 0,
        'strobe': False,
        'current_time': 0,
    })

@socketio.on('restart_playback')
def handle_restart_playback():
    """Restart the current song from the beginning"""
    global current_filepath
    if not current_filepath or not os.path.exists(current_filepath):
        socketio.emit('status_update', {**current_status, 'state': 'error', 'message': 'No song loaded to restart.'})
        return
    filepath = current_filepath
    stop_requested.set()
    playback_paused.set()
    print('[PLAYBACK] Restarting...')
    # Give the running thread a moment to exit before launching a new one
    def _delayed_restart():
        time.sleep(0.3)
        thread = threading.Thread(target=process_and_play, args=(filepath,))
        thread.daemon = True
        thread.start()
    t = threading.Thread(target=_delayed_restart)
    t.daemon = True
    t.start()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print("=" * 60)
    print("  Music-to-DMX Lighting Control Web Server")
    print("=" * 60)
    print("\n✓ Server starting...")
    print("✓ Open your browser and go to: http://localhost:5000")
    print("✓ Make sure QLC+ is running with OSC input on port 7700")
    print("\nPress Ctrl+C to stop the server\n")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
