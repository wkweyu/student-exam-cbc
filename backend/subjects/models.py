from django.db import models
from users.models import CustomUser
from students.models import Stream


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_core = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"



class StreamSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, limit_choices_to={'role': 'teacher'}, on_delete=models.CASCADE)

