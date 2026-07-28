from django.urls import path

from . import views

urlpatterns = [
    path("", views.garage, name="garage"),
    path("add/", views.add_vehicle, name="add_vehicle"),
    path("<int:vehicle_id>/edit/", views.edit_vehicle, name="edit_vehicle"),
    path("<int:vehicle_id>/delete/", views.delete_vehicle, name="delete_vehicle"),
]