// Tree detail page functionality

document.addEventListener('DOMContentLoaded', function() {
    // Load tree data from localStorage
    const treeData = JSON.parse(localStorage.getItem('selectedTree'));
    
    if (treeData) {
        // Populate page with tree data
        document.getElementById('treeImage').src = treeData.image;
        document.getElementById('treeType').textContent = treeData.type;
        document.getElementById('plantDate').textContent = treeData.date;
        document.getElementById('coordinates').textContent = treeData.coordinates;
        document.getElementById('coinsEarned').textContent = treeData.coins;
    } else {
        // Fallback data if no tree selected
        document.getElementById('treeImage').src = 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=600&h=600&fit=crop';
        document.getElementById('treeType').textContent = 'Сосна';
        document.getElementById('plantDate').textContent = '15.03.2024';
        document.getElementById('coordinates').textContent = '55.7558, 37.6173';
        document.getElementById('coinsEarned').textContent = '50';
    }
});

function openMap(button) {
    let lat = button.getAttribute('data-lat');
    let lon = button.getAttribute('data-lon');

    // Заменяем запятые на точки — на случай, если пришли через , (региональные настройки)
    lat = lat.replace(',', '.');
    lon = lon.replace(',', '.');

    const mapUrl = `https://www.google.com/maps?q=${lat},${lon}`;
    window.open(mapUrl, '_blank');
}





function shareTree() {
    const treeType = document.getElementById('treeType').textContent;
    const plantDate = document.getElementById('plantDate').textContent;
    
    if (navigator.share) {
        navigator.share({
            title: 'Мое дерево в эко-приложении',
            text: `Я посадил ${treeType} ${plantDate}! Присоединяйтесь к движению за экологию!`,
            url: window.location.href
        }).then(() => {
            showNotification('Поделились успешно!');
        }).catch((error) => {
            console.error('Error sharing:', error);
            fallbackShare();
        });
    } else {
        fallbackShare();
    }
}

function fallbackShare() {
    const treeType = document.getElementById('treeType').textContent;
    const plantDate = document.getElementById('plantDate').textContent;
    const shareText = `Я посадил ${treeType} ${plantDate}! Присоединяйтесь к движению за экологию!`;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(shareText).then(() => {
            showNotification('Текст скопирован в буфер обмена!');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = shareText;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Текст скопирован в буфер обмена!');
    }
}

function editTree() {
    showNotification('Функция редактирования будет доступна в следующей версии!', 'info');
}

// Add animation effects
document.addEventListener('DOMContentLoaded', function() {
    const image = document.querySelector('.tree-detail-image img');
    const infoCards = document.querySelectorAll('.info-row');
    
    // Animate image entrance
    setTimeout(() => {
        if (image) {
            image.style.opacity = '0';
            image.style.transform = 'scale(0.8)';
            image.style.transition = 'all 0.6s ease-out';
            
            setTimeout(() => {
                image.style.opacity = '1';
                image.style.transform = 'scale(1)';
            }, 100);
        }
    }, 200);
    
    // Animate info cards
    infoCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateX(-20px)';
        card.style.transition = 'all 0.4s ease-out';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateX(0)';
        }, 400 + (index * 100));
    });
});