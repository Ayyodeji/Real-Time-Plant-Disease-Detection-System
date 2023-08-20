// Get access to the webcam
async function startVideo() {
    const videoElement = document.getElementById('video');
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = stream;
}

startVideo();

// Capture video frames and send to Flask
const videoElement = document.getElementById('video');
const predictionElement = document.getElementById('prediction');

videoElement.addEventListener('play', () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    setInterval(() => {
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg'); // Convert to base64
        sendFrame(imageData);
    }, 1000); // Adjust interval as needed
});

// Send video frame to Flask backend
async function sendFrame(frameData) {
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ frame_data: frameData }),
    });
    const prediction = await response.json();
    predictionElement.textContent = `Prediction: ${prediction.class} (${prediction.confidence})`;
}
