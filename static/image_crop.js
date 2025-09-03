// Image crop flow for signup profile image
(function () {
  let cropper = null;
  const input = document.getElementById('file-upload');
  const modal = document.getElementById('cropper-modal');
  const img = document.getElementById('cropper-image');
  const previewBox = document.getElementById('cropper-preview');
  const profilePreviewImg = document.getElementById('profile-preview-img');
  const profilePreviewIcon = document.getElementById('profile-preview-icon');
  const btnClose = document.getElementById('cropper-close');
  const btnCancel = document.getElementById('cropper-cancel');
  const btnApply = document.getElementById('cropper-apply');

  if (!input || !modal || !img) return;

  const openModal = () => {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
  };
  const closeModal = () => {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
  };

  input.addEventListener('change', (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    img.src = url;
    openModal();
    // Wait image loaded
    img.onload = () => {
      if (cropper) cropper.destroy();
      cropper = new Cropper(img, {
        viewMode: 1,
        aspectRatio: 1,
        dragMode: 'move',
        autoCropArea: 1,
        background: false,
        guides: false,
        movable: true,
        zoomable: true,
        responsive: true,
        preview: previewBox ? previewBox : undefined,
        ready() {
          // circle preview via CSS mask using container (visual only)
        },
      });
    };
  });

  const toFile = (blob, fileName) => new File([blob], fileName, { type: blob.type, lastModified: Date.now() });

  const replaceInputFile = (file) => {
    // Replace the file in the input by using DataTransfer
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
  };

  btnApply && btnApply.addEventListener('click', async () => {
    if (!cropper) return;
    cropper.getCroppedCanvas({ width: 512, height: 512, imageSmoothingQuality: 'high' }).toBlob((blob) => {
      if (!blob) return;
      const file = toFile(blob, 'profile_cropped.png');
      replaceInputFile(file);
      // 미리보기 반영
      if (profilePreviewImg) {
        profilePreviewImg.src = URL.createObjectURL(blob);
        profilePreviewImg.classList.remove('hidden');
      }
      if (profilePreviewIcon) {
        profilePreviewIcon.classList.add('hidden');
      }
      closeModal();
    }, 'image/png', 0.95);
  });

  [btnClose, btnCancel].forEach((b) => b && b.addEventListener('click', closeModal));
})();


