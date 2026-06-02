document.addEventListener('DOMContentLoaded', function () {

    /* ================= FLASH AUTO DISMISS ================= */
    const alerts = document.querySelectorAll('.alert-flexi');

    alerts.forEach((alert) => {
        setTimeout(() => {
            if (!alert) return;

            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';

            setTimeout(() => {
                alert.remove();
            }, 500);

        }, 5000);
    });


    /* ================= ACTIVE SIDEBAR LINK ================= */
    const currentPath = window.location.pathname;

    document.querySelectorAll('.sidebar-link').forEach((link) => {
        try {
            const href = link.getAttribute('href');

            if (!href) return;

            // exact match OR endsWith fallback (Flask url fix friendly)
            if (currentPath === href || currentPath.endsWith(href)) {
                link.classList.add('active');
            }

        } catch (e) {
            console.warn('Sidebar link error:', e);
        }
    });


    /* ================= CONFIRM TOGGLE FORMS ================= */
    document.querySelectorAll('form[action*="toggle"]').forEach((form) => {

        form.addEventListener('submit', function (e) {

            const ok = confirm("Are you sure you want to change this user's status?");

            if (!ok) {
                e.preventDefault();
            }

        });

    });


    /* ================= NUMBER INPUT SAFETY ================= */
    document.querySelectorAll('input[type="number"]').forEach((input) => {

        input.addEventListener('input', function () {

            if (this.value === '') return;

            const value = parseFloat(this.value);

            if (isNaN(value)) {
                this.value = '';
                return;
            }

            if (value < 0) {
                this.value = 0;
            }

        });

    });

});
