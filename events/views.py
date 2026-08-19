from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import calendar
from collections import defaultdict
from datetime import date

from preparation.models import PreparationItem
from .models import Event, EventTask, EVENT_TYPES 
from garage.models import Vehicle
from .forms import EventForm, EventTaskForm
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

@login_required
def event_detail(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id,
        user=request.user,
    )

    preparation_checks = PreparationItem.objects.filter(
        user=request.user,
        event=event,
    )

    total_checks = preparation_checks.count()

    completed_checks = preparation_checks.filter(
        completed=True
    ).count()

    if total_checks:
        preparation_progress = round(
            (completed_checks / total_checks) * 100
        )
    else:
        preparation_progress = 0

    checks_remaining = total_checks - completed_checks

    # Preparation status
    if total_checks == 0:

        preparation_status = "Not Started"
        preparation_status_class = "secondary"

    elif preparation_progress == 100:

        preparation_status = "Ready for Event"
        preparation_status_class = "success"

    elif preparation_progress >= 75:

        preparation_status = "Almost Ready"
        preparation_status_class = "warning"

    else:

        preparation_status = "Preparation Required"
        preparation_status_class = "danger"

    # -----------------------------------------
    # EVENT TASKS
    # -----------------------------------------

    event_tasks = event.tasks.filter(
        user=request.user,
    )

    total_tasks = event_tasks.count()

    completed_tasks = event_tasks.filter(
        completed=True,
    ).count()

    if total_tasks:
        task_progress = round(
            (completed_tasks / total_tasks) * 100
    )
    else:
        task_progress = 0

    tasks_remaining = total_tasks - completed_tasks

    # Individual checklist sections
    vehicle_checks = preparation_checks.filter(
        category="Vehicle"
    )

    safety_checks = preparation_checks.filter(
        category="Safety"
    )

    document_checks = preparation_checks.filter(
        category="Documents"
    )

    tool_checks = preparation_checks.filter(
        category="Tools"
    )
    # -----------------------------------------
    # DAYS UNTIL EVENT
    # -----------------------------------------

    days_remaining = (
        event.event_date - date.today()
    ).days

    # ==========================================
    # EVENT TASK SUMMARY
    # ==========================================

    event_tasks = EventTask.objects.filter(
        event=event,
        user=request.user,
    )

    total_tasks = event_tasks.count()

    completed_tasks = event_tasks.filter(
        completed=True
    ).count()

    high_priority_tasks = event_tasks.filter(
        priority="High",
        completed=False,
    ).count()

    overdue_tasks = 0
    due_today_tasks = 0
    due_soon_tasks = 0
    upcoming_tasks = 0
    no_deadline_tasks = 0

    for task in event_tasks:

        if task.due_status == "Overdue":
            overdue_tasks += 1

        elif task.due_status == "Due Today":
            due_today_tasks += 1

        elif task.due_status == "Due Soon":
            due_soon_tasks += 1

        elif task.due_status == "Upcoming":
            upcoming_tasks += 1

        elif task.due_status == "No Deadline":
            no_deadline_tasks += 1

    tasks_remaining = total_tasks - completed_tasks

    if total_tasks:
        task_progress = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        task_progress = 0

    # -----------------------------------------
    # TASK FILTER (from Task Attention boxes)
    # -----------------------------------------

    task_filter = request.GET.get("task_filter")

    task_filter_map = {
        "overdue": "Overdue",
        "due_today": "Due Today",
        "due_soon": "Due Soon",
        "upcoming": "Upcoming",
        "no_deadline": "No Deadline",
        "completed": "Completed",
    }

    if task_filter in task_filter_map:

        due_status_label = task_filter_map[task_filter]

        event_tasks = [
            task
            for task in event_tasks
            if task.due_status == due_status_label
        ]


    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,

            "total_checks": total_checks,
            "completed_checks": completed_checks,
            "checks_remaining": checks_remaining,

            "preparation_progress": preparation_progress,

            "preparation_status": preparation_status,
            "preparation_status_class": preparation_status_class,

            "event_tasks": event_tasks,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "task_progress": task_progress,
            "tasks_remaining": tasks_remaining,
            "task_filter": task_filter,

            "overdue_tasks": overdue_tasks,
            "due_today_tasks": due_today_tasks,
            "due_soon_tasks": due_soon_tasks,
            "upcoming_tasks": upcoming_tasks,
            "no_deadline_tasks": no_deadline_tasks,
            "high_priority_tasks": high_priority_tasks,
            
            "days_remaining":days_remaining,

            "vehicle_checks": vehicle_checks,
            "safety_checks": safety_checks,
            "document_checks": document_checks,
            "tool_checks": tool_checks,
        },
    )

