from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Event
from garage.models import Vehicle
# Create your views here.
@login_required
def events(request):

    events = Event.objects.filter(
        user=request.user
    )

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

    return render(
        request,
        "events/events.html",
        {
            "events": events,
            "upcoming": upcoming,
            "completed": completed,
            "cancelled": cancelled,
            "active_event": active_event,
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