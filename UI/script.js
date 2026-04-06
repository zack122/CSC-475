// Connect to WebSocket (same-origin)
const socket = io();

// DOM elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const statusMessage = document.getElementById('status-message');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const infoPanel = document.getElementById('info-panel');
const statusPanel = document.getElementById('status-panel');

const pauseBtn = document.getElementById('pause-btn');
const stopBtn = document.getElementById('stop-btn');
const restartBtn = document.getElementById('restart-btn');
const newSongBtn = document.getElementById('new-song-btn');

let hasLoadedSong = false;

// Pause button
pauseBtn.addEventListener('click', () => {
    socket.emit('toggle_pause');
});
socket.on('playback_paused', (data) => {
    if (data.paused) {
        pauseBtn.textContent = 'Resume';
        if (audioPlayer) audioPlayer.pause();
    } else {
        pauseBtn.textContent = 'Pause';
        if (audioPlayer) audioPlayer.play();
    }
});

// Stop button — halt playback, reset UI values to zero
stopBtn.addEventListener('click', () => {
    socket.emit('stop_playback');
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
    }
    resetPlaybackUI();
});

// Restart button — replay the same song from the beginning
restartBtn.addEventListener('click', () => {
    socket.emit('restart_playback');
    pauseBtn.textContent = 'Pause';
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
    }
});

// New Song button — stop playback and clear everything so user can upload a new file
newSongBtn.addEventListener('click', () => {
    socket.emit('stop_playback');
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer = null;
    }
    if (audioBlobUrl) {
        URL.revokeObjectURL(audioBlobUrl);
        audioBlobUrl = null;
    }
    fileInput.value = '';
    hasLoadedSong = false;
    resetPlaybackUI();
    infoPanel.style.display = 'none';
    statusMessage.textContent = 'Ready to upload audio file';
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
    statusPanel.className = 'panel';
    updateControlVisibility('idle');
});

function resetPlaybackUI() {
    // Reset DMX channel bars to zero
    document.getElementById('brightness-bar').style.width = '0%';
    document.getElementById('brightness-val').textContent = '0';
    document.getElementById('warm-bar').style.width = '0%';
    document.getElementById('warm-val').textContent = '0';
    document.getElementById('cool-bar').style.width = '0%';
    document.getElementById('cool-val').textContent = '0';
    document.getElementById('strobe-indicator').classList.remove('active');
    document.getElementById('strobe-val').textContent = 'OFF';
    document.getElementById('silence-value').textContent = 'OFF';
    document.getElementById('time-value').textContent = '0.0';
}

function updateControlVisibility(state) {
    const isActive = state === 'processing' || state === 'playing';
    const isPlaying = state === 'playing';

    pauseBtn.style.display = isPlaying ? 'inline-block' : 'none';
    stopBtn.style.display = isActive ? 'inline-block' : 'none';
    restartBtn.style.display = hasLoadedSong ? 'inline-block' : 'none';
    newSongBtn.style.display = hasLoadedSong ? 'inline-block' : 'none';

    if (!isPlaying) {
        pauseBtn.textContent = 'Pause';
    }
}

// File upload handlers
dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        uploadFile(fileInput.files[0]);
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('hover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('hover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('hover');
    
    if (e.dataTransfer.files.length > 0) {
        uploadFile(e.dataTransfer.files[0]);
    }
});

// Audio playback element
let audioPlayer = null;
let audioBlobUrl = null;

// Upload file to server
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    statusMessage.textContent = 'Uploading file...';

    // Prepare audio for playback using the local file (no server round-trip needed)
    if (audioBlobUrl) {
        URL.revokeObjectURL(audioBlobUrl);
    }
    audioBlobUrl = URL.createObjectURL(file);

    // Pre-create the audio element during user gesture so autoplay is allowed
    if (audioPlayer) {
        audioPlayer.pause();
    }
    audioPlayer = new Audio(audioBlobUrl);
    audioPlayer.preload = 'auto';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Upload successful:', data);
    })
    .catch(error => {
        statusMessage.textContent = 'Upload failed: ' + error.message;
        console.error('Upload error:', error);
    });
}

