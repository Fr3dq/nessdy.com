function loadTextFile() {
    fetch('static/policy.txt')
        .then(response => {
            if (!response.ok) {
                throw new Error('File not found');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('textContent').textContent = data;
        })
        .catch(error => {
            document.getElementById('textContent').textContent = "Error loading file.";
            console.error('Error:', error);
        });
}

window.onload = loadTextFile;