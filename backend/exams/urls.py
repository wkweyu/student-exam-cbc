from django.urls import path
from .views import (
    list_academic_years, list_terms, list_exams, list_subjects,
    list_streams, list_classes, list_students_by_class_stream,
    bulk_exam_results_entry
)

urlpatterns = [
    path("academic-years/", list_academic_years),
    path("terms/", list_terms),
    path("exams/", list_exams),
    path("subjects/", list_subjects),
    path("streams/", list_streams),
    path("classes/", list_classes),
    path("students/", list_students_by_class_stream),
    path("results/bulk/", bulk_exam_results_entry),
]
