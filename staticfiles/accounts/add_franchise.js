document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('franchiseForm');
  const submitBtn = document.getElementById('submitBtn');
  const inputs = form.querySelectorAll('input, textarea, select');
  const progressSteps = document.querySelectorAll('.progress-step');
  const sections = document.querySelectorAll('.form-section');

  inputs.forEach(input => {
    input.addEventListener('input', () => { validateField(input); updateProgress(); });
    input.addEventListener('blur', () => validateField(input));
  });

  function validateField(field) {
    const group = field.closest('.form-group');
    if (!group) return true;
    const existing = group.querySelector('.validation-message');
    if (existing) existing.remove();
    field.classList.remove('error');

    let valid = true;
    let msg = '';

    if (field.hasAttribute('required') && !field.value.trim()) {
      valid = false; msg = 'This field is required';
    } else if (field.type === 'email' && field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) {
      valid = false; msg = 'Please enter a valid email address';
    } else if (field.type === 'number' && field.value) {
      const num = parseFloat(field.value);
      if (isNaN(num) || num < 0) { valid = false; msg = 'Please enter a valid positive number'; }
    }

    if (!valid) {
      field.classList.add('error');
      group.insertAdjacentHTML('beforeend', `
        <div class="validation-message error">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>${msg}
        </div>`);
    } else if (field.value.trim()) {
      group.insertAdjacentHTML('beforeend', `
        <div class="validation-message success">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>Looks good!
        </div>`);
    }
    return valid;
  }

  function updateProgress() {
    sections.forEach((section, idx) => {
      const inputs = section.querySelectorAll('input, textarea, select');
      const filled = Array.from(inputs).filter(i => i.value.trim() !== '' || !i.hasAttribute('required'));
      const step = progressSteps[idx];
      const divider = step.nextElementSibling;

      if (filled.length === inputs.length) {
        step.classList.add('completed'); step.classList.remove('active','inactive');
        if (divider && divider.classList.contains('step-divider')) divider.classList.add('completed');
      } else if (filled.length > 0) {
        step.classList.add('active'); step.classList.remove('completed','inactive');
      } else {
        step.classList.add('inactive'); step.classList.remove('active','completed');
        if (divider && divider.classList.contains('step-divider')) divider.classList.remove('completed');
      }
    });
  }

  // Description counter
  const descriptionField = document.querySelector('textarea[name="description"]');
  const countDisplay = document.getElementById('descriptionCount');
  if (descriptionField && countDisplay) {
    const updateCount = () => {
      const len = descriptionField.value.length;
      countDisplay.textContent = len;
      countDisplay.style.color =
        len > 1000 ? 'var(--error)' :
        len > 800 ? 'var(--warning)' :
        'var(--text-light)';
    };
    descriptionField.addEventListener('input', updateCount);
    updateCount();
  }

  // Image upload
  const imageInput = document.querySelector('input[name="image"]');
  const uploadArea = document.getElementById('uploadArea');
  const imagePreview = document.getElementById('imagePreview');
  const previewImage = document.getElementById('previewImage');

  if (imageInput && uploadArea) {
    uploadArea.addEventListener('click', () => imageInput.click());
    imageInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        if (file.size > 5 * 1024 * 1024) { alert('File size must be less than 5MB'); imageInput.value=''; return; }
        const reader = new FileReader();
        reader.onload = ev => {
          previewImage.src = ev.target.result;
          uploadArea.classList.add('hidden');
          imagePreview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
      }
    });

    ['dragenter','dragover','dragleave','drop'].forEach(evt => {
      uploadArea.addEventListener(evt, preventDefaults, false);
      document.body.addEventListener(evt, preventDefaults, false);
    });

    function preventDefaults(e){ e.preventDefault(); e.stopPropagation(); }
    ['dragenter','dragover'].forEach(evt => uploadArea.addEventListener(evt, () => uploadArea.classList.add('dragover'), false));
    ['dragleave','drop'].forEach(evt => uploadArea.addEventListener(evt, () => uploadArea.classList.remove('dragover'), false));

    uploadArea.addEventListener('drop', e => {
      const files = e.dataTransfer.files;
      if (files.length) {
        imageInput.files = files;
        imageInput.dispatchEvent(new Event('change',{bubbles:true}));
      }
    });
  }

  // Generic file uploads
  setupFileUpload('brochureInput','brochureUploadArea','brochurePreview','brochureFileName',10);
  setupFileUpload('businessPlanInput','businessPlanUploadArea','businessPlanPreview','businessPlanFileName',10);

  function setupFileUpload(inputId, areaId, previewId, nameSpanId, maxMB){
    const input = document.getElementById(inputId);
    const area = document.getElementById(areaId);
    const preview = document.getElementById(previewId);
    const nameSpan = document.getElementById(nameSpanId);
    if (!input || !area) return;
    area.addEventListener('click', () => input.click());
    input.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      if (file.size > maxMB * 1024 * 1024){ alert(`File size must be less than ${maxMB}MB`); input.value=''; return; }
      nameSpan.textContent = file.name;
      area.classList.add('hidden');
      preview.classList.remove('hidden');
    });
  }

  form.addEventListener('submit', e => {
    let ok = true;
    form.querySelectorAll('[required]').forEach(f => { if(!validateField(f)) ok=false; });
    if (!ok){
      e.preventDefault();
      const firstError = form.querySelector('.validation-message.error');
      if (firstError) firstError.scrollIntoView({behavior:'smooth',block:'center'});
      return;
    }
    submitBtn.disabled = true;
    submitBtn.classList.add('btn-loading');
    submitBtn.innerHTML = `
      <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
      </svg>Creating...`;
  });

  updateProgress();
});

// Global functions
function removeImage(){
  const imageInput = document.querySelector('input[name="image"]');
  const uploadArea = document.getElementById('uploadArea');
  const imagePreview = document.getElementById('imagePreview');
  if (!imageInput) return;
  imageInput.value='';
  uploadArea.classList.remove('hidden');
  imagePreview.classList.add('hidden');
}

function removeFile(type){
  if (type === 'brochure') {
    resetFile('brochureInput','brochureUploadArea','brochurePreview');
  } else if (type === 'business_plan') {
    resetFile('businessPlanInput','businessPlanUploadArea','businessPlanPreview');
  }
}

function resetFile(inputId, areaId, previewId){
  const input = document.getElementById(inputId);
  const area = document.getElementById(areaId);
  const preview = document.getElementById(previewId);
  if (!input) return;
  input.value='';
  area.classList.remove('hidden');
  preview.classList.add('hidden');
}
