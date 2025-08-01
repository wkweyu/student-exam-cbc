from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'students'

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='student')
router.register('classes', views.ClassViewSet, basename='class')
router.register('streams', views.StreamViewSet, basename='stream')

urlpatterns = [
    path('', include(router.urls)),

    # Web views
    path('register/', views.StudentRegistrationView.as_view(), name='student-register'),
    path('register-form/', views.student_register_page, name='student-register-form'),
    path('list/', views.StudentListView.as_view(), name='student-list'),
    path('promote-students-batch/', views.promote_students_batch, name='promote_students_batch'),
    path('transfer-or-promote/', views.student_transfer_or_promote, name='student_transfer_or_promote'),
    path('get-streams-by-class/', views.get_streams_by_class, name='get_streams_by_class'),
    path('get-student-details/<int:student_id>/', views.get_student_details, name='get_student_details'),
]
