from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import (
    ClassViewSet, 
    StreamViewSet, 
    StudentViewSet,
    StudentRegistrationView,
    StudentListView,
    StudentDetailView,
    student_register_page,
    student_list,
    transfer_student,
    test_base,
    student_transfer_search,
    get_streams_by_class,
    student_transfer_or_promote,
    promote_class_students,
    class_list_view

)
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'streams', StreamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('register-form/', student_register_page, name='student-register-form'),
    path('student-list/', student_list, name='student-list'),
    path('register/success/', lambda r: render(r, 'students/success.html'), name='student_success'),
    path('list/', StudentListView.as_view(), name='student_list'),
    path('list/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:student_id>/transfer/', transfer_student, name='transfer_student'),
    path('test-base/', test_base, name='test_base'),
    path('transfer/', student_transfer_search, name='student_transfer_search'),
    path('transfer/<int:student_id>/', transfer_student, name='transfer_student'),
    path('ajax/get-streams/', get_streams_by_class, name='get_streams_by_class'),
    path('student/transfer-promote/', student_transfer_or_promote, name='student_transfer_or_promote'),
    path('promote/<int:class_id>/', promote_class_students, name='promote_class_students'),
    path('classes/', class_list_view, name='class_list'),
    



    
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)