from django.urls import path
from . import views
urlpatterns = [
    path("salesperson/sample/", views.salesperson_sample,
         name="salesperson_sample"),
    path("salesperson/admin-login/", views.admin_login, name="admin_login"),
    path("salesperson/admin-login/add-email/<str:added_email>/",
         views.admin_login, name="admin_login_addemail"),
    path("salesperson/admin-salesperson/", views.admin_salesperson_api,
         name="admin-salesperson"),
]
