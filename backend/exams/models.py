from django.db import models
from subjects.models import Subject, Stream
from students.models import Student


class AcademicYear(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.year)


class Term(models.Model):
    name = models.CharField(max_length=20)
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.year}"


class Exam(models.Model):
    name = models.CharField(max_length=50)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.name} - {self.stream}"


class ExamPaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_marks = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.exam} - {self.subject}"


class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="exam_results")
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE, related_name="results")
    marks = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'exam_paper', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.marks})"
