// Basic JS for drag-and-drop of MP3

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
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
    const files = e.dataTransfer.files;
    handleFiles(files);
});

function handleFiles(files) {
    if (files.length === 0) return;
    const file = files[0];
    if (file.type !== 'audio/mpeg') {
        alert('Please drop an MP3 file.');
        return;
    }
    console.log('File received:', file.name);
    // further processing here
}
