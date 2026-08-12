from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date

from preparation.models import PreparationItem
from .models import Event
from garage.models import Vehicle
# Create your views here.
@login_required
def events(request):

    events = Event.objects.filter(
        user=request.user
    ).order_by("event_date")

    upcoming = events.filter(
        status="Upcoming"
    ).count()

    completed = events.filter(
        status="Completed"
    ).count()

    cancelled = events.filter(
        status="Cancelled"
    ).count()

    active_event = events.filter(
        selected=True
    ).first()

    upcoming_events = events.filter(
        event_date__gte=date.today()
    ).count()

    completed_events = events.filter(
        event_date__lt=date.today()
    ).count()

    total_events = events.count()

    # -----------------------------------------
    # PREPARATION PROGRESS FOR EACH EVENT
    # -----------------------------------------

    for event in events:

        preparation_checks = PreparationItem.objects.filter(
            user=request.user,
            event=event,
        )

        total_checks = preparation_checks.count()

        completed_checks = preparation_checks.filter(
            completed=True
        ).count()

        event.total_checks = total_checks
        event.completed_checks = completed_checks

        if total_checks:

            event.progress = round(
                (completed_checks / total_checks) * 100
            )

        else:

            event.progress = 0

        # Preparation status
        if total_checks == 0:

            event.preparation_status = "Not Started"
            event.preparation_status_class = "secondary"

        elif event.progress == 100:

            event.preparation_status = "Ready for Event"
            event.preparation_status_class = "success"

        elif event.progress >= 75:

            event.preparation_status = "Almost Ready"
            event.preparation_status_class = "warning"

        else:

            event.preparation_status = "Preparation Required"
            event.preparation_status_class = "danger"

    return render(
        request,
        "events/events.html",
        {
            "events": events,

            "upcoming": upcoming,
            "completed": completed,
            "cancelled": cancelled,

            "active_event": active_event,

            "upcoming_events": upcoming_events,
            "completed_events": completed_events,

            "total_events": total_events,
        },
    )

from .forms import EventForm

@login_required
def add_event(request):

    if request.method == "POST":

        form = EventForm(request.POST)

        form.fields["vehicle"].queryset = Vehicle.objects.filter(
            owner=request.user
        )

        if form.is_valid():

            event = form.save(commit=False)

            event.user = request.user

            event.save()

            return redirect("events:events")

    else:

        form = EventForm()

        form.fields["vehicle"].queryset = Vehicle.objects.filter(
            owner=request.user
        )

    return render(
        request,
        "events/add_event.html",
        {
            "form": form,
        },
    )

@login_required
def select_event(request, event_id):

    Event.objects.filter(
        user=request.user,
        selected=True,
    ).update(
        selected=False
    )

    event = get_object_or_404(
        Event,
        id=event_id,
        user=request.user,
    )

    event.selected = True
    event.save()

    next_page = request.GET.get("next")

    if next_page == "preparation":
        return redirect("preparation:preparation")

    return redirect("events:events")

@login_required
def edit_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id,
        user=request.user,
    )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            instance=event,
        )

        form.fields["vehicle"].queryset = Vehicle.objects.filter(
            owner=request.user
        )

        if form.is_valid():

            form.save()

            return redirect("events:events")

    else:

        form = EventForm(
            instance=event,
        )

        form.fields["vehicle"].queryset = Vehicle.objects.filter(
            owner=request.user
        )

    return render(
        request,
        "events/edit_event.html",
        {
            "form": form,
            "event": event,
        },
    )
@login_required
def delete_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id,
        user=request.user,
    )

    if request.method == "POST":

        event.delete()

        return redirect("events:events")

    return render(
        request,
        "events/delete_event.html",
        {
            "event": event,
        },
    )