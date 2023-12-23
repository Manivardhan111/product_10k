from django.urls import path
from . import views
urlpatterns = [
    path("student/sample/", views.student_sample, name="student_sample"),
    path("student/interestedstudents/", views.interested_student,
         name='interested_student_post'),
    path("student/interested-students/<str:sp_email>/",
         views.interested_student, name='interested_student_get'),
    path("student/student-login/", views.student_login, name="student_login")

]
