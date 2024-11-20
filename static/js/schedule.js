document.addEventListener('DOMContentLoaded', function() {
    // Prevenir que el dropdown es tanqui al clicar dins
    document.querySelectorAll('.dropdown-menu').forEach(function(dropdownMenu) {
        dropdownMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
});