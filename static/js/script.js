document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const errorContainer = document.getElementById('errorContainer');
    const originalGallery = document.getElementById('originalGallery');
    const borderedGallery = document.getElementById('borderedGallery');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorContainer.textContent = '';
        
        if (!fileInput.files || fileInput.files.length === 0) {
            showError('Por favor selecciona un archivo');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error al procesar la imagen');
            }

            // Actualizar las galerías
            addImageToGallery(originalGallery, data.original, 'original');
            addImageToGallery(borderedGallery, data.bordered, 'bordered');

            // Resetear el formulario
            form.reset();
        } catch (error) {
            showError(error.message);
            console.error('Error:', error);
        }
    });

    function addImageToGallery(galleryElement, filename, type) {
        const img = document.createElement('img');
        img.src = `/uploads/${type === 'original' ? 'default' : 'border'}/${filename}`;
        img.alt = type === 'original' ? 'Original' : 'Con bordes';
        galleryElement.prepend(img);
    }

    function showError(message) {
        errorContainer.textContent = message;
    }
});
