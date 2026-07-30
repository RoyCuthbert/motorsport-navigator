from django.urls import path
from . import views

app_name = "preparation"

urlpatterns = [
    path("preparation/", views.preparation, name="preparation"),
]