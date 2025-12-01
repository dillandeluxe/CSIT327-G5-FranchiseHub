(function() {
  // Character counter
  const textarea = document.getElementById('id_description');
  const charCount = document.getElementById('charCount');
  if (textarea && charCount) {
    textarea.addEventListener('input', function() {
      charCount.textContent = this.value.length;
    });
  }

  // Image upload handling
  const imageInput = document.getElementById('imageInput');
  const uploadZone = document.querySelector('.upload-zone');
  const existingImage = document.getElementById('existingImage');
  const newImagePreview = document.getElementById('newImagePreview');
  const previewImg = document.getElementById('previewImg');

  if (imageInput) {
    imageInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(ev) {
          previewImg.src = ev.target.result;
          if (uploadZone) uploadZone.classList.add('hidden');
          if (existingImage) existingImage.classList.add('hidden');
          newImagePreview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Document upload handlers
  const documents = ['brochure', 'business_plan'];
  documents.forEach(docType => {
    const inputId = docType === 'brochure' ? 'brochureInput' : 'businessPlanInput';
    const zoneId = docType === 'brochure' ? 'brochureUploadZone' : 'businessPlanUploadZone';
    const previewId = docType === 'brochure' ? 'brochurePreview' : 'businessPlanPreview';
    const nameId = docType === 'brochure' ? 'brochureName' : 'businessPlanName';
    const sizeId = docType === 'brochure' ? 'brochureSize' : 'businessPlanSize';

    const input = document.getElementById(inputId);
    const zone = document.getElementById(zoneId);
    const preview = document.getElementById(previewId);
    const nameEl = document.getElementById(nameId);
    const sizeEl = document.getElementById(sizeId);

    if (zone && input) {
      zone.addEventListener('click', () => input.click());
      input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
          if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB');
            this.value = '';
            return;
          }
          nameEl.textContent = file.name;
          sizeEl.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
          zone.classList.add('hidden');
          preview.classList.add('preview-active');
        }
      });
    }
  });
})();

// Global functions
function triggerImageUpload() {
  document.getElementById('imageInput')?.click();
}

function removeNewImage() {
  const imageInput = document.getElementById('imageInput');
  const uploadZone = document.querySelector('.upload-zone');
  const existingImage = document.getElementById('existingImage');
  const newImagePreview = document.getElementById('newImagePreview');

  if (imageInput) imageInput.value = '';
  if (newImagePreview) newImagePreview.classList.add('hidden');
  if (existingImage && !imageInput?.files?.length) {
    existingImage.classList.remove('hidden');
  } else if (uploadZone) {
    uploadZone.classList.remove('hidden');
  }
}

function removeDocument(type) {
  const inputId = type === 'brochure' ? 'brochureInput' : 'businessPlanInput';
  const zoneId = type === 'brochure' ? 'brochureUploadZone' : 'businessPlanUploadZone';
  const previewId = type === 'brochure' ? 'brochurePreview' : 'businessPlanPreview';

  const input = document.getElementById(inputId);
  const zone = document.getElementById(zoneId);
  const preview = document.getElementById(previewId);

  if (input) input.value = '';
  if (zone) zone.classList.remove('hidden');
  if (preview) preview.classList.remove('preview-active');
}
