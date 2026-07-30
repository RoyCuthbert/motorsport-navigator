from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from garage.models import Vehicle

# Create your views here.
@login_required
def preparation(request):

    vehicles = Vehicle.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "preparation/preparation.html",
        {
            "vehicles": vehicles,
        },
    )
