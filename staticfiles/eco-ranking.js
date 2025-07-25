// User data


// Balance animation
function animateBalance() {
    const balanceElement = document.getElementById('balance');
    const targetBalance = parseInt(balanceElement.dataset.balance);
    const increment = targetBalance / 30;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= targetBalance) {
            balanceElement.textContent = targetBalance;
            clearInterval(timer);
        } else {
            balanceElement.textContent = Math.floor(current);
        }
    }, 30);
}

// Get rank icon
function getRankIcon(rank) {
    switch (rank) {
        case 1: return "🥇";
        case 2: return "🥈";
        case 3: return "🥉";
        default: return null;
    }
}

// Create ranking item
function createRankingItem(user, rank) {
    const isCurrentUser = user.id === currentUserId;
    const rankIcon = getRankIcon(rank);
    
    const item = document.createElement('div');
    item.className = `ranking-item fade-in ${isCurrentUser ? 'current-user' : ''}`;
    
    item.innerHTML = `
        <div class="ranking-left">
            <div class="rank-badge ${isCurrentUser ? 'current-user' : rank <= 3 ? 'top-three' : 'other'}">
                ${rankIcon || rank}
            </div>
            <div class="user-info">
                <h3>${user.name} ${isCurrentUser ? '<span class="you-label">Вы</span>' : ''}</h3>

                <div class="trees ${isCurrentUser ? 'current-user' : ''}">
                    <i class="fas fa-tree tree-icon-small"></i>
                    <span>${user.trees} деревьев</span>
                </div>
            </div>
        </div>
        ${rank <= 3 && !isCurrentUser ? `<div class="medal">${rankIcon}</div>` : ''}
    `;
    
    return item;
}

// Render ranking list
function renderRankingList() {
    const rankingList = document.getElementById('rankingList');
    const currentUserPosition = document.getElementById('currentUserPosition');
    
    // Clear existing content
    rankingList.innerHTML = '';
    
    // Get current user info
    const currentUser = users.find(user => user.id === currentUserId);
    const currentUserRank = users.findIndex(user => user.id === currentUserId) + 1;
    const topUsers = users.slice(0, 10);
    
    // Render top 10 users
    topUsers.forEach((user, index) => {
        const rank = index + 1;
        const item = createRankingItem(user, rank);
        rankingList.appendChild(item);
    });
    
    // Show current user position if not in top 10
    if (currentUserRank > 10 && currentUser) {
        currentUserPosition.style.display = 'block';
        currentUserPosition.innerHTML = `
            <div class="position-label">Ваша позиция</div>
            <div class="ranking-left">
                <div class="rank-badge current-user">
                    ${currentUserRank}
                </div>
                <div class="user-info">
                    <h3 style="color: white;">${currentUser.name}</h3>
                    <div class="trees current-user">
                        <i class="fas fa-tree"></i>
                        <span>${currentUser.trees} деревьев</span>
                    </div>
                </div>
            </div>
        `;
    }
}

// Home button click handler
function handleHomeClick() {
    // Create toast notification
    const toast = document.createElement('div');
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'fadeIn 0.3s ease-out reverse';
        setTimeout(() => {
            document.body.removeChild(toast);
            window.location.href = homeUrl;

        }, 300);
    },);
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Animate balance
    animateBalance();
    
    // Render ranking list
    renderRankingList();
    
    // Add home button event listener
    document.getElementById('homeButton').addEventListener('click', handleHomeClick);
    
    // Add stagger animation to ranking items
    const items = document.querySelectorAll('.ranking-item');
    items.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
});