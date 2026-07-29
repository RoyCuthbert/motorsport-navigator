from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from garage.models import Vehicle

# Create your views here.

@login_required
def dashboard(request):

    vehicle_count = Vehicle.objects.filter(
        owner=request.user
    ).count()

    context = {
        "vehicle_count": vehicle_count,
    }

    return render(
        request,
        "dashboard/dashboard.html",
    )