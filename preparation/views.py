from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


from .models import PreparationItem
from .checklist import create_default_checklist
from events.models import Event

from garage.models import Vehicle

# Create your views here.
@login_required
def preparation(request):

    # Get the currently selected event
    active_event = Event.objects.filter(
        user=request.user,
        selected=True,
    ).first()

    # All user's events for the event selector
    events = Event.objects.filter(
        user=request.user,
    ).order_by("event_date")

    # Default values
    current_vehicle = None

    vehicle_checks = []
    safety_checks = []
    document_checks = []
    tool_checks = []

    # If an event is selected and has a vehicle
    if active_event and active_event.vehicle:

        current_vehicle = active_event.vehicle

        # Create the checklist for THIS EVENT
        create_default_checklist(
            request.user,
            active_event,
        )

        vehicle_checks = PreparationItem.objects.filter(
            user=request.user,
            event=active_event,
            category="Vehicle",
        )

        safety_checks = PreparationItem.objects.filter(
            user=request.user,
            event=active_event,
            category="Safety",
        )

        document_checks = PreparationItem.objects.filter(
            user=request.user,
            event=active_event,
            category="Documents",
        )

        tool_checks = PreparationItem.objects.filter(
            user=request.user,
            event=active_event,
            category="Tools",
        )

    # Overall progress
    total_checks = PreparationItem.objects.filter(
        user=request.user,
        event=active_event,
    ).count()

    completed_checks = PreparationItem.objects.filter(
        user=request.user,
        event=active_event,
        completed=True,
    ).count()

    if total_checks:
        progress = round(
            (completed_checks / total_checks) * 100
        )
    else:
        progress = 0

    checks_remaining = total_checks - completed_checks

    # Section totals
    vehicle_total = vehicle_checks.count()
    vehicle_completed = vehicle_checks.filter(
        completed=True
    ).count()

    safety_total = safety_checks.count()
    safety_completed = safety_checks.filter(
        completed=True
    ).count()

    document_total = document_checks.count()
    document_completed = document_checks.filter(
        completed=True
    ).count()

    tool_total = tool_checks.count()
    tool_completed = tool_checks.filter(
        completed=True
    ).count()

    # Section progress
    vehicle_progress = (
        round(vehicle_completed / vehicle_total * 100)
        if vehicle_total else 0
    )

    safety_progress = (
        round(safety_completed / safety_total * 100)
        if safety_total else 0
    )

    document_progress = (
        round(document_completed / document_total * 100)
        if document_total else 0
    )

    tool_progress = (
        round(tool_completed / tool_total * 100)
        if tool_total else 0
    )

    return render(
        request,
        "preparation/preparation.html",
        {
            "active_event": active_event,
            "events":events,
            "current_vehicle": current_vehicle,

            "vehicle_checks": vehicle_checks,
            "safety_checks": safety_checks,
            "document_checks": document_checks,
            "tool_checks": tool_checks,

            "progress": progress,
            "completed_checks": completed_checks,
            "total_checks": total_checks,
            "checks_remaining": checks_remaining,

            "vehicle_total": vehicle_total,
            "vehicle_completed": vehicle_completed,
            "vehicle_progress": vehicle_progress,

            "safety_total": safety_total,
            "safety_completed": safety_completed,
            "safety_progress": safety_progress,

            "document_total": document_total,
            "document_completed": document_completed,
            "document_progress": document_progress,

            "tool_total": tool_total,
            "tool_completed": tool_completed,
            "tool_progress": tool_progress,
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