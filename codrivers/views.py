from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import DriverProfile

from .forms import CoDriverProfileForm

# Create your views here.
@login_required
def add_codriver(request):
    driver_profile = DriverProfile.objects.get(
        user=request.user,
    )

    if driver_profile.codrivers.count() >= 5:
        messages.warning(
            request,
            "You can have a maximum of 5 co-drivers"
        )

        return redirect("dashboard:dashboard")

    codriver_count = driver_profile.codrivers.count()
    remaining_slots = 5 - codriver_count

    if request.method == "POST":
        form = CoDriverProfileForm(request.POST)

        if form.is_valid():
            codriver = form.save(commit=False)
            codriver.driver = driver_profile
            codriver.save()
            return redirect("dashboard:dashboard")

    else:
        form = CoDriverProfileForm()

    context = {
        "form": form,
        "codriver_count": codriver_count,
        "remaining_slots": remaining_slots,
    }

    return render(
        request,
        "codrivers/add_codriver.html",
        context,
    )

@login_required
def codriver_list(request):
    driver_profile = DriverProfile.objects.get(
        user=request.user,
    )

    codrivers = driver_profile.codrivers.all().order_by(
        "first_name",
        "last_name",
    )

    context = {
        "codrivers": codrivers,
        "codriver_count": codrivers.count(),
        "remaining_slots": 5 - codrivers.count(),
    }

    return render(
        request,
        "codrivers/codriver_list.html",
        context,
    )

@login_required
def codriver_detail(request, pk):
    driver_profile = DriverProfile.objects.get(
        user=request.user,
    )

    codriver = get_object_or_404(
        driver_profile.codrivers.all(),
        pk=pk,
    )

    context = {
        "codriver": codriver,
    }

    return render(
        request,
        "codrivers/codriver_detail.html",
        context,
    )
@login_required
def edit_codriver(request, pk):
    driver_profile = DriverProfile.objects.get(
        user=request.user,
    )

    codriver = get_object_or_404(
        driver_profile.codrivers.all(),
        pk=pk,
    )

    if request.method == "POST":
        form = CoDriverProfileForm(
            request.POST,
            instance=codriver,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "codriver_detail",
                pk=codriver.pk,
            )

    else:
        form = CoDriverProfileForm(
            instance=codriver,
        )

    context = {
        "form": form,
        "codriver": codriver,
    }

    return render(
        request,
        "codrivers/edit_codriver.html",
        context,
    )

@login_required
@require_POST
def delete_codriver(request, pk):
    driver_profile = DriverProfile.objects.get(
        user=request.user,
    )

    codriver = get_object_or_404(
        driver_profile.codrivers.all(),
        pk=pk,
    )

    codriver.delete()

    messages.success(
        request,
        "Co-driver deleted successfully.",
    )

    return redirect("codriver_list")