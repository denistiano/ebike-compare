/**
 * E-Bike Compare JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Handle bike selection form
    const bikeForm = document.querySelector('form[action="/compare"]');
    if (bikeForm) {
        // Add select/deselect all functionality
        const selectAllBtn = document.createElement('button');
        selectAllBtn.type = 'button';
        selectAllBtn.className = 'btn btn-sm btn-outline-secondary me-2';
        selectAllBtn.textContent = 'Select All';
        selectAllBtn.addEventListener('click', function() {
            document.querySelectorAll('input[name="bike_ids"]').forEach(checkbox => {
                checkbox.checked = true;
            });
        });

        const deselectAllBtn = document.createElement('button');
        deselectAllBtn.type = 'button';
        deselectAllBtn.className = 'btn btn-sm btn-outline-secondary me-2';
        deselectAllBtn.textContent = 'Deselect All';
        deselectAllBtn.addEventListener('click', function() {
            document.querySelectorAll('input[name="bike_ids"]').forEach(checkbox => {
                checkbox.checked = false;
            });
        });

        // Insert buttons before the submit button
        const submitBtn = bikeForm.querySelector('button[type="submit"]');
        submitBtn.parentNode.insertBefore(deselectAllBtn, submitBtn);
        submitBtn.parentNode.insertBefore(selectAllBtn, deselectAllBtn);
    }

    // Comparison table enhancements
    const comparisonTable = document.querySelector('.comparison-table');
    if (comparisonTable) {
        // Make sticky header work better with Bootstrap
        const tableHeader = comparisonTable.querySelector('thead');
        if (tableHeader) {
            tableHeader.style.position = 'sticky';
            tableHeader.style.top = '0';
            tableHeader.style.zIndex = '1';
        }

        // Add tooltips to any truncated cell content
        comparisonTable.querySelectorAll('td').forEach(cell => {
            if (cell.offsetWidth < cell.scrollWidth) {
                cell.title = cell.textContent;
                cell.style.cursor = 'help';
            }
        });
    }
}); 