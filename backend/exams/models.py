from django.db import models
from subjects.models import Subject, Stream
from students.models import Student

class AcademicYear(models.Model):
    year = models.PositiveIntegerField(unique=True)

class Term(models.Model):
    name = models.CharField(max_length=20)
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

class Exam(models.Model):
    name = models.CharField(max_length=50)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    weight = models.FloatField(default=1.0)

class ExamPaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_marks = models.PositiveIntegerField()

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    marks = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'exam_paper', 'subject')
