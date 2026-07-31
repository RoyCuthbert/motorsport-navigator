from django.urls import path

from . import views

app_name = "garage"

urlpatterns = [
    path("", views.garage, name="garage"),
    path("add/", views.add_vehicle, name="add_vehicle"),
    path("<int:vehicle_id>/", views.vehicle_detail, name="vehicle_detail"),
    path("<int:vehicle_id>/edit/", views.edit_vehicle, name="edit_vehicle"),
    path("<int:vehicle_id>/delete/", views.delete_vehicle, name="delete_vehicle"),
    path("repairs/", views.repairs, name="repairs"),
    path("repairs/add/", views.add_repair, name="add_repair"),
    path("repairs/<int:pk>/edit/", views.edit_repair, name="edit_repair"),
]