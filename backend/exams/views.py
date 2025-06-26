from rest_framework import viewsets
from .models import Exam, ExamPaper, ExamResult, Term, AcademicYear
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from students.models import Student
from students.models import Student
from classes.models import ClassRoom

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamPaperViewSet(viewsets.ModelViewSet):
    queryset = ExamPaper.objects.all()
    serializer_class = ExamPaperSerializer

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    
@api_view(['POST'])
def bulk_exam_results_entry(request):
    """
    Expected format:
    {
        "exam_id": 1,
        "subject_id": 3,
        "results": [
            {"student_id": 10, "marks": 78.5},
            {"student_id": 11, "marks": 65},
            ...
        ]
    }
    """
    exam_id = request.data.get("exam_id")
    subject_id = request.data.get("subject_id")
    results = request.data.get("results", [])

    try:
        exam_paper = ExamPaper.objects.get(exam_id=exam_id, subject_id=subject_id)
    except ExamPaper.DoesNotExist:
        return Response({"error": "ExamPaper not found"}, status=400)

    for r in results:
        ExamResult.objects.update_or_create(
            student_id=r["student_id"],
            exam_paper=exam_paper,
            defaults={"marks": r["marks"]}
        )

    return Response({"status": "Results saved"})

@api_view(['GET'])
def list_students_by_class_stream(request):
    class_id = request.GET.get("class_id")
    stream_id = request.GET.get("stream_id")

    if not class_id or not stream_id:
        return Response([], status=400)

    students = Student.objects.filter(classroom_id=class_id, stream_id=stream_id)
    return Response(StudentSerializer(students, many=True).data)