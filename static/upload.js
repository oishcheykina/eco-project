function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const latitude = position.coords.latitude.toFixed(6);
            const longitude = position.coords.longitude.toFixed(6);
            document.getElementById('coordinates').value = `${latitude}, ${longitude}`;
        }, function (error) {
            alert('Не удалось получить координаты. Разрешите доступ к геолокации.');
        });
    } else {
        alert("Геолокация не поддерживается вашим браузером.");
    }
}

function openFileUpload() {
    document.getElementById('fileInput').click();
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const previewImage = document.getElementById('previewImage');
            previewImage.src = e.target.result;
            document.getElementById('photoPreview').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

function openCamera() {
    const fileInput = document.getElementById('fileInput');
    fileInput.setAttribute('capture', 'environment'); // Открывает камеру
    fileInput.click();
}
