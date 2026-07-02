from django.shortcuts import render

from apps.accounts.permissions import owner_required


@owner_required
def dashboard(request):
    return render(request, "analytics/dashboard.html")

# Create your views here.
