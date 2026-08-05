from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="events"),
    path("add/", views.add_event, name="add_event"),
    path("select/<int:event_id>/", views.select_event, name="select_event"),
    path("edit/<int:event_id>/", views.edit_event, name="edit_event"),
     path("delete/<int:event_id>/", views.delete_event, name="delete_event"),
]