from django.db import models
from users.models import CustomUser
from students.models import Stream

class Subject(models.Model):
    name = models.CharField(max_length=100)
    

class StreamSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, limit_choices_to={'role': 'teacher'}, on_delete=models.CASCADE)
