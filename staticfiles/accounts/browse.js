document.addEventListener('DOMContentLoaded', function() {
  // Mobile filters toggle
  const toggleFiltersBtn = document.getElementById('toggleFilters');
  const closeFiltersBtn = document.getElementById('closeFilters');
  const filtersSidebar = document.querySelector('.filters-sidebar');

  toggleFiltersBtn?.addEventListener('click', () => {
    filtersSidebar.classList.toggle('active');
  });
  closeFiltersBtn?.addEventListener('click', () => {
    filtersSidebar.classList.remove('active');
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.filters-sidebar') && !e.target.closest('#toggleFilters')) {
      filtersSidebar.classList.remove('active');
    }
  });

  // Favorite buttons
  const favoriteButtons = document.querySelectorAll('.favorite-btn');
  favoriteButtons.forEach(btn => {
    const franchiseId = btn.dataset.franchiseId;

    // Check initial favorite status
    fetch(`/accounts/favorites/check/${franchiseId}/`)
      .then(res => res.json())
      .then(data => { if (data.is_favorited) btn.classList.add('active'); })
      .catch(err => console.error('Error checking favorite:', err));

    // Toggle favorite on click
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      try {
        const csrf =
          document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
          document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1];

        const response = await fetch(`/accounts/favorites/toggle/${franchiseId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrf,
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        if (response.ok) {
          if (data.status === 'added') btn.classList.add('active');
          else if (data.status === 'removed') btn.classList.remove('active');
          showToast(data.message, 'success');
        } else {
          showToast(data.message || 'Error updating favorite', 'error');
        }
      } catch (error) {
        console.error('Error:', error);
        showToast('Failed to update favorite', 'error');
      }
    });
  });

  // Toast notification
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.animation = 'slideInUp 0.3s ease-out reverse forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Optional: filters form hook
  const filtersForm = document.getElementById('filtersForm');
  filtersForm?.addEventListener('submit', () => {
    console.log('✅ Filters form submitted');
  });

  // ✅ Clear button: reset fields and reload page without params
  const clearBtn = document.querySelector('.btn-reset');
  if (clearBtn && filtersForm) {
    clearBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // Clear inputs
      filtersForm.querySelectorAll('input').forEach(input => input.value = '');
      // Navigate to browse route without query params
      const browseUrl = document.querySelector('.nav-link.active')?.getAttribute('href') || '/accounts/browse/';
      window.location.href = browseUrl;
    });
  }

  // Image error handling: replace broken images with placeholder
  document.querySelectorAll('.franchise-img').forEach(img => {
    img.addEventListener('error', () => {
      img.classList.add('hidden');
      const placeholder = img.parentElement.querySelector('.image-placeholder');
      if (placeholder) placeholder.classList.remove('hidden');
    });
  });
});
