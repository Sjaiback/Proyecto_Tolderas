from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import Category, Product
from apps.operations.models import InventoryItem, InventoryMovement
from apps.orders.models import Customer, Order, OrderItem, Payment, Ticket

from .forms import LoginForm, ManagedUserEditForm, ManagedUserForm
from .models import UserProfile
from .permissions import owner_required, role_required


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        role = getattr(form.get_user(), "profile", None)
        if form.get_user().username == "75371089":
            return redirect("accounts:admin_dashboard")
        if role and role.role == UserProfile.Role.OPERATOR:
            return redirect("operations:dashboard")
        return redirect("public:home")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("public:home")


@owner_required
def admin_dashboard(request):
    return render(
        request,
        "accounts/admin_dashboard.html",
        {
            "users_count": User.objects.count(),
            "customers_count": Customer.objects.count(),
            "orders_count": Order.objects.count(),
            "products_count": Product.objects.count(),
        },
    )


@owner_required
def users_index(request):
    users = User.objects.select_related("profile").order_by("username")
    return render(request, "accounts/users_index.html", {"users": users})


@owner_required
def user_create(request):
    form = ManagedUserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "role": form.cleaned_data["role"],
                "dni": form.cleaned_data["dni"],
                "phone": form.cleaned_data["phone"],
            },
        )
        return redirect("accounts:users")
    return render(request, "accounts/user_form.html", {"form": form, "title": "Nuevo usuario"})


@owner_required
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    initial = {"role": profile.role, "dni": profile.dni, "phone": profile.phone}
    form = ManagedUserEditForm(request.POST or None, instance=user, initial=initial)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        profile.role = form.cleaned_data["role"]
        profile.dni = form.cleaned_data["dni"]
        profile.phone = form.cleaned_data["phone"]
        profile.save()
        return redirect("accounts:users")
    return render(request, "accounts/user_form.html", {"form": form, "title": "Editar usuario"})


@owner_required
def database_download(request):
    models = [User, UserProfile, Category, Product, Customer, Order, OrderItem, Payment, Ticket, InventoryItem, InventoryMovement]
    objects = []
    for model in models:
        objects.extend(model.objects.all())
    payload = serializers.serialize("json", objects, indent=2)
    response = HttpResponse(payload, content_type="application/json")
    response["Content-Disposition"] = 'attachment; filename="taller_toldera_bdd_export.json"'
    return response
