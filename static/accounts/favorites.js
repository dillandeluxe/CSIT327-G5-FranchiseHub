document.addEventListener('DOMContentLoaded', function() {
  const favoriteButtons = document.querySelectorAll('.favorite-btn');
  const favoritesGrid = document.getElementById('favoritesGrid');

  const getCookie = (name) => {
    const cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  };
  const csrfToken = getCookie('csrftoken');

  favoriteButtons.forEach(btn => {
    btn.addEventListener('click', async function(e) {
      e.preventDefault();
      e.stopPropagation();

      const franchiseId = this.dataset.franchiseId;
      const card = this.closest('.favorite-card');

      this.disabled = true;
      const originalHTML = this.innerHTML;
      this.innerHTML = '<div class="loading-spinner"></div>';

      try {
        const response = await fetch(`/accounts/favorites/toggle/${franchiseId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          },
          credentials: 'same-origin'
        });

        const data = await response.json();

        if (response.ok && data.status === 'removed') {
          // Animate card removal
          if (card) {
            card.style.animation = 'cardFadeOut 0.3s ease-out forwards';
            setTimeout(() => {
              card.remove();

              // If grid emptied, refresh to show empty state
              if (favoritesGrid && favoritesGrid.children.length === 0) {
                window.location.reload();
              }

              // Update count badge
              const countBadge = document.querySelector('.favorites-count');
              if (countBadge) {
                const currentCount = parseInt(countBadge.textContent || '0', 10);
                countBadge.textContent = Math.max(0, currentCount - 1);
              }
            }, 300);
          }
          showToast('success', data.message || 'Removed from favorites');
        } else {
          showToast('error', data.message || 'Failed to update favorite.');
          this.innerHTML = originalHTML;
          this.disabled = false;
        }
      } catch (error) {
        console.error('Error toggling favorite:', error);
        showToast('error', 'Failed to update favorite. Please try again.');
        this.innerHTML = originalHTML;
        this.disabled = false;
      }
    });
  });

  // Toast notification
  function showToast(type, message) {
    const container = document.getElementById('toastContainer') || document.body;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success'
      ? '<svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>'
      : '<svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>';

    toast.innerHTML = `
      <div class="toast-icon">${icon}</div>
      <div class="toast-message">${message}</div>
    `;

    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }
});
