from rest_framework import serializers
from .models import GradingSystem

class GradingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingSystem
        fields = '__all__'
