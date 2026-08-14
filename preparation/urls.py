from django.urls import path
from . import views

app_name = "preparation"

urlpatterns = [
    path("preparation/", views.preparation, name="preparation"),
    path("event/<int:event_id>/", views.preparation, name="event_preparation"),
    path("toggle/<int:item_id>/", views.toggle_check, name="toggle_check"),
]