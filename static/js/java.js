document.getElementById('resumir-btn').addEventListener('click', function() {
    const texto = document.getElementById('original-text').value;

    if (texto.trim() === '') {
        alert('Por favor, ingresa un texto para resumir.');
        return;
    }

    // Crear la petición POST a la API Flask
    fetch('/resumir', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ texto: texto })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Hubo un error: ' + data.error);
        } else {
            // Mostrar el resumen en la página
            document.getElementById('resumen-text').textContent = data.resumen;
            document.getElementById('resumen-container').style.display = 'block';
            // No limpiar el campo de texto, permite ingresar nuevo texto para resumir
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
