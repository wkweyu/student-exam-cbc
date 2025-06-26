from rest_framework import serializers
from .models import Subject, StreamSubject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StreamSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamSubject
        fields = '__all__'
