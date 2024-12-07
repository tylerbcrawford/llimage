const dropArea = document.getElementById("drop-area");
const fileElem = document.getElementById("fileElem");
const messageDiv = document.getElementById("message");

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop zone when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add('hover');
}

function unhighlight(e) {
    dropArea.classList.remove('hover');
}

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);
dropArea.addEventListener('click', () => fileElem.click());
fileElem.addEventListener('change', handleFiles, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles({target: {files: files}});
}

function handleFiles(e) {
    const files = e.target.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type !== 'application/pdf') {
            showMessage('Please upload a PDF file.', 'error');
            return;
        }
        uploadFile(file);
    }
}

function uploadFile(file) {
    showMessage('Processing...', 'info');
    const formData = new FormData();
    formData.append('file', file);

    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {throw new Error(text)});
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'LLiMage_output.txt';
        document.body.appendChild(a);
        a.click();
        a.remove();
        showMessage('Processing complete! Check your downloads.', 'success');
    })
    .catch(error => {
        console.error(error);
        showMessage('Error processing file. Please try again.', 'error');
    });
}

function showMessage(text, type = 'info') {
    messageDiv.textContent = text;
    messageDiv.className = type;
}
