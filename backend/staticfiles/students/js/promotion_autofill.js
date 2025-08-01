(function ($) {
  $(document).ready(function () {
    console.log("✅ Promotion form JS loaded");

    $("#id_student").on("change", function () {
      var studentId = $(this).val();
      if (!studentId) return;

      $.get(
        "/api/students/get-student-details/" + studentId + "/",
        function (data) {
          $("#id_from_class").val(data.class_id);
          $("#id_from_stream").val(data.stream_id);
        }
      );
    });
  });
})(django.jQuery);
