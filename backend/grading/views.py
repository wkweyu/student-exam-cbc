from rest_framework import viewsets
from .models import GradingSystem
from .serializers import GradingSystemSerializer

class GradingSystemViewSet(viewsets.ModelViewSet):
    queryset = GradingSystem.objects.all()
    serializer_class = GradingSystemSerializer
