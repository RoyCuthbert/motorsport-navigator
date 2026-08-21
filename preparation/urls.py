from django.urls import path
from . import views

app_name = "preparation"

urlpatterns = [
    path("preparation/", views.preparation, name="preparation"),
    path("event/<int:event_id>/", views.preparation, name="event_preparation"),
    path("toggle/<int:item_id>/", views.toggle_check, name="toggle_check"),
    path("event/<int:event_id>/add-item/", views.add_preparation_item, name="add_preparation_item"),
    path("item/<int:item_id>/edit/", views.edit_preparation_item, name="edit_preparation_item"),
    path("item/<int:item_id>/delete/", views.delete_preparation_item, name="delete_preparation_item"),
]