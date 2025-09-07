from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Student Exam CBC System!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Students app routes
    path('api/students/', include('students.urls', namespace='students')),
]
