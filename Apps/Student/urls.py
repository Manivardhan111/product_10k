from django.urls import path
from . import views
urlpatterns = [
    path("student/sample/",views.student_sample,name="sample"),
    path("student/interested-student/",
         views.interested_student, name="intrested_student"),
    path("student/register-student/",
         views.student_registration, name="register_student"),
    path("student/student-login/", views.student_login, name="student_login"),
    path("student/pre-assessment-questions/",
         views.assessment_exam, name="pre_assessment_exam"),
    path("student/forgot-password/", views.forgot_password,
         name="student_forgot_password"),
    path("student/verify-otp/", views.verify_otp,
         name="student_verify_otp"),
    path("student/change-password/", views.change_password,
         name="student_change_password")
]
