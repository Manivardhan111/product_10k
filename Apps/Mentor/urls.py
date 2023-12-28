from django.urls import path
from . import views
from ..SalesPerson import views as admin
urlpatterns = [
    path("", views.mentor_sample, name="mentor_sample"),
    path("mentor/admin-login/", views.admin_login, name="mentor_admin_login"),
    path("mentor/admin-login/add-email/<str:added_email>/",
         views.admin_login, name="mentor_login_addemail"),
    path("mentor/mentor/", views.mentor_api, name="mentor_api")
]
