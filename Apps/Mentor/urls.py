from django.urls import path
from . import views
urlpatterns = [
    path("mentor/sample/", views.mentor_sample, name="mentor_sample")
]
