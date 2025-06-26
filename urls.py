from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from students.views import StudentViewSet, ClassViewSet, StreamViewSet
from subjects.views import SubjectViewSet, StreamSubjectViewSet
from exams.views import *
from grading.views import GradingSystemViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'streams', StreamViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'stream-subjects', StreamSubjectViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'terms', TermViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'exam-papers', ExamPaperViewSet)
router.register(r'exam-results', ExamResultViewSet)
router.register(r'grading', GradingSystemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/', include(router.urls)),
    path("api/", include("exam.urls")),

]
