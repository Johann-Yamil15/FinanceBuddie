// Variable global para rastrear el estado de edición
let editandoId = null;

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Mapeo de iconos por categoría
    const iconosCategoria = {
        'Comida': 'utensils',
        'Compras': 'shopping-bag',
        'Entretenimiento': 'film',
        'Transporte': 'bus',
        'Servicios': 'zap',
        'Salud': 'heart-pulse',
        'Educación': 'book-open',
        'Honorarios': 'briefcase'
    };

    // 2. Inyectar iconos dinámicamente según el nombre de la categoría
    document.querySelectorAll('.transaction-item').forEach(item => {
        const h4 = item.querySelector('h4');
        const iconElement = item.querySelector('i[data-lucide]');
        
        if (h4 && iconElement) {
            const categoria = h4.innerText.trim();
            iconElement.setAttribute('data-lucide', iconosCategoria[categoria] || 'circle-dollar-sign');
        }
    });

    // 3. Inicializar iconos de Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // 4. Lógica de Envío del Formulario (Unificada para POST y PUT)
    const form = document.getElementById('transaction-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                tipo: form.querySelector('input[name="tipo"]:checked').value,
                monto: parseFloat(form.querySelector('input[type="number"]').value),
                categoria_id: parseInt(form.querySelector('select[name="categoria"]').value)
            };

            // Si editandoId tiene valor, es una actualización (PUT), si no, es creación (POST)
            const url = editandoId ? `/api/finanzas/${editandoId}` : '/api/finanzas';
            const method = editandoId ? 'PUT' : 'POST';

            try {
                const response = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (result.status === 'success') {
                    editandoId = null; // Limpiar estado
                    toggleModal(false);
                    form.reset();
                    location.reload(); 
                } else {
                    alert("Error: " + result.message);
                }
            } catch (error) {
                console.error("Error en la petición:", error);
                alert("No se pudo conectar con el servidor.");
            }
        });
    }
});

/**
 * Abre el modal para crear un nuevo registro (limpia el estado previo)
 */
function abrirModalCrear() {
    editandoId = null;
    const form = document.getElementById('transaction-form');
    if (form) form.reset();
    document.querySelector('#modal-transaction h3').innerText = "Nuevo Movimiento";
    toggleModal(true);
}

/**
 * Función global para abrir/cerrar el modal
 */
function toggleModal(show) {
    const modal = document.getElementById('modal-transaction');
    if (modal) {
        modal.classList.toggle('active', show);
    }
}

/**
 * Rellena el modal con los datos del item seleccionado para editar
 */
function prepararEdicion(button) {
    // Buscamos el contenedor padre que tiene los atributos data-*
    const item = button.closest('.transaction-item');
    if (!item) return;

    editandoId = item.dataset.id;

    // Cambiar título del modal
    document.querySelector('#modal-transaction h3').innerText = "Editar Movimiento";
    
    // Rellenar campos del formulario usando los dataset del HTML
    const form = document.getElementById('transaction-form');
    form.querySelector('input[type="number"]').value = item.dataset.monto;
    form.querySelector(`#type-${item.dataset.tipo}`).checked = true;
    form.querySelector('select[name="categoria"]').value = item.dataset.categoriaId;

    toggleModal(true);
}

/**
 * Función global para eliminar transacciones
 */
async function eliminarTransaccion(id) {
    if (!confirm('¿Estás seguro de eliminar este movimiento? El saldo se ajustará automáticamente.')) {
        return;
    }

    try {
        const response = await fetch(`/api/finanzas/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.status === 'success') {
            location.reload();
        } else {
            alert("Error al eliminar: " + result.message);
        }
    } catch (error) {
        console.error("Error en la eliminación:", error);
    }
}

/**
 * Manejo visual de los dropdowns (tres puntos)
 */
function toggleDropdown(event, btn) {
    // 1. Evitar que el clic cierre el menú inmediatamente
    event.stopPropagation(); 
    
    const currentDropdown = btn.parentElement;
    
    // 2. Cerrar cualquier otro menú abierto
    document.querySelectorAll('.dropdown').forEach(d => {
        if (d !== currentDropdown) d.classList.remove('active');
    });

    // 3. Alternar el menú actual
    currentDropdown.classList.toggle('active');
}

// Cerrar si se hace clic fuera del menú
window.onclick = function(event) {
    if (!event.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown').forEach(d => {
            d.classList.remove('active');
        });
    }
};