@login_required
def add_event_task(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id,
        user=request.user,
    )

    if request.method == "POST":

        form = EventTaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.event = event
            task.user = request.user

            task.save()

            return redirect(
                f"{reverse('events:event_detail', args=[event.id])}#event-tasks"
            )

    else:

        form = EventTaskForm()

    return render(
        request,
        "events/add_event_task.html",
        {
            "event": event,
            "form": form,
        },
    )

@login_required
def edit_event_task(request, task_id):
    task = get_object_or_404(
        EventTask,
        id=task_id,
        user=request.user,
    )

    if request.method == "POST":
        form = EventTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()

            return redirect(
                f"{reverse('events:event_detail', args=[task.event.id])}#event-tasks"
            )

    else:
        form = EventTaskForm(instance=task)

    context = {
        "form": form,
        "task": task,
        "event": task.event,
    }

    return render(
        request,
        "events/edit_event_task.html",
        context,
    )

@login_required
def toggle_event_task(request, task_id):

    task = get_object_or_404(
        EventTask,
        id=task_id,
        user=request.user,
    )

    task.completed = not task.completed

    task.save()

    return redirect(
        "events:event_detail",
        event_id=task.event.id,
    )

@login_required
def delete_event_task(request, task_id):

    task = get_object_or_404(
        EventTask,
        id=task_id,
        user=request.user,
    )

    event_id = task.event.id

    if request.method == "POST":

        task.delete()

        return redirect(
            "events:event_detail",
            event_id=event_id,
        )

    return render(
        request,
        "events/delete_event_task.html",
        {
            "task": task,
        },
    )

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

