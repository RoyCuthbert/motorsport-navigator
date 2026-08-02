from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import Sum

from .forms import VehicleForm, RepairForm
from .models import Vehicle, Repair

# Create your views here.
@login_required
def garage(request):

    vehicles = Vehicle.objects.filter(
    owner=request.user
).order_by(
    "-is_default",
    "make",
    "model",
)

    default_vehicle = vehicles.filter(
        is_default=True
    ).first()

    outstanding_repairs = Repair.objects.filter(
        vehicle__owner=request.user,
        status="Outstanding"
    ).count()

    repair_cost = (
    Repair.objects.filter(
        vehicle__owner=request.user,
        status="Outstanding",
    ).aggregate(
        total=Sum("estimated_cost")
    )["total"] or 0
    )

    completed_repairs = Repair.objects.filter(
    vehicle__owner=request.user,
    status="Completed",
    ).count()

    if vehicles.exists():

        readiness = sum(
            vehicle.readiness_score
            for vehicle in vehicles
        ) / vehicles.count()

    else:

        readiness = 100

    ready_count = sum(
        1 for vehicle in vehicles
        if vehicle.competition_status == "READY TO COMPETE"
    )

    needs_attention = sum(
        1 for vehicle in vehicles
        if vehicle.competition_status == "NEEDS ATTENTION"
    )

    not_ready = sum(
        1 for vehicle in vehicles
        if vehicle.competition_status == "NOT READY"
    )

    mot_due = sum(
        1 for vehicle in vehicles
        if vehicle.mot_days_remaining is not None
        and 0 <= vehicle.mot_days_remaining <=30
    )

    return render(
        request,
        "garage/garage.html",
        {
            "vehicles": vehicles,
            "default_vehicle": default_vehicle,
            "outstanding_repairs": outstanding_repairs,
            "readiness": round(readiness),
            "repair_cost":repair_cost,
            "completed_repairs": completed_repairs,
            "ready_count": ready_count,
            "needs_attention": needs_attention,
            "not_ready": not_ready,
            "mot_due": mot_due,
        }
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
        "garage/add_vehicle.html",
        {
            "form": form,
        },
    )

@login_required
def vehicle_detail(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
        owner=request.user,
    )

    repairs = vehicle.repairs.all()

    context = {
        "vehicle": vehicle,
        "repairs": repairs,
    }

    return render(
        request,
        "garage/vehicle_detail.html",
        context,
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

    vehicles_affected = (
        repairs.values("vehicle").distinct().count()
    )

    critical_repairs = repairs.filter(
    priority="Critical",
    status="Outstanding"
    ).count()

    context = {
        "repairs": repairs,
        "outstanding_count": outstanding_count,
        "completed_count": completed_count,
        "total_cost": total_cost,
        "vehicles_affected": vehicles_affected,
        "critical_repairs": critical_repairs,
    }

    return render(
        request,
        "garage/repairs.html",
        context,
    )

@login_required
def add_repair(request):

    if request.method == "POST":

        form = RepairForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Repair added successfully."
            )

            return redirect("garage:repairs")

    else:

        form = RepairForm()

    return render(
        request,
        "garage/add_repair.html",
        {
            "form": form
        }
    )


@login_required
def edit_repair(request, repair_id):

    repair = get_object_or_404(
        Repair,
        pk=repair_id,
        vehicle__owner=request.user,
    )

    if request.method == "POST":

        form = RepairForm(
            request.POST,
            instance=repair,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Repair updated successfully."
            )

            return redirect("garage:repairs")

    else:

        form = RepairForm(instance=repair)

    return render(
        request,
        "garage/edit_repair.html",
        {
            "form": form,
            "repair": repair,
        },
    )

@login_required
def delete_repair(request, repair_id):

    repair = get_object_or_404(
        Repair,
        pk=repair_id,
        vehicle__owner=request.user,
    )

    if request.method == "POST":

        repair.delete()

        messages.success(
            request,
            "Repair deleted successfully."
        )

        return redirect("garage:repairs")

    return render(
        request,
        "garage/delete_repair.html",
        {
            "repair": repair,
        },
    )