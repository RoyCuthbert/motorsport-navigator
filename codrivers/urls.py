from django.urls import path

from . import views


urlpatterns = [
    path("",views.codriver_list,name="codriver_list"),
    path("add/",views.add_codriver,name="add_codriver"),
    path("<int:pk>/",views.codriver_detail,name="codriver_detail"),
    path("<int:pk>/edit/", views.edit_codriver, name="edit_codriver"),
    
]