@login_required
def season_dashboard(request):

    today = date.today()

    # -----------------------------------------
    # USER'S VEHICLES
    # -----------------------------------------

    vehicles = Vehicle.objects.filter(
        owner=request.user
    ).order_by(
        "-is_default",
        "nickname",
    )

    # -----------------------------------------
    # VEHICLE FILTER
    # -----------------------------------------

    vehicle_id = request.GET.get("vehicle")

    events = Event.objects.filter(
        user=request.user
    ).select_related(
        "vehicle"
    ).order_by(
        "event_date"
    )

    if vehicle_id:

        # Make sure the selected vehicle belongs
        # to the current user.

        selected_vehicle = vehicles.filter(
            id=vehicle_id
        ).first()

        if selected_vehicle:

            events = events.filter(
                vehicle=selected_vehicle
            )

        else:

            vehicle_id = None

    # -----------------------------------------
    # EVENT STATISTICS
    # -----------------------------------------

    total_events = events.count()

    upcoming_count = events.filter(
        event_date__gte=today
    ).count()

    completed_count = events.filter(
        status="Completed"
    ).count()

    cancelled_count = events.filter(
        status="Cancelled"
    ).count()

    # -----------------------------------------
    # NEXT EVENT
    # -----------------------------------------

    next_event = events.filter(
        event_date__gte=today
    ).exclude(
        status="Cancelled"
    ).order_by(
        "event_date"
    ).first()

    # -----------------------------------------
    # SEASON TOTALS
    # -----------------------------------------

    total_preparation = 0
    completed_preparation = 0

    total_tasks = 0
    completed_tasks = 0

    # -----------------------------------------
    # EVENT INFORMATION
    # -----------------------------------------

    for event in events:

        # =====================================
        # PREPARATION
        # =====================================

        preparation_checks = PreparationItem.objects.filter(
            user=request.user,
            event=event,
        )

        event.total_checks = preparation_checks.count()

        event.completed_checks = preparation_checks.filter(
            completed=True
        ).count()

        if event.total_checks:

            event.preparation_progress = round(
                (
                    event.completed_checks
                    / event.total_checks
                ) * 100
            )

        else:

            event.preparation_progress = 0

        # =====================================
        # EVENT TASKS
        # =====================================

        event.total_tasks = EventTask.objects.filter(
            user=request.user,
            event=event,
        ).count()

        event.completed_tasks = EventTask.objects.filter(
            user=request.user,
            event=event,
            completed=True,
        ).count()

        if event.total_tasks:

            event.task_progress = round(
                (
                    event.completed_tasks
                    / event.total_tasks
                ) * 100
            )

        else:

            event.task_progress = 0

        # =====================================
        # OVERALL READINESS
        # =====================================

        if (
            event.preparation_progress == 100
            and event.task_progress == 100
        ):

            event.readiness = "Ready"
            event.readiness_class = "success"

        elif (
            event.preparation_progress >= 75
            and event.task_progress >= 75
        ):

            event.readiness = "Almost Ready"
            event.readiness_class = "warning"

        elif (
            event.total_checks == 0
            and event.total_tasks == 0
        ):

            event.readiness = "Not Started"
            event.readiness_class = "secondary"

        else:

            event.readiness = "Needs Attention"
            event.readiness_class = "danger"

        # =====================================
        # SEASON TOTALS
        # =====================================

        total_preparation += event.total_checks
        completed_preparation += event.completed_checks

        total_tasks += event.total_tasks
        completed_tasks += event.completed_tasks

    # -----------------------------------------
    # OVERALL PREPARATION PROGRESS
    # -----------------------------------------

    if total_preparation:

        preparation_progress = round(
            (
                completed_preparation
                / total_preparation
            ) * 100
        )

    else:

        preparation_progress = 0

    # -----------------------------------------
    # OVERALL TASK PROGRESS
    # -----------------------------------------

    if total_tasks:

        task_progress = round(
            (
                completed_tasks
                / total_tasks
            ) * 100
        )

    else:

        task_progress = 0

    # -----------------------------------------
    # NEXT EVENT DETAILS
    # -----------------------------------------

    if next_event:

        next_event_days = (
            next_event.event_date - today
        ).days

        next_event.total_checks = (
            PreparationItem.objects.filter(
                user=request.user,
                event=next_event,
            ).count()
        )

        next_event.completed_checks = (
            PreparationItem.objects.filter(
                user=request.user,
                event=next_event,
                completed=True,
            ).count()
        )

        if next_event.total_checks:

            next_event.preparation_progress = round(
                (
                    next_event.completed_checks
                    / next_event.total_checks
                ) * 100
            )

        else:

            next_event.preparation_progress = 0

        next_event.total_tasks = EventTask.objects.filter(
            user=request.user,
            event=next_event,
        ).count()

        next_event.completed_tasks = EventTask.objects.filter(
            user=request.user,
            event=next_event,
            completed=True,
        ).count()

        if next_event.total_tasks:

            next_event.task_progress = round(
                (
                    next_event.completed_tasks
                    / next_event.total_tasks
                ) * 100
            )

        else:

            next_event.task_progress = 0

    else:

        next_event_days = None

    return render(
        request,
        "events/season_dashboard.html",
        {
            "events": events,
            "vehicles": vehicles,

            "selected_vehicle": vehicle_id,

            "total_events": total_events,
            "upcoming_count": upcoming_count,
            "completed_count": completed_count,
            "cancelled_count": cancelled_count,

            "total_preparation": total_preparation,
            "completed_preparation": completed_preparation,
            "preparation_progress": preparation_progress,

            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "task_progress": task_progress,

            "next_event": next_event,
            "next_event_days": next_event_days,
        },
    )

