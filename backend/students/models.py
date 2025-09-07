from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator
from django.conf import settings
from django.utils.crypto import get_random_string
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
#from exams.models import ExamPaper


# Constants
SCHOOL_LEVELS = [
    ('PP', 'Pre-Primary'),
    ('LP', 'Lower Primary'),
    ('UP', 'Upper Primary'),
    ('LS', 'Lower Secondary'),
    ('SS', 'Senior Secondary')
]

GRADE_LEVELS = [
    ('PP1', 'Pre-Primary 1'),
    ('PP2', 'Pre-Primary 2'),
    ('G1', 'Grade 1'),
    ('G2', 'Grade 2'),
    ('G3', 'Grade 3'),
    ('G4', 'Grade 4'),
    ('G5', 'Grade 5'),
    ('G6', 'Grade 6'),
    ('J7', 'Junior Secondary Grade 7'),
    ('J8', 'Junior Secondary Grade 8'),
    ('J9', 'Junior Secondary Grade 9'),
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('U', 'Undisclosed')
]

class Class(models.Model):
    grade_level = models.CharField(max_length=3, choices=GRADE_LEVELS)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2100)])

    class Meta:
        verbose_name_plural = "Classes"
        unique_together = ('grade_level', 'year')

    def __str__(self):
        return f"{self.get_grade_level_display()} ({self.year})"

class Stream(models.Model):
    name = models.CharField(max_length=50)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='streams')
    year = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ('name', 'class_ref', 'year')
        ordering = ['class_ref', 'name']

    def __str__(self):
        return f"{self.class_ref} - {self.name}"


class Student(models.Model):
    # other fields...
    admission_number = models.CharField(max_length=9, unique=True, blank=True)

    class Meta:
        ordering = ['admission_number']

    def save(self, *args, **kwargs):
        if not self.admission_number:
            current_year = timezone.now().year
            last_admission = (
                Student.objects
                .filter(admission_number__startswith=str(current_year))
                .order_by('-admission_number')
                .first()
            )

            if last_admission:
                try:
                    last_seq = int(last_admission.admission_number.split('-')[1])
                except (IndexError, ValueError):
                    last_seq = 0
            else:
                last_seq = 0

            next_seq = last_seq + 1
            if next_seq > 9999:
                raise ValidationError("Maximum admission number limit reached for this year.")

            self.admission_number = f"{current_year}-{next_seq:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.admission_number})"


     
     
    def generate_admission_number(self):
        # Customize this logic as needed
        return f"ADM{get_random_string(6).upper()}"
    
    legacy_admission_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        unique=True,
        verbose_name="Legacy Admission Number",
        help_text="Original admission number from legacy system"
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    class_ref = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    date_admitted = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_contact = models.CharField(max_length=20, blank=True)
    guardian_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['admission_number']),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.admission_number})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def current_age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_core = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

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

    class Meta:
        unique_together = ('name', 'year')
        ordering = ['-year', 'start_date']

    def __str__(self):
        return f"{self.name} {self.year}"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='scores')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='scores')
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=2, blank=True)
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

class StudentPromotionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='promotion_history')
    from_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='promoted_from')
    from_stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, related_name='promoted_stream_from')
    to_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='promoted_to')
    to_stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, related_name='promoted_stream_to')
    reason = models.CharField(max_length=100, default='Promotion')  # e.g. Promotion, Correction, Transfer
    date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f"{self.student} promoted to {self.to_class} - {self.to_stream} on {self.date}"



phone_validator = RegexValidator(
    regex=r'^(?:\+?254|0)?(7|1)\d{8}$',
    message="Enter a valid Kenyan phone number (e.g. 0712345678 or +254712345678)"
)

guardian_contact = models.CharField(
    max_length=20,
    blank=True,
    validators=[phone_validator],
    help_text="Phone number for guardian"
)

emergency_contact = models.CharField(
    max_length=20,
    blank=True,
    validators=[phone_validator],
    help_text="Alternate phone number for emergencies"
)


