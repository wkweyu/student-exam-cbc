(function ($) {
  $(document).ready(function () {
    console.log("✅ Student form JS loaded");

    $("#id_class_ref").on("change", function () {
      var classId = $(this).val();
      var $streamSelect = $("#id_stream");

      if (classId) {
        $.get(
          "/api/students/get-streams-by-class/?class_id=" + classId,
          function (data) {
            $streamSelect.empty();
            $streamSelect.append('<option value="">---------</option>');
            data.forEach(function (stream) {
              $streamSelect.append(
                '<option value="' + stream.id + '">' + stream.name + "</option>"
              );
            });
          }
        );
      } else {
        $streamSelect.empty();
        $streamSelect.append('<option value="">---------</option>');
      }
    });
  });
})(django.jQuery);
