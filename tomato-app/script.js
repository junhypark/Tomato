function handleFileUpload(event) {
    const input = event.target;
    if (input.files.length === 0) {
        console.error('No file selected');
        return;
    }
    const fileName = input.files[0].name;
    const fileLabelId = `${input.id}-file-name`;
    const fileLabel = document.getElementById(fileLabelId);

    if (fileLabel) {
        fileLabel.textContent = fileName;
        console.log(`File selected: ${fileName}`);
        const nextButton = input.closest('.step').querySelector('.next-button');
        if (nextButton) {
            nextButton.style.display = 'block';
        }
    } else {
        console.error(`Label element with id ${fileLabelId} not found`);
    }
}

async function uploadFiles() {
    const videoInput = document.getElementById('video');
    const fileInput = document.getElementById('file');

    if (!videoInput.files.length || !fileInput.files.length) {
        console.error('No files selected');
        return;
    }

    const formData = new FormData();
    formData.append('video', videoInput.files[0]);
    formData.append('file', fileInput.files[0]);

    console.log('Uploading files...');

    try {
        const response = await fetch('http://127.0.0.1:3001/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Files uploaded successfully:', result);
            nextStep(3);
            window.resultFilePath = result.output;
        } else {
            const error = await response.json();
            console.error('File upload failed', error);
        }
    } catch (error) {
        console.error('Failed to fetch:', error);
    }
}

function nextStep(step) {
    console.log(`Moving to step: ${step}`);

    document.querySelectorAll('.step').forEach((el, index) => {
        el.classList.toggle('active', index + 1 === step);
    });

    document.querySelectorAll('.step-item').forEach((el, index) => {
        el.classList.toggle('active', index + 1 === step);
    });

    updateNextButton(step);

    if (step === 4) {
        const downloadLink = document.getElementById('download-link');
        downloadLink.href = `http://127.0.0.1:3001/download?path=${encodeURIComponent(window.resultFilePath)}`;
        downloadLink.style.display = 'block';
    }
}

function updateNextButton(step) {
    document.querySelectorAll('.next-button').forEach((button, index) => {
        button.style.display = (index + 1 === step) ? 'block' : 'none';
    });
}

function goToStep(step) {
    console.log(`Go to step: ${step}`);
    nextStep(step);
}

document.getElementById('video').addEventListener('change', handleFileUpload);
document.getElementById('file').addEventListener('change', handleFileUpload);
