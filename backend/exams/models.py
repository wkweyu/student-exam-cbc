from django.db import models
from subjects.models import Subject, Stream
from students.models import Student
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator




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
    EXAM_TYPES = [
        ('T1', 'Term 1'),
        ('T2', 'Term 2'),
        ('T3', 'Term 3'),
        ('MS', 'Mid Semester'),
        ('ES', 'End Semester'),
        ('AN', 'Annual')
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=2, choices=EXAM_TYPES)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.name} - {self.stream}"

    class Meta:
        unique_together = ('name', 'year')
        ordering = ['-year', 'start_date']

    def __str__(self):
        return f"{self.name} {self.year}"

class ExamPaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='papers')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_papers')
    duration_minutes = models.PositiveIntegerField(default=60)
    total_marks = models.PositiveIntegerField(default=100)

    class Meta:
        unique_together = ('exam', 'subject')

    def __str__(self):
        return f"{self.subject.name} - {self.exam.name}"



class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='scores')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='scores')
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=2, blank=True)
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    marks = models.FloatField()
    comment = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'subject', 'exam')
        verbose_name = "Exam Score"
        verbose_name_plural = "Exam Scores"

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"

    def save(self, *args, **kwargs):
        if not self.grade:
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def calculate_grade(self):
        if self.score >= 80:
            return 'A'
        elif self.score >= 70:
            return 'B'
        elif self.score >= 60:
            return 'C'
        elif self.score >= 50:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return f"{self.exam} - {self.subject}"


class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="exam_results")
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='exam_results',
        db_constraint= False
    )
    exam_paper = models.ForeignKey('ExamPaper', on_delete=models.CASCADE)
    marks = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        #db_table = 'students_examresult'  # Explicit table name
        managed = True
        unique_together = ('student', 'exam_paper', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.marks})"
        verbose_name = 'Exam Result'
        verbose_name_plural = 'Exam Results'
        
