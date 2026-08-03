from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


from .models import PreparationItem
from .checklist import create_default_checklist


from garage.models import Vehicle

# Create your views here.
@login_required
def preparation(request):

    default_vehicle = Vehicle.objects.filter(
        owner=request.user,
        is_default=True,
    ).first()

    vehicles = Vehicle.objects.filter(
        owner=request.user
    )

    if default_vehicle:
        create_default_checklist(
            request.user,
            default_vehicle,
        )

        vehicle_checks = PreparationItem.objects.filter(
            user=request.user,
            vehicle=default_vehicle,
            category="Vehicle",
        )

        safety_checks = PreparationItem.objects.filter(
            user=request.user,
            vehicle=default_vehicle,
            category="Safety",
        )

        document_checks = PreparationItem.objects.filter(
            user=request.user,
            vehicle=default_vehicle,
            category="Documents",
        )

        tool_checks = PreparationItem.objects.filter(
            user=request.user,
            vehicle=default_vehicle,
            category="Tools",
        )

    else:

        vehicle_checks = []
        safety_checks = []
        document_checks = []
        tool_checks = []

    return render(
        request,
        "preparation/preparation.html",
        {
            "default_vehicle": default_vehicle,
            "vehicles": vehicles,
            "vehicle_checks": vehicle_checks,
            "safety_checks": safety_checks,
            "document_checks": document_checks,
            "tool_checks": tool_checks,
        },
    )

@require_POST
@login_required
def toggle_check(request, item_id):

    item = get_object_or_404(
        PreparationItem,
        id=item_id,
        user=request.user,
    )

    item.completed = not item.completed
    item.save()

    section = request.POST.get("section", "vehicle-checks")

    url = reverse("preparation:preparation")
    return redirect(f"{url}#{section}")