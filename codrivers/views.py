from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import DriverProfile

from .forms import CoDriverProfileForm

# Create your views here.
@login_required
def add_codriver(request):
    driver_profile = DriverProfile.objects.get(
        user=request.user,
    )

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
    }

    return render(
        request,
        "codrivers/add_codriver.html",
        context,
    )