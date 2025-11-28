// Password Strength Checker
function checkPasswordStrength(password) {
  let strength = 0;
  const strengthBar = document.getElementById('strengthBar');
  const strengthText = document.getElementById('strengthText');

  if (!strengthBar || !password) return;

  if (password.length >= 8) strength += 25;
  if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 25;
  if (password.match(/\d/)) strength += 25;
  if (password.match(/[^a-zA-Z\d]/)) strength += 25;

  strengthBar.style.width = strength + '%';

  if (strength <= 25) {
    strengthBar.style.background = '#ef4444';
    strengthText.textContent = 'Weak password';
    strengthText.style.color = '#ef4444';
  } else if (strength <= 50) {
    strengthBar.style.background = '#f59e0b';
    strengthText.textContent = 'Fair password';
    strengthText.style.color = '#f59e0b';
  } else if (strength <= 75) {
    strengthBar.style.background = '#3b82f6';
    strengthText.textContent = 'Good password';
    strengthText.style.color = '#3b82f6';
  } else {
    strengthBar.style.background = '#10b981';
    strengthText.textContent = 'Strong password';
    strengthText.style.color = '#10b981';
  }
}

// Toggle Password Visibility
function togglePassword(fieldId) {
  const field = document.getElementById(fieldId);
  const icon = document.getElementById(fieldId + '-icon');
  
  if (field.type === 'password') {
    field.type = 'text';
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
  } else {
    field.type = 'password';
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
  }
}

// Form Validation
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return true;

  let isValid = true;

  form.querySelectorAll('[required]').forEach(input => {
    const formGroup = input.closest('.form-group');
    const errorSpan = formGroup.querySelector('.form-error');

    if (!input.value.trim()) {
      formGroup.classList.add('has-error');
      if (errorSpan) errorSpan.textContent = 'This field is required';
      isValid = false;
    } else {
      formGroup.classList.remove('has-error');
      if (errorSpan) errorSpan.textContent = '';
    }
  });

  // Password match validation
  const password = form.querySelector('[name="password"]');
  const confirmPassword = form.querySelector('[name="confirm_password"]');
  
  if (password && confirmPassword && password.value && confirmPassword.value) {
    if (password.value !== confirmPassword.value) {
      const formGroup = confirmPassword.closest('.form-group');
      const errorSpan = formGroup.querySelector('.form-error');
      formGroup.classList.add('has-error');
      if (errorSpan) errorSpan.textContent = 'Passwords do not match';
      isValid = false;
    }
  }

  return isValid;
}

// Form Submit Handler
function setupFormSubmit(formId) {
  const form = document.getElementById(formId);
  const submitBtn = document.getElementById('submitBtn');

  if (!form || !submitBtn) return;

  form.addEventListener('submit', function(e) {
    if (!validateForm(formId)) {
      e.preventDefault();
      return false;
    }

    // Show loading state
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    if (btnText && btnLoader) {
      btnText.style.display = 'none';
      btnLoader.style.display = 'inline-block';
    }
    
    submitBtn.disabled = true;
  });
}

// Real-time validation
function setupRealTimeValidation() {
  document.querySelectorAll('.form-input[required]').forEach(input => {
    input.addEventListener('blur', function() {
      const formGroup = this.closest('.form-group');
      const errorSpan = formGroup.querySelector('.form-error');

      if (!this.value.trim()) {
        formGroup.classList.add('has-error');
        if (errorSpan) errorSpan.textContent = 'This field is required';
      } else {
        formGroup.classList.remove('has-error');
        if (errorSpan) errorSpan.textContent = '';
      }
    });

    input.addEventListener('input', function() {
      if (this.value.trim()) {
        const formGroup = this.closest('.form-group');
        formGroup.classList.remove('has-error');
      }
    });
  });

  // Password strength check
  const passwordInput = document.getElementById('password') || document.getElementById('new_password');
  if (passwordInput) {
    passwordInput.addEventListener('input', function() {
      checkPasswordStrength(this.value);
    });
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  setupRealTimeValidation();
  
  // Setup form submit handlers
  setupFormSubmit('registerForm');
  setupFormSubmit('loginForm');
  setupFormSubmit('forgotForm');
  setupFormSubmit('securityForm');
  setupFormSubmit('resetForm');

  // Auto-dismiss messages after 5 seconds
  setTimeout(() => {
    document.querySelectorAll('.message-alert').forEach(alert => {
      alert.style.animation = 'slideOut 0.3s ease-out';
      setTimeout(() => alert.remove(), 300);
    });
  }, 5000);
});

// Slide out animation
const style = document.createElement('style');
style.textContent = `
  @keyframes slideOut {
    to {
      opacity: 0;
      transform: translateY(-20px);
    }
  }
`;
document.head.appendChild(style);

// ✅ PREVENT BROWSER BACK BUTTON FROM BYPASSING LOGOUT
(function() {
    'use strict';

    // Function to detect if user is on an authenticated page
    function isAuthenticatedPage() {
        const path = window.location.pathname;
        const authPages = [
            '/accounts/browse/',
            '/accounts/profile/',
            '/accounts/franchisor/dashboard/',
            '/accounts/franchisee/dashboard/',
            '/accounts/admin-dashboard/',
            '/accounts/franchise/',
            '/accounts/franchisor/',
            '/accounts/application/'
        ];
        return authPages.some(page => path.includes(page));
    }

    // Prevent back navigation to authenticated pages after logout
    if (isAuthenticatedPage()) {
        // Push current state
        window.history.pushState(null, null, window.location.href);
        
        // Handle back button
        window.addEventListener('popstate', function(event) {
            // Push state again to prevent going back
            window.history.pushState(null, null, window.location.href);
        });
    }

    // Clear any cached authentication state on logout
    window.addEventListener('beforeunload', function() {
        if (window.location.pathname.includes('/logout')) {
            // Clear storage
            sessionStorage.clear();
            
            // Prevent caching
            if (window.performance && window.performance.navigation.type === 1) {
                // Clear browser cache
                window.location.reload(true);
            }
        }
    });

    // Redirect to login if accessing authenticated page when logged out
    window.addEventListener('pageshow', function(event) {
        // Check if page was loaded from cache
        if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
            // If on authenticated page but no session, redirect to login
            const isAuthPage = isAuthenticatedPage();
            if (isAuthPage) {
                // Force reload to check authentication status
                window.location.reload(true);
            }
        }
    });

})();

// ✅ FORM VALIDATION AND ERROR HANDLING
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            const btnText = submitBtn.querySelector('.btn-text');
            const btnLoader = submitBtn.querySelector('.btn-loader');
            
            // Show loading state
            if (btnText && btnLoader) {
                submitBtn.disabled = true;
                btnText.style.display = 'none';
                btnLoader.style.display = 'inline-block';
            }
        });
    });

    // Real-time form validation
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    function validateField(field) {
        const formGroup = field.closest('.form-group');
        const errorSpan = formGroup.querySelector('.form-error');
        
        if (field.hasAttribute('required') && !field.value.trim()) {
            formGroup.classList.add('has-error');
            if (errorSpan) {
                errorSpan.textContent = 'This field is required';
                errorSpan.style.display = 'block';
            }
            return false;
        } else {
            formGroup.classList.remove('has-error');
            if (errorSpan) {
                errorSpan.textContent = '';
                errorSpan.style.display = 'none';
            }
            return true;
        }
    }
});
