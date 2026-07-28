from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VehicleForm
from .models import Vehicle

# Create your views here.
@login_required
def garage(request):

    vehicles = Vehicle.objects.filter(owner=request.user)

    return render(
        request,
        "garage/garage.html",
        {
            "vehicles": vehicles,
        },
    )


@login_required
def add_vehicle(request):

    if request.method == "POST":

        form = VehicleForm(request.POST, request.FILES)

        if form.is_valid():

            vehicle = form.save(commit=False)

            vehicle.owner = request.user

            vehicle.save()

            messages.success(request, "Vehicle added successfully.")

            return redirect("garage")

    else:

        form = VehicleForm()

    return render(
        request,
        "garage/vehicle_form.html",
        {
            "form": form,
            "title": "Add Vehicle",
        },
    )


@login_required
def edit_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
        owner=request.user,
    )

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle,
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Vehicle updated.")

            return redirect("garage")

    else:

        form = VehicleForm(instance=vehicle)

    return render(
        request,
        "garage/vehicle_form.html",
        {
            "form": form,
            "title": "Edit Vehicle",
        },
    )


@login_required
def delete_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
        owner=request.user,
    )

    if request.method == "POST":

        vehicle.delete()

        messages.success(request, "Vehicle deleted.")

        return redirect("garage")

    return render(
        request,
        "garage/vehicle_confirm_delete.html",
        {
            "vehicle": vehicle,
        },
    )