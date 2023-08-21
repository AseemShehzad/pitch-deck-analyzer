document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect('http://localhost:5000');
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const uploadContainer = document.querySelector('.upload-container');
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
        messageContainer.style.display = 'block';
        messageContainer.classList.remove('fade-out');

        setTimeout(() => {
            messageContainer.classList.add('fade-out');
            setTimeout(() => {
                messageContainer.style.display = 'none';
            }, 1000);
        }, 2000);
    }

    function handleFiles(files) {
        spinner.style.display = "block";
        const acceptedFileType = "application/pdf";
        const file = files[0];

        if (file.type !== acceptedFileType) {
            showMessage("Please upload only .pdf files!");
            spinner.style.display = "none";
            return;
        }

        const fileSizeInMB = file.size / (1024 * 1024);
        if (fileSizeInMB > 10) {
            showMessage("File size should be under 10 MB!");
            spinner.style.display = "none";
            return;
        }

        // Read the file and send to server using WebSocket
        const reader = new FileReader();
        reader.onload = function() {
            console.log("Emitting process_file event to the server");
            socket.emit('process_file', {
                file: reader.result.split(',')[1], 
                filename: file.name
            });
        };
        reader.readAsDataURL(file);
    }
    
    socket.on('file_response', function(data) {
        console.log("Received file_response event from the server:", data);
    
        // Re-query the iframe here
        let outputIframe = document.querySelector('.output-iframe');
    
        if (data.error) {
            showMessage(data.error);
        } else {
            if (outputIframe) {
                outputIframe.srcdoc = data.content;
                outputIframe.style.display = "block"; // Make sure to display the iframe when content is received
                if (window.getComputedStyle(uploadContainer).display !== "none") {
                    uploadContainer.classList.add('hidden');
                }
            } else {
                console.error("outputIframe is not available in the DOM");
            }
        }
        spinner.style.display = "none"; // Hide the spinner
    });
    
    socket.on('error_response', function(data) {
        console.error("Received error_response event:", data);
        showMessage(data.error);
        spinner.style.display = "none";
    });
    
    socket.on('error', function(error) {
        console.error("General Socket error:", error);
        spinner.style.display = "none";
    });

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

    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            handleFiles(this.files);
        }
    });
});
