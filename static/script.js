// Main JavaScript functionality

// Counter animation
function animateCounter(element) {
    const target = parseInt(element.dataset.target);
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// Balance animation
function animateBalance() {
    const balanceElement = document.getElementById('balance');
    if (balanceElement) {
        const target = parseInt(balanceElement.dataset.balance || '0', 10);
        const currentDisplay = parseInt(balanceElement.textContent.replace(/\D/g, ''), 10) || 0;

        if (currentDisplay >= target) return;  // Не анимировать, если уже актуальное значение

        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            balanceElement.textContent = Math.floor(current).toLocaleString();
        }, 16);
        
    }
}


// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Animate balance
    setTimeout(animateBalance, 500);
    
    // Animate counters
    const counters = document.querySelectorAll('.counter');
    counters.forEach((counter, index) => {
        setTimeout(() => {
            animateCounter(counter);
        }, 800 + (index * 300));
    });
    
    // Add click effects to navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
        });
    });
});

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: ${type === 'success' ? '#00df2d' : '#ff4444'};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        z-index: 2000;
        animation: slideDown 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateX(-50%) translateY(0); opacity: 1; }
        to { transform: translateX(-50%) translateY(-100%); opacity: 0; }
    }
`;
document.head.appendChild(style);