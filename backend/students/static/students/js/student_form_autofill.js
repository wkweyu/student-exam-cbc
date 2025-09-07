document.addEventListener("DOMContentLoaded", function () {
  // Highlight the class select element for better UX
  const classSelect = document.querySelector('select[name="class_ref"]');
  if (classSelect) {
    classSelect.addEventListener("change", function () {
      // Show loading indicator
      const streamSelect = document.querySelector('select[name="stream_ref"]');
      if (streamSelect) {
        streamSelect.disabled = true;
        streamSelect.innerHTML = '<option value="">Loading streams...</option>';
      }
    });
  }

  // Auto-focus on stream select when class is selected
  if (classSelect && classSelect.value) {
    const streamSelect = document.querySelector('select[name="stream_ref"]');
    if (streamSelect) streamSelect.focus();
  }
});
