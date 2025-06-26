from django.db import models

class GradingSystem(models.Model):
    grade = models.CharField(max_length=2)
    min_score = models.FloatField()
    max_score = models.FloatField()
    comment = models.CharField(max_length=100)
