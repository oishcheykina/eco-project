// My trees page functionality

const treeData = {
    tree1: {
        image: 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=600&h=600&fit=crop',
        type: 'Сосна',
        date: '15.03.2024',
        coordinates: '55.7558, 37.6173',
        coins: 50
    },
    tree2: {
        image: 'https://images.unsplash.com/photo-1511596266673-dd4b762a39b6?w=600&h=600&fit=crop',
        type: 'Дуб',
        date: '12.03.2024',
        coordinates: '55.7622, 37.6156',
        coins: 50
    },
    tree3: {
        image: 'https://images.unsplash.com/photo-1515525008-4cd43f8bb63a?w=600&h=600&fit=crop',
        type: 'Береза',
        date: '10.03.2024',
        coordinates: '55.7492, 37.6236',
        coins: 50
    },
    tree4: {
        image: 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=600&h=600&fit=crop',
        type: 'Ель',
        date: '08.03.2024',
        coordinates: '55.7558, 37.6098',
        coins: 50
    },
    tree5: {
        image: 'https://images.unsplash.com/photo-1520637736862-4d197d17c25a?w=600&h=600&fit=crop',
        type: 'Клен',
        date: '05.03.2024',
        coordinates: '55.7677, 37.6156',
        coins: 50
    },
    tree6: {
        image: 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=600&h=600&fit=crop',
        type: 'Фруктовое дерево',
        date: '02.03.2024',
        coordinates: '55.7435, 37.6289',
        coins: 50
    }
};

function openTreeDetail(treeId) {
    // Переход по URL, предполагая, что у тебя есть маршрут вида /trees/<id>/
    window.location.href = `/tree/${treeId}/`;
}

// Add hover effects to tree items
document.addEventListener('DOMContentLoaded', function() {
    const treeItems = document.querySelectorAll('.my-tree-item');
    
    treeItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});