from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .forms import VehicleForm
from .models import Vehicle, Repair

# Create your views here.
@login_required
def garage(request):

    vehicles = Vehicle.objects.filter(owner=request.user)

    repairs = Repair.objects.filter(
        vehicle__owner=request.user
    )

    context = {
        "vehicles": vehicles,
        "critical_repairs": repairs.filter(
            priority="Critical",
            status="Outstanding",
        ).count(),

        "major_repairs": repairs.filter(
            priority="Major",
            status="Outstanding",
        ).count(),

        "minor_repairs": repairs.filter(
            priority="Minor",
            status="Outstanding",
        ).count(),
    }

    return render(
        request,
        "garage/garage.html",
        context,
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

            return redirect("garage:garage")

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

            return redirect("garage:garage")

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

        return redirect("garage:garage")

    return render(
        request,
        "garage/vehicle_confirm_delete.html",
        {
            "vehicle": vehicle,
        },
    )

@login_required
def repairs(request):

    repairs = Repair.objects.filter(
        vehicle__owner=request.user
    ).order_by("status","-reported_on")

    outstanding_count = repairs.filter(
        status="Outstanding"
    ).count()

    completed_count = repairs.filter(
        status="Completed"
    ).count()

    total_cost = (
        repairs.filter(status="Outstanding")
        .aggregate(total=Sum("estimated_cost"))["total"]
        or 0
    )

    context = {
        "repairs": repairs,
        "outstanding_count": outstanding_count,
        "completed_count": completed_count,
        "total_cost": total_cost,
    }

    return render(
        request,
        "garage/repairs.html",
        context,
    )

@login_required
def add_repair(request):
    return HttpResponse("Add Repair page coming soon")


@login_required
def edit_repair(request, pk):
    return HttpResponse(f"Edit Repair {pk} coming soon")