@login_required
def season_calendar(request):

    today = date.today()

    # -----------------------------------------
    # SELECT MONTH
    # -----------------------------------------

    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
    except (TypeError, ValueError):
        year = today.year
        month = today.month

    if month < 1:
        month = 12
        year -= 1

    elif month > 12:
        month = 1
        year += 1


    # -----------------------------------------
    # FILTER VALUES
    # -----------------------------------------

    status_filter = request.GET.get("status", "").strip()
    event_type_filter = request.GET.get("event_type", "").strip()
    vehicle_id = request.GET.get("vehicle", "").strip()


    # -----------------------------------------
    # VEHICLES
    # -----------------------------------------

    vehicles = Vehicle.objects.filter(
        owner=request.user
    ).order_by("nickname")


    selected_vehicle = None

    if vehicle_id:

        try:

            selected_vehicle = vehicles.get(
                id=vehicle_id
            )

        except Vehicle.DoesNotExist:

            selected_vehicle = None


    # -----------------------------------------
    # EVENTS FOR MONTH
    # -----------------------------------------

    events = Event.objects.filter(
        user=request.user,
        event_date__year=year,
        event_date__month=month,
    ).select_related(
        "vehicle",
    ).order_by(
        "event_date",
    )


    # -----------------------------------------
    # APPLY STATUS FILTER
    # -----------------------------------------

    if status_filter in {
        "Upcoming",
        "Completed",
        "Cancelled",
    }:

        events = events.filter(
            status=status_filter
        )

    else:

        status_filter = ""


    # -----------------------------------------
    # APPLY RALLY TYPE FILTER
    # -----------------------------------------

    valid_event_types = {
        value
        for value, label in EVENT_TYPES
    }


    if event_type_filter in valid_event_types:

        events = events.filter(
            event_type=event_type_filter
        )

    else:

        event_type_filter = ""


    # -----------------------------------------
    # APPLY VEHICLE FILTER
    # -----------------------------------------

    if selected_vehicle:

        events = events.filter(
            vehicle=selected_vehicle
        )


    # -----------------------------------------
    # GROUP EVENTS BY DATE
    # -----------------------------------------

    events_by_date = defaultdict(list)

    for event in events:

        events_by_date[
            event.event_date
        ].append(event)


    # -----------------------------------------
    # PREPARATION PROGRESS
    # -----------------------------------------

    for event in events:

        preparation_checks = PreparationItem.objects.filter(
            user=request.user,
            event=event,
        )

        total_checks = preparation_checks.count()

        completed_checks = preparation_checks.filter(
            completed=True,
        ).count()

        event.total_checks = total_checks
        event.completed_checks = completed_checks

        if total_checks:

            event.progress = round(
                (completed_checks / total_checks) * 100
            )

        else:

            event.progress = 0


    # -----------------------------------------
    # CALENDAR
    # -----------------------------------------

    calendar_obj = calendar.Calendar(
        firstweekday=0
    )

    weeks = calendar_obj.monthdatescalendar(
        year,
        month,
    )


    # -----------------------------------------
    # PREVIOUS MONTH
    # -----------------------------------------

    if month == 1:

        previous_month = 12
        previous_year = year - 1

    else:

        previous_month = month - 1
        previous_year = year


    # -----------------------------------------
    # NEXT MONTH
    # -----------------------------------------

    if month == 12:

        next_month = 1
        next_year = year + 1

    else:

        next_month = month + 1
        next_year = year


    # -----------------------------------------
    # MONTH NAME
    # -----------------------------------------

    month_name = calendar.month_name[
        month
    ]


    # -----------------------------------------
    # RENDER
    # -----------------------------------------

    return render(
        request,
        "events/season_calendar.html",
        {
            "weeks": weeks,
            "events_by_date": events_by_date,

            "calendar_year": year,
            "calendar_month": month,
            "month_name": month_name,

            "previous_year": previous_year,
            "previous_month": previous_month,

            "next_year": next_year,
            "next_month": next_month,

            "today": today,

            # Filters
            "vehicles": vehicles,
            "selected_vehicle": selected_vehicle,
            "vehicle_id": vehicle_id,

            "event_types": EVENT_TYPES,
            "event_type_filter": event_type_filter,

            "status_filter": status_filter,
        },
    )