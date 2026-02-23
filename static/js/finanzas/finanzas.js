// static/js/finanzas.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Inicializar iconos de Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // 2. Lógica para los chips de filtro (visual por ahora)
    const filterChips = document.querySelectorAll('.filter-chip');
    filterChips.forEach(chip => {
        chip.addEventListener('click', () => {
            // Remover 'active' de todos
            filterChips.forEach(c => c.classList.remove('active'));
            // Agregar 'active' al clickeado
            chip.classList.add('active');
            
            // Aquí iría la lógica para filtrar la lista según el tipo
            const filterType = chip.dataset.filter;
            console.log(`Filtrando por: ${filterType}`);
        });
    });

    // 3. Lógica del Formulario (Evitar recarga y simular guardado)
    const form = document.getElementById('transaction-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log("Transacción guardada (simulada)");
            toggleModal(false);
            form.reset();
        });
    }
});

// Función global para abrir/cerrar el modal
function toggleModal(show) {
    const modal = document.getElementById('modal-transaction');
    if (modal) {
        modal.classList.toggle('active', show);
    }
}