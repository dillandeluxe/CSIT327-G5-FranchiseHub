document.addEventListener('DOMContentLoaded', function() {
  // ===== NOTIFICATION BELL SYSTEM
  const notificationBell = document.getElementById('notificationBell');
  const notificationDropdown = document.getElementById('notificationDropdown');
  const markAllReadBtn = notificationDropdown?.querySelector('.mark-all-read');
  const notificationBadge = document.querySelector('.notification-badge');

  console.log('🔔 Notification Bell:', notificationBell);
  console.log('📋 Notification Dropdown:', notificationDropdown);
  console.log('🔴 Badge:', notificationBadge);

  if (notificationBell && notificationDropdown) {
    // Toggle dropdown on bell click
    notificationBell.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log('✅ Bell clicked');
      notificationDropdown.classList.toggle('active');
      notificationBell.classList.toggle('active', notificationDropdown.classList.contains('active'));
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!notificationDropdown.contains(e.target) && !notificationBell.contains(e.target)) {
        notificationDropdown.classList.remove('active');
        notificationBell.classList.remove('active');
      }
    });

    // Mark all as read
    if (markAllReadBtn) {
      markAllReadBtn.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.notification-item.unread').forEach(item => {
          item.classList.remove('unread');
        });
        if (notificationBadge) {
          notificationBadge.classList.add('hidden');
        }
        console.log('✅ All marked as read');
      });
    }

    // Mark individual items as read
    document.querySelectorAll('.notification-item').forEach(item => {
      item.addEventListener('click', function() {
        this.classList.remove('unread');
        updateNotificationBadge();
      });
    });

    function updateNotificationBadge() {
      const unreadCount = document.querySelectorAll('.notification-item.unread').length;
      if (notificationBadge) {
        if (unreadCount === 0) {
          notificationBadge.classList.add('hidden');
        } else {
          notificationBadge.textContent = unreadCount;
          notificationBadge.classList.remove('hidden');
        }
      }
    }
  } else {
    console.warn('⚠️ Notification elements not found in DOM');
  }

  // ===== REAL-TIME STAT UPDATES WITH POLLING
  (function() {
    let updateInterval = null;
    let isUpdating = false;
    const UPDATE_INTERVAL = 5000; // 5 seconds

    const statElements = {
      activeFranchises: document.getElementById('stat-active-franchises'),
      totalApplications: document.getElementById('stat-total_applications'),
      activeFranchisees: document.getElementById('stat-active-franchisees'),
      revenue: document.getElementById('stat-revenue')
    };

    console.log('📊 Stat Elements:', statElements);

    function fetchDashboardStats() {
      if (isUpdating) return;
      isUpdating = true;

      fetch('/accounts/franchisor/dashboard-stats/', {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        cache: 'no-cache'
      })
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(data => {
          console.log('✅ Stats updated:', data);
          updateStatsUI(data);
        })
        .catch(err => {
          console.error('❌ Error fetching stats:', err);
          // Silently fail - don't break the page
        })
        .finally(() => { isUpdating = false; });
    }

    function updateStatsUI(data) {
      const updates = [
        { element: statElements.activeFranchises, value: data.active_franchises },
        { element: statElements.totalApplications, value: data.total_applications },
        { element: statElements.activeFranchisees, value: data.active_franchisees },
        { element: statElements.revenue, value: data.revenue }
      ];

      updates.forEach(({ element, value }) => {
        if (element && value !== undefined) {
          const currentValue = parseInt(element.textContent.replace(/[^0-9]/g, '')) || 0;
          const newValue = parseInt(value);

          if (currentValue !== newValue) {
            console.log(`📊 Updating: ${element.id} from ${currentValue} to ${newValue}`);
            element.classList.add('updating');
            animateNumberChange(element, currentValue, newValue);
          }
        }
      });
    }

    function animateNumberChange(element, from, to) {
      const duration = 800;
      const steps = 30;
      const increment = (to - from) / steps;
      let current = from;
      let step = 0;

      const timer = setInterval(() => {
        step++;
        current += increment;

        if (step >= steps) {
          current = to;
          clearInterval(timer);
          element.classList.remove('updating');
        }

        element.textContent = Math.floor(current).toLocaleString();
      }, duration / steps);
    }

    // Start polling on load
    setTimeout(() => {
      console.log('🚀 Starting stats polling...');
      fetchDashboardStats();
      updateInterval = setInterval(fetchDashboardStats, UPDATE_INTERVAL);
    }, 500);

    // Pause/resume on tab visibility
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        console.log('⏸️ Tab hidden - pausing updates');
        if (updateInterval) clearInterval(updateInterval);
      } else {
        console.log('▶️ Tab visible - resuming updates');
        fetchDashboardStats();
        updateInterval = setInterval(fetchDashboardStats, UPDATE_INTERVAL);
      }
    });

    window.dashboardStats = { refresh: fetchDashboardStats, elements: statElements };
  })();

  // ===== Decision Modal (Accept/Reject Applications)
  const decisionModal = document.getElementById('decisionModal');
  const decisionTitle = document.getElementById('decisionTitle');
  const decisionLabel = document.getElementById('decisionLabel');
  const decisionHelp = document.getElementById('decisionHelp');
  const decisionTextarea = document.getElementById('decisionTextarea');
  const decisionForm = document.getElementById('decisionForm');
  const decisionSubmitBtn = document.getElementById('decisionSubmitBtn');
  const decisionCloseBtns = [document.getElementById('decisionClose'), document.getElementById('decisionCancel')];

  function openModalAccept(appId) {
    decisionTitle.textContent = 'Accept Application';
    decisionLabel.textContent = 'Approval Notes (Optional)';
    decisionHelp.textContent = 'Optional notes for the applicant';
    decisionTextarea.name = 'approval_note';
    decisionTextarea.placeholder = 'Optional notes for the applicant...';
    decisionTextarea.value = '';
    decisionTextarea.required = false;
    decisionForm.action = `/accounts/franchisor/application/${appId}/accept/`;
    decisionSubmitBtn.textContent = 'Accept Application';
    decisionSubmitBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    decisionModal.classList.remove('hidden');
    decisionModal.classList.add('is-open');
  }

  function openModalReject(appId) {
    decisionTitle.textContent = 'Reject Application';
    decisionLabel.textContent = 'Reason for Rejection *';
    decisionHelp.textContent = 'Please provide a clear reason for rejection';
    decisionTextarea.name = 'rejection_reason';
    decisionTextarea.placeholder = 'Please provide a clear reason...';
    decisionTextarea.value = '';
    decisionTextarea.required = true;
    decisionForm.action = `/accounts/franchisor/application/${appId}/reject/`;
    decisionSubmitBtn.textContent = 'Reject Application';
    decisionSubmitBtn.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    decisionModal.classList.remove('hidden');
    decisionModal.classList.add('is-open');
  }

  // Bind accept/reject buttons
  document.querySelectorAll('.js-open-accept').forEach(btn => {
    const appId = btn.getAttribute('data-app');
    btn.addEventListener('click', (e) => { e.preventDefault(); openModalAccept(appId); });
  });
  document.querySelectorAll('.js-open-reject').forEach(btn => {
    const appId = btn.getAttribute('data-app');
    btn.addEventListener('click', (e) => { e.preventDefault(); openModalReject(appId); });
  });

  // Close decision modal
  decisionCloseBtns.forEach(b => b && b.addEventListener('click', () => {
    decisionModal.classList.add('hidden');
    decisionModal.classList.remove('is-open');
    decisionForm.reset();
  }));

  decisionModal?.addEventListener('click', (e) => {
    if (e.target === decisionModal) {
      decisionModal.classList.add('hidden');
      decisionModal.classList.remove('is-open');
      decisionForm.reset();
    }
  });

  // Decision form submit
  decisionForm?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const isRejection = decisionForm.action.includes('/reject/');
    const reasonValue = decisionTextarea.value.trim();
    if (isRejection && !reasonValue) {
      alert('Rejection reason is required.');
      decisionTextarea.focus();
      return;
    }

    const formData = new FormData(decisionForm);
    const originalText = decisionSubmitBtn.textContent;

    decisionSubmitBtn.disabled = true;
    decisionSubmitBtn.innerHTML = `
      <svg class="spinner" width="16" height="16" viewBox="0 0 50 50">
        <circle class="spinner-path" cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="5"></circle>
      </svg>
      Processing...
    `;

    try {
      const response = await fetch(decisionForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin'
      });
      if (response.ok) {
        const isApproval = decisionForm.action.includes('/accept/');
        alert(isApproval ? '✅ Application accepted successfully!' : '✅ Application rejected successfully!');
        decisionModal.classList.add('hidden');
        decisionModal.classList.remove('is-open');
        decisionForm.reset();
        window.location.reload();
      } else {
        alert('❌ Error: ' + (response.statusText || 'Please try again'));
      }
    } catch (err) {
      console.error(err);
      alert('❌ Network error. Please try again.');
    } finally {
      decisionSubmitBtn.disabled = false;
      decisionSubmitBtn.textContent = originalText;
    }
  });

  // ===== Delete Modal
  const deleteModal = document.getElementById('deleteModal');
  const deleteForm = document.getElementById('deleteForm');

  function openDeleteModalInternal(franchiseId) {
    if (deleteModal && deleteForm) {
      deleteForm.action = `/accounts/franchise/delete/${franchiseId}/`;
      deleteModal.classList.remove('hidden');
      deleteModal.classList.add('is-open');
    }
  }

  function closeDeleteModalInternal() {
    if (deleteModal) {
      deleteModal.classList.add('hidden');
      deleteModal.classList.remove('is-open');
    }
  }

  // Bind delete button
  document.querySelectorAll('.btn-approval-delete,[data-delete-franchise-id]').forEach(btn => {
    const id = btn.getAttribute('data-franchise-id') || btn.getAttribute('data-delete-franchise-id');
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (id) openDeleteModalInternal(id);
    });
  });

  window.closeDeleteModal = closeDeleteModalInternal;

  // Force-hide modals on load
  [decisionModal, deleteModal].forEach(m => {
    if (m) {
      m.classList.add('hidden');
      m.classList.remove('is-open');
      m.style.display = '';
    }
  });

  // Close modals on ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (decisionModal?.classList.contains('is-open')) {
        decisionModal.classList.add('hidden');
        decisionModal.classList.remove('is-open');
      }
      if (deleteModal?.classList.contains('is-open')) {
        deleteModal.classList.add('hidden');
        deleteModal.classList.remove('is-open');
      }
    }
  });

  console.log('✅ Dashboard JS initialized');
});
