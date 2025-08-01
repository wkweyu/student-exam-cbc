document.addEventListener("DOMContentLoaded", function () {
  // Photo preview
  const photoInput = document.getElementById("id_photo");
  if (photoInput) {
    photoInput.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          let preview = document.getElementById("photo-preview");
          if (!preview) {
            preview = document.createElement("div");
            preview.id = "photo-preview";
            preview.className = "image-preview";
            photoInput.parentNode.appendChild(preview);
          }
          preview.innerHTML = `<img src="${e.target.result}" class="image-preview">`;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Class-stream dependency
  const classSelect = document.getElementById("id_class_ref");
  const streamSelect = document.getElementById("id_stream");

  if (classSelect && streamSelect) {
    classSelect.addEventListener("change", function () {
      const classId = this.value;
      if (classId) {
        fetch(`/api/streams/?class_ref=${classId}`)
          .then((response) => response.json())
          .then((data) => {
            streamSelect.innerHTML = "";
            data.forEach((stream) => {
              const option = document.createElement("option");
              option.value = stream.id;
              option.textContent = stream.name;
              streamSelect.appendChild(option);
            });
          });
      }
    });
  }
});
