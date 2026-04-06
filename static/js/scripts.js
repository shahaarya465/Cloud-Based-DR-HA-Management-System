document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alertElement) => {
        setTimeout(() => {
            alertElement.classList.add('fade');
            alertElement.classList.remove('show');
        }, 5000); // Extended slightly for readability of complex errors
    });

    // Real-time UTC clock for the banking dashboard
    const clockElement = document.getElementById('utc-clock');
    if (clockElement) {
        setInterval(() => {
            const now = new Date();
            clockElement.textContent = `System Time (UTC): ${now.toISOString().replace('T', ' ').substring(0, 19)}`;
        }, 1000);
    }
});