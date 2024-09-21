document.getElementById('uploadForm').onsubmit = async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput').files[0];
    if (!fileInput) return;

    const formData = new FormData();
    formData.append('file', fileInput);

    const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    document.getElementById('predictionResult').innerText = result.prediction ? `Prediction: ${result.prediction}` : `Error: ${result.error}`;
};
