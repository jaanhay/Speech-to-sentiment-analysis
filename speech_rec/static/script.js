const uploadForm = document.getElementById("upload")

uploadForm.addEventListener('submit', function(e) {
    e.preventDefault();
    let file = uploadForm.upload_f.files[0]; // Accessing the form element directly

    let formData = new FormData();
    formData.append('file', file);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        document.getElementById('prediction').textContent = result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


