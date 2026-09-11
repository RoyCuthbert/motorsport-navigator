from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

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
            codriver = form.save()
            codriver.drivers.add(driver_profile)

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