// Start audio playback when server signals
socket.on('start_playback', () => {
    console.log('Starting audio playback');
    if (audioPlayer) {
        audioPlayer.currentTime = 0;
        audioPlayer.play().catch(err => {
            console.error('Audio playback failed:', err);
            statusMessage.textContent += ' (Audio playback blocked — click the page first)';
        });
    }
});

// WebSocket: Receive status updates
socket.on('status_update', (status) => {
    // Update status message
    statusMessage.textContent = status.message;

    // Update progress bar
    progressFill.style.width = status.progress + '%';
    progressText.textContent = status.progress + '%';

    // Stop audio when playback ends or errors
    if ((status.state === 'idle' || status.state === 'error') && audioPlayer) {
        audioPlayer.pause();
        if (status.state === 'idle') {
            audioPlayer = null;
        }
    }

    // Track whether a song has ever been loaded this session
    if (status.state === 'processing' || status.state === 'playing') {
        hasLoadedSong = true;
    }

    // Update button visibility
    updateControlVisibility(status.state);

    // Update status panel color based on state
    statusPanel.className = 'panel status-' + status.state;
    
    // Update audio info
    if (status.tempo !== null) {
        document.getElementById('tempo-value').textContent = status.tempo.toFixed(1);
        document.getElementById('beats-value').textContent = status.beats;
        document.getElementById('duration-value').textContent = status.duration.toFixed(1);
        infoPanel.style.display = 'block';
    }
    if (status.mean_spectral_centroid !== undefined) {
        const v = Number(status.mean_spectral_centroid);
        if (!Number.isNaN(v)) {
            document.getElementById('centroid-value').textContent = v.toFixed(1);
        }
    }
    if (status.mean_spectral_flux !== undefined) {
        const v = Number(status.mean_spectral_flux);
        if (!Number.isNaN(v)) {
            document.getElementById('flux-value').textContent = v.toFixed(3);
        }
    }
    
    if (status.current_time !== undefined) {
        document.getElementById('time-value').textContent = status.current_time.toFixed(1);
    }
    if (typeof status.silent === 'boolean') {
        document.getElementById('silence-value').textContent = status.silent ? 'ON' : 'OFF';
    }
    
    // Update lighting visualization
    updateLightingViz(status);
});

function updateLightingViz(status) {
    // Update brightness
    const brightnessBar = document.getElementById('brightness-bar');
    const brightnessVal = document.getElementById('brightness-val');
    const brightnessPercent = (status.brightness / 255) * 100;
    brightnessBar.style.width = brightnessPercent + '%';
    brightnessVal.textContent = status.brightness;
    
    // Update warm
    const warmBar = document.getElementById('warm-bar');
    const warmVal = document.getElementById('warm-val');
    const warmPercent = (status.warm / 255) * 100;
    warmBar.style.width = warmPercent + '%';
    warmVal.textContent = status.warm;
    
    // Update cool
    const coolBar = document.getElementById('cool-bar');
    const coolVal = document.getElementById('cool-val');
    const coolPercent = (status.cool / 255) * 100;
    coolBar.style.width = coolPercent + '%';
    coolVal.textContent = status.cool;
    
    // Update strobe
    const strobeIndicator = document.getElementById('strobe-indicator');
    const strobeVal = document.getElementById('strobe-val');
    if (status.strobe) {
        strobeIndicator.classList.add('active');
        strobeVal.textContent = 'ON';
    } else {
        strobeIndicator.classList.remove('active');
        strobeVal.textContent = 'OFF';
    }
}

// WebSocket connection status
socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    statusMessage.textContent = 'Connection lost. Please refresh.';
    statusPanel.className = 'panel status-error';
});
