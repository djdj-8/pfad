document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const styledImage = document.getElementById('styled-image');
    const imageContainer = document.getElementById('image-container');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        });

    document.addEventListener('keydown', function(event) {
        if (event.code === 'Space') {
            event.preventDefault();
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageBlob = canvas.toBlob(function(blob) {
                const formData = new FormData();
                formData.append('image', blob);
                fetch('/process_image', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.blob())
                .then(blob => {
                    const imgURL = URL.createObjectURL(blob);
                    styledImage.src = imgURL;
                    styledImage.style.display = 'block';
                    imageContainer.style.display = 'block';
                })
                .catch(error => console.error('Error:', error));
            }, 'image/png');
        } else if (event.code === 'KeyQ' && styledImage.src) {
            event.preventDefault();
            const link = document.createElement('a');
            link.download = 'styled-image.png';
            link.href = styledImage.src;
            link.click();
        }
    });
});