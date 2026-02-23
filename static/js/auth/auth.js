function toggleAuth() {
    const loginSec = document.getElementById('loginSection');
    const registerSec = document.getElementById('registerSection');
    const card = document.getElementById('authCard');
    const logo = document.querySelector('.brand-logo');

    // Efecto de rotación leve en el logo al cambiar
    logo.style.transform = "rotate(360deg)";
    
    // Animación de salida
    card.style.opacity = "0";
    card.style.transform = "scale(0.95)";

    setTimeout(() => {
        if (loginSec.classList.contains('d-none')) {
            loginSec.classList.remove('d-none');
            registerSec.classList.add('d-none');
        } else {
            loginSec.classList.add('d-none');
            registerSec.classList.remove('d-none');
        }
        
        // Reiniciar logo y mostrar card
        card.style.opacity = "1";
        card.style.transform = "scale(1)";
        setTimeout(() => { logo.style.transform = "rotate(0deg)"; }, 500);
        
        // Re-inicializar iconos de Lucide por si acaso
        lucide.createIcons();
    }, 400);
}
async function handleSubmit(event, type) {
    event.preventDefault();
    const formData = new FormData(event.target);
    
    // Coincide exactamente con tu diccionario en urls.py
    const url = type === 'login' ? '/login' : '/register'; 

    try { // <-- Faltaba abrir este bloque
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });

        // Si el controlador hizo un redirect('/finanzas'), fetch lo detecta aquí
        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        const data = await response.json();
        if (response.ok) {
            // En caso de que no use redirect pero sea exitoso
            window.location.href = '/finanzas';
        } else {
            alert(data.message || "Error en la operación");
        }
    } catch (error) {
        console.error("Error fatal:", error);
        alert("Ocurrió un error al conectar con el servidor.");
    }
}