(function() {
  let currentStep = 1;
  const totalSteps = 4;

  const form = document.getElementById('applicationForm');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const submitBtn = document.getElementById('submitBtn');
  const progressLine = document.getElementById('progressLine');

  // Initialize file uploads
  document.querySelectorAll('.file-upload-zone').forEach(zone => {
    const inputId = zone.dataset.input;
    const input = document.getElementById(inputId);
    
    zone.addEventListener('click', () => input.click());
    
    // Drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      zone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
      zone.addEventListener(eventName, () => zone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      zone.addEventListener(eventName, () => zone.classList.remove('dragover'), false);
    });

    zone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      input.files = files;
      handleFileSelect({ target: input });
    }

    input.addEventListener('change', handleFileSelect);
  });

  function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    const inputId = e.target.id;
    const preview = document.getElementById(`${inputId}-preview`);
    
    preview.innerHTML = `
      <div class="file-icon">
        <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/>
        </svg>
      </div>
      <div class="file-info">
        <div class="file-name">${file.name}</div>
        <div class="file-size">${(file.size / 1024 / 1024).toFixed(2)} MB</div>
      </div>
      <button type="button" class="file-remove" onclick="removeFile('${inputId}')">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </button>
    `;
    preview.classList.add('active');
  }

  window.removeFile = function(inputId) {
    document.getElementById(inputId).value = '';
    document.getElementById(`${inputId}-preview`).classList.remove('active');
  };

  nextBtn.addEventListener('click', () => {
    if (validateStep(currentStep)) {
      if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
      }
    }
  });

  prevBtn.addEventListener('click', () => {
    if (currentStep > 1) {
      currentStep--;
      showStep(currentStep);
    }
  });

  function showStep(step) {
    document.querySelectorAll('.form-section').forEach(section => {
      section.classList.remove('active');
    });
    document.querySelector(`.form-section[data-step="${step}"]`).classList.add('active');

    document.querySelectorAll('.step').forEach((s, i) => {
      s.classList.remove('active', 'completed');
      if (i + 1 < step) s.classList.add('completed');
      if (i + 1 === step) s.classList.add('active');
    });

    // Update progress line
    const progress = ((step - 1) / (totalSteps - 1)) * 100;
    if (progressLine) progressLine.style.width = `${progress}%`;

    // Show/hide buttons using classes (avoid inline styles)
    prevBtn.classList.toggle('hidden', step === 1);
    nextBtn.classList.toggle('hidden', step === totalSteps);
    submitBtn.classList.toggle('hidden', step !== totalSteps);

    // Show review on last step
    if (step === totalSteps) {
      showReview();
    }
  }

  function validateStep(step) {
    const section = document.querySelector(`.form-section[data-step="${step}"]`);
    const inputs = section.querySelectorAll('[required]');
    let valid = true;

    inputs.forEach(input => {
      if (!input.value.trim()) {
        input.style.borderColor = 'var(--error)';
        valid = false;
      } else {
        input.style.borderColor = 'var(--success)';
      }
    });

    return valid;
  }

  function showReview() {
    const fullName = document.querySelector('[name="full_name"]').value;
    const email = document.querySelector('[name="email"]').value;
    const phone = document.querySelector('[name="phone"]').value;
    const experience = document.querySelector('[name="experience"]').value;

    const files = ['resume', 'business_proposal', 'financial_statement']
      .map(id => {
        const file = document.getElementById(id).files[0];
        return file ? `<li>${file.name}</li>` : '';
      })
      .filter(Boolean)
      .join('');

    document.getElementById('reviewContent').innerHTML = `
      <h5 style="margin-bottom: 16px; font-size: 18px; font-weight: 700;">Your Information</h5>
      <p style="margin-bottom: 8px;"><strong>Name:</strong> ${fullName}</p>
      <p style="margin-bottom: 8px;"><strong>Email:</strong> ${email}</p>
      <p style="margin-bottom: 8px;"><strong>Phone:</strong> ${phone || 'Not provided'}</p>
      <p style="margin-bottom: 16px;"><strong>Experience:</strong> ${experience || 'Not provided'}</p>
      ${files ? `<h5 style="margin-bottom: 8px; font-size: 16px; font-weight: 700;">Uploaded Documents</h5><ul style="margin-left: 20px;">${files}</ul>` : ''}
    `;
  }

  form.addEventListener('submit', (e) => {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Submitting...</span>';
  });

  // Ensure initial state is correct on load
  showStep(currentStep);
})();
