from rest_framework import viewsets
from .models import Subject, StreamSubject
from .serializers import SubjectSerializer, StreamSubjectSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StreamSubjectViewSet(viewsets.ModelViewSet):
    queryset = StreamSubject.objects.all()
    serializer_class = StreamSubjectSerializer
