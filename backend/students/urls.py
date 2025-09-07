from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'students'  # Add namespace

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='student')
router.register('classes', views.ClassViewSet, basename='class')
router.register('streams', views.StreamViewSet, basename='stream')

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # Web views
    path('register/', views.StudentRegistrationView.as_view(), name='student-register'),
    path('register-form/', views.student_register_page, name='student-register-form'),
    path('list/', views.StudentListView.as_view(), name='student-list'),
    
    # Add other patterns one at a time
]