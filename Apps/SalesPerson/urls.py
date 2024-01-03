from django.urls import path
from . import views
urlpatterns = [
    path("salesperson/sample/", views.salesperson_sample,
         name="salesperson_sample"),
    path("salesperson/admin-login/", views.admin_login, name="admin_login"),
    path("salesperson/admin-login/add-salesperson/<str:added_email>/",
         views.admin_login, name="admin_login_addemail"),
    path("salesperson/register-salesperson/", views.salesperson_registration,
         name="admin-salesperson"),
    path("salesperson/get-interested-students/<str:sp_email>/",
         views.get_intrested_students, name="get_interested_students"),
    path("salesperson/get-registered-students/<str:sp_email>/",
         views.get_registered_students, name="get_registered_students"),
]
