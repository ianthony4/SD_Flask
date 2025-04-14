// En base a la pagina web proporcionada https://www.dropzonejs.com/#usage
// Desactivar auto-descubrimiento de Dropzone
Dropzone.autoDiscover = false;

// Configuracion cuando el DOM este listo
document.addEventListener("DOMContentLoaded", function() {
    const myDropzone = new Dropzone("#myDropzone", {
        url: "/",
        paramName: "file",
        maxFilesize: 2, // MB
        acceptedFiles: "image/jpeg, image/png, image/gif",
        addRemoveLinks: true,
        autoProcessQueue: true,
        parallelUploads: 5,
        
        // Mensajes personalizados
        dictDefaultMessage: "Arrastra las imágenes aquí",
        dictFallbackMessage: "Tu navegador no soporta arrastrar y soltar archivos",
        dictFileTooBig: "El archivo es demasiado grande ({{filesize}}MB). Tamaño máximo: {{maxFilesize}}MB.",
        dictInvalidFileType: "No puedes subir archivos de este tipo.",
        dictResponseError: "El servidor respondió con código {{statusCode}}",
        dictCancelUpload: "Cancelar subida",
        dictUploadCanceled: "Subida cancelada",
        dictRemoveFile: "Eliminar archivo",
        dictMaxFilesExceeded: "No puedes subir más archivos"
    });

    // Esto recarga la pagina cuando la subida sea exitosa
    myDropzone.on("complete", function(file) {
        if (file.status === "success") {
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    });

    // Errores en consola para depurar!
    myDropzone.on("error", function(file, message) {
        console.error("Error al subir archivo:", message);
    });
});

//Recuerda que en la pagina se explica que debemos usar DROPZONE.JS
//https://www.dropzonejs.com/#usage
