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
    )

    today = date.today()

    upcoming = events.filter(
        event_date__gt=today
    ).count()

    completed = events.filter(
        event_date__lt=today
    ).count()

    cancelled = 0

    upcoming_events = Event.objects.filter(
        user=request.user,
        event_date__gte=date.today(),
    ).count()

    completed_events = Event.objects.filter(
        user=request.user,
        event_date__lt=date.today(),
    ).count()

    active_event = Event.objects.filter(
        user=request.user,
        selected=True,
    ).first()

    total_events = Event.objects.filter(
        user=request.user,
    ).count()

    for event in events:

        if event.vehicle:

            total = PreparationItem.objects.filter(
                user=request.user,
                vehicle=event.vehicle,
            ).count()

            completed = PreparationItem.objects.filter(
                user=request.user,
                vehicle=event.vehicle,
                completed=True,
            ).count()

            if total:
                event.progress = round((completed / total) * 100)
            else:
                event.progress = 0

            event.completed_checks = completed
            event.total_checks = total

        else:

            event.progress = 0
            event.completed_checks = 0
            event.total_checks = 0

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
            "active_event": active_event,
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
    ).update(selected=False)

    event = get_object_or_404(
        Event,
        id=event_id,
        user=request.user,
    )

    event.selected = True
    event.save()

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