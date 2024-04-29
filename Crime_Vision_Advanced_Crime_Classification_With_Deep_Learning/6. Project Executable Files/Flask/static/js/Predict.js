const uploadBtn = document.getElementById('uploadBtn');
const predictBtn = document.getElementById('predictBtn');
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const predictResult = document.getElementById('predictResult')

uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        // Display the uploaded image
        const uploadedImage = document.getElementById('uploadedImage');
        uploadedImage.src = reader.result;
        uploadedImage.style.display = 'block';

        // Show the predict button
        predictBtn.style.display = 'inline-block';
    };
    reader.readAsDataURL(file);
});

predictBtn.addEventListener('click', () => {
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);
   
    // Get the prediction result by sending a request to '/predict' endpoint
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(prediction => {
        // alert('Prediction: ' + prediction);     
        predictResult.innerHTML = prediction;
    })
    .catch(error => {
        console.error('Error predicting image:', error);
    });
});