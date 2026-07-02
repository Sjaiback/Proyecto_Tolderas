from django.shortcuts import redirect, render, get_object_or_404

from apps.accounts.models import UserProfile
from apps.accounts.permissions import role_required
from apps.catalog.forms import ProductForm
from apps.orders.models import Order
from apps.orders.forms import CustomerForm, OrderForm
from apps.orders.models import Customer, Ticket

from .models import InventoryItem


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def dashboard(request):
    db_orders = Order.objects.exclude(status=Order.Status.DELIVERED).select_related("customer")[:8]
    orders = [
        {"code": item.tracking_code, "title": item.description, "status": item.get_status_display()}
        for item in db_orders
    ]
    if not orders:
        orders = [
            {"code": "ER-2407", "title": "Toldera reforzada", "status": "Listo"},
            {"code": "ER-2408", "title": "Reparacion lona roja", "status": "En proceso"},
            {"code": "ER-2409", "title": "Carpa comercial", "status": "Recibido"},
            {"code": "ER-2410", "title": "Confeccion especial", "status": "En proceso"},
        ]

    db_inventory = InventoryItem.objects.select_related("product")[:8]
    inventory = [
        {
            "name": item.product.name,
            "value": min(100, int(item.stock)),
            "stock": f"{item.stock} {item.unit}",
        }
        for item in db_inventory
    ]
    if not inventory:
        inventory = [
            {"name": "Lona azul", "value": 72, "stock": "72 m"},
            {"name": "Hilo reforzado", "value": 35, "stock": "35 und"},
            {"name": "Tubos estructura", "value": 18, "stock": "Bajo"},
        ]
    return render(
        request,
        "operations/dashboard.html",
        {"orders": orders, "inventory": inventory, "active_count": len(orders)},
    )


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("operations:dashboard")
    return render(request, "operations/form_page.html", {"form": form, "title": "Registrar producto"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customer = form.save()
        customer.ensure_login_user()
        return redirect("operations:dashboard")
    return render(
        request,
        "operations/form_page.html",
        {
            "form": form,
            "title": "Registrar cliente",
            "hint": "El usuario del cliente sera su DNI y su contraseña inicial tambien sera su DNI.",
        },
    )


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def order_create(request):
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(user=request.user)
        Ticket.objects.get_or_create(
            order=order,
            defaults={
                "number": f"T-{order.tracking_code}",
                "content": f"Pedido {order.tracking_code} - {order.customer.name} - {order.description}",
            },
        )
        return redirect("operations:ticket", order_id=order.id)
    return render(request, "operations/form_page.html", {"form": form, "title": "Registrar pedido"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def ticket_print(request, order_id):
    order = get_object_or_404(Order.objects.select_related("customer"), pk=order_id)
    ticket, _ = Ticket.objects.get_or_create(
        order=order,
        defaults={
            "number": f"T-{order.tracking_code}",
            "content": f"Pedido {order.tracking_code} - {order.customer.name} - {order.description}",
        },
    )
    return render(request, "operations/ticket_print.html", {"order": order, "ticket": ticket})

# Create your views here.
