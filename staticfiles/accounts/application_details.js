document.addEventListener('DOMContentLoaded', () => {
  // Card entrance animations
  const cards = document.querySelectorAll('.profile-card, .details-card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'all 0.6s cubic-bezier(0.4,0,0.2,1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, i * 100);
  });

  // Reject modal character counter
  const rejectTextarea = document.getElementById('rejectionReasonTextarea');
  const charCount = document.getElementById('charCount');
  if (rejectTextarea && charCount) {
    rejectTextarea.addEventListener('input', () => {
      const len = rejectTextarea.value.length;
      charCount.textContent = len;
      if (len < 10) charCount.style.color = '#ef4444';
      else if (len > 450) charCount.style.color = '#f59e0b';
      else charCount.style.color = '#10b981';
    });
  }

  // Reject form validation
  const rejectForm = document.getElementById('rejectForm');
  if (rejectForm) {
    rejectForm.addEventListener('submit', e => {
      const textarea = rejectTextarea;
      const reason = textarea.value.trim();
      if (reason.length < 10) {
        e.preventDefault();
        alert('Please provide a rejection reason with at least 10 characters.');
        textarea.focus();
        return;
      }
      const submitBtn = document.getElementById('rejectSubmitBtn');
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20" class="spinner-inline">
          <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z"/>
        </svg>
        Processing...`;
    });
  }
});

// Open reject modal
function openRejectModal() {
  const modal = document.getElementById('rejectModal');
  if (!modal) return;
  modal.classList.add('active');
  const ta = document.getElementById('rejectionReasonTextarea');
  if (ta) ta.focus();
}

// Close reject modal
function closeRejectModal() {
  const modal = document.getElementById('rejectModal');
  if (!modal) return;
  modal.classList.remove('active');
  const form = document.getElementById('rejectForm');
  if (form) form.reset();
  const cc = document.getElementById('charCount');
  if (cc) cc.textContent = '0';
}

// Outside click to close
document.getElementById('rejectModal')?.addEventListener('click', e => {
  if (e.target === e.currentTarget) closeRejectModal();
});

// Escape key to close
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeRejectModal();
});

// Legacy prompt-based reject (kept for compatibility)
function handleReject() {
  const reason = prompt('Please provide a detailed reason for rejection:');
  if (reason && reason.trim().length >= 10) {
    const form = document.getElementById('rejectForm');
    if (form) {
      const hidden = document.createElement('input');
      hidden.type = 'hidden';
      hidden.name = 'rejection_reason';
      hidden.value = reason.trim();
      form.appendChild(hidden);
      form.submit();
    }
  } else if (reason !== null) {
    alert('Rejection reason (min 10 chars) is required. Please try again.');
  }
}
