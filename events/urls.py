from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="events"),
    path("dashboard/", views.season_dashboard, name="season_dashboard"),
    path("add/", views.add_event, name="add_event"),
    path("select/<int:event_id>/", views.select_event, name="select_event"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path("<int:event_id>/cancel/", views.cancel_event, name="cancel_event"),
    path("<int:event_id>/reopen/", views.reopen_event, name="reopen_event"),
    path("edit/<int:event_id>/", views.edit_event, name="edit_event"),
    path("<int:event_id>/review/", views.edit_event_review, name="edit_event_review",),
    path("delete/<int:event_id>/", views.delete_event, name="delete_event"),
    path("<int:event_id>/tasks/add/", views.add_event_task, name="add_event_task"),
    path("tasks/<int:task_id>/edit/", views.edit_event_task, name="edit_event_task"),
    path("tasks/<int:task_id>/toggle", views.toggle_event_task, name="toggle_event_task"),
    path("tasks/<int:task_id>/delete/", views.delete_event_task, name="delete_event_task"),
    path("calendar/", views.season_calendar, name="season_calendar"),
]