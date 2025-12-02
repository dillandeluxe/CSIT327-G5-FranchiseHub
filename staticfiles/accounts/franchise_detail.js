document.addEventListener('DOMContentLoaded', function() {
  // CSRF from cookie
  const getCookie = (name) => {
    const cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  };
  const csrfToken = getCookie('csrftoken');

  // Hero image error fallback (replaces inline onerror)
  const heroImg = document.getElementById('heroImage');
  if (heroImg) {
    heroImg.addEventListener('error', () => {
      const hero = heroImg.parentNode;
      heroImg.style.display = 'none';
      hero.style.background = 'linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%)';
    }, { once: true });
  }

  // Favorite button toggle
  const franchiseId = document.body.querySelector('[data-franchise-id]')?.dataset.franchiseId || document.getElementById('favoriteBtn')?.dataset.franchiseId;
  const favoriteBtn = document.getElementById('favoriteBtn');
  const favoriteText = document.getElementById('favoriteText');

  if (favoriteBtn && franchiseId) {
    // Initial state
    fetch(`/accounts/favorites/check/${franchiseId}/`, { credentials: 'same-origin' })
      .then(res => res.json())
      .then(data => {
        if (data.is_favorited) {
          favoriteBtn.style.background = '#10b981';
          favoriteBtn.style.borderColor = 'white';
          favoriteText.textContent = '♥ Saved to Favorites';
        }
      })
      .catch(() => {});

    // Toggle
    favoriteBtn.addEventListener('click', async function(e) {
      e.preventDefault();
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

        if (response.ok) {
          if (data.status === 'added') {
            favoriteBtn.style.background = '#10b981';
            favoriteBtn.style.borderColor = 'white';
            favoriteText.textContent = '♥ Saved to Favorites';
          } else if (data.status === 'removed') {
            favoriteBtn.style.background = 'rgba(255, 255, 255, 0.2)';
            favoriteBtn.style.borderColor = 'white';
            favoriteText.textContent = 'Add to Favorites';
          }
          showToast(data.message, 'success');
        } else {
          showToast(data.message || 'Error updating favorite', 'error');
        }
      } catch (error) {
        showToast('Error updating favorite', 'error');
      }
    });
  }

  // Toast
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast-lite ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.animation = 'slideOutDown 0.3s ease-out forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
});
