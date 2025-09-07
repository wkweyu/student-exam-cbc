(function ($) {
  $(document).ready(function () {
    $("#id_student").on("change", function () {
      var studentId = $(this).val();
      if (studentId) {
        $.get(
          "/api/students/get-student-details/" + studentId + "/",
          function (data) {
            $("#id_from_class").val(data.class_id);
            $("#id_from_stream").val(data.stream_id);
          }
        );
      } else {
        $("#id_from_class").val("");
        $("#id_from_stream").val("");
      }
    });
  });
})(django.jQuery);
