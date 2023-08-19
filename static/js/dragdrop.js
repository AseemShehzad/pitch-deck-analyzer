document.addEventListener("DOMContentLoaded", function() {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const uploadContainer = document.querySelector('.upload-container');
    const outputIframe = document.querySelector('.output-iframe');
    const spinner = document.getElementById("spinner");

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropZone.style.background = "#e6e6e6";
    }

    function unhighlight() {
        dropZone.style.background = "";
    }

    function showMessage(message) {
        const messageContainer = document.getElementById('messageContainer');
        messageContainer.innerHTML = message;
        messageContainer.style.display = 'block'; // show the message container
        messageContainer.classList.remove('fade-out'); // if it already has the fade-out class, remove it
    
        setTimeout(() => {
            messageContainer.classList.add('fade-out'); // Add the fade-out class after 5 seconds
            setTimeout(() => {
                messageContainer.style.display = 'none';
                messageContainer.classList.remove('fade-out'); // Reset for next use
            }, 1000); // 1s is the duration of the fade-out animation
        }, 2000); // 2 seconds delay
    }

    function handleFiles(files) {
        spinner.style.display = "block"; // Show the spinner
        const acceptedFileType = "application/pdf";
        const file = files[0];

        if (file.type !== acceptedFileType) {
            showMessage("Please upload only .pdf files!");
            spinner.style.display = "none";
            return;
        }

        const fileSizeInMB = file.size / (1024 * 1024); // Convert bytes to MB
        if (fileSizeInMB > 10) {
            showMessage("File size should be under 10 MB!");
            spinner.style.display = "none";
            return;
        }

        fileInput.files = files;
        document.getElementById("uploadForm").submit();
    }

    // Drag and Drop Event Listeners
    ["dragenter", "dragover"].forEach(eventName => dropZone.addEventListener(eventName, (e) => {
        preventDefaults(e);
        highlight();
    }, false));

    ["dragleave", "drop"].forEach(eventName => dropZone.addEventListener(eventName, (e) => {
        preventDefaults(e);
        unhighlight();
        if (eventName === "drop") {
            handleFiles(e.dataTransfer.files);
        }
    }, false));

    // File Input Change Listener
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            handleFiles(this.files);
        }
    });

    // If output is visible, hide the upload container
    if (outputIframe && window.getComputedStyle(outputIframe).display !== "none") {
        uploadContainer.classList.add('hidden');
    }
});