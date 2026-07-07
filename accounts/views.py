from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import DriverProfile
from .forms import DriverProfileForm
# Create your views here.
@login_required
def profile(request):

    profile, created = DriverProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = DriverProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard")

    else:

        form = DriverProfileForm(
            instance=profile
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
        },
    )