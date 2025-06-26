from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse


# A simple test view
def home(request):
    return HttpResponse("Welcome to the Student Exam CBC System!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/auth/', include('dj_rest_auth.urls')),  # Login, logout, password reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Signup
    path('api/students/', include('students.urls')),

]

