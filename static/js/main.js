document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const wrapper = document.getElementById('wrapper');

    if (sidebarToggle && wrapper) {
        sidebarToggle.addEventListener('click', function () {
            if (window.innerWidth < 992) {
                wrapper.classList.toggle('sidebar-open');
            } else {
                wrapper.classList.toggle('sidebar-collapsed');
            }
        });

        // Close sidebar on outside click (mobile)
        document.addEventListener('click', function (e) {
            if (window.innerWidth < 992 &&
                wrapper.classList.contains('sidebar-open') &&
                !e.target.closest('#sidebar') &&
                !e.target.closest('#sidebarToggle')) {
                wrapper.classList.remove('sidebar-open');
            }
        });
    }

    // Auto-dismiss alerts after 4s
    document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });
});
