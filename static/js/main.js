// HackHub-Code - Main JS
document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 5s
    document.querySelectorAll('.alert.alert-dismissible').forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Animate score bars on page load
    document.querySelectorAll('.score-bar').forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(function() {
            setTimeout(function() {
                bar.style.width = width;
            }, 100);
        });
    });
});
