from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from apps.accounts.models import UserProfile
from apps.accounts.permissions import role_required
from apps.catalog.models import Product
from apps.catalog.forms import ProductForm
from apps.orders.models import Order
from apps.orders.forms import CustomerForm, OrderForm
from apps.orders.models import Customer, Ticket

from .models import InventoryItem


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def dashboard(request):
    return render(
        request,
        "operations/dashboard.html",
        {
            "active_count": Order.objects.exclude(status=Order.Status.DELIVERED).count(),
            "products_count": Product.objects.count(),
            "customers_count": Customer.objects.count(),
            "inventory_count": InventoryItem.objects.count(),
        },
    )


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def products_index(request):
    products = Product.objects.select_related("category").prefetch_related("images").order_by("name")
    return render(request, "operations/products_index.html", {"products": products})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Producto registrado correctamente.")
        return redirect("operations:products")
    return render(request, "operations/form_page.html", {"form": form, "title": "Registrar producto"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect("operations:products")
    return render(request, "operations/form_page.html", {"form": form, "title": "Editar producto"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado.")
        return redirect("operations:products")
    return render(request, "operations/confirm_delete.html", {"object": product, "title": "Eliminar producto"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def customers_index(request):
    customers = Customer.objects.order_by("name")
    return render(request, "operations/customers_index.html", {"customers": customers})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customer = form.save()
        customer.ensure_login_user()
        messages.success(request, "Cliente registrado y usuario creado con DNI.")
        return redirect("operations:customers")
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
def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == "POST" and form.is_valid():
        customer = form.save()
        customer.ensure_login_user()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect("operations:customers")
    return render(request, "operations/form_page.html", {"form": form, "title": "Editar cliente"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == "POST":
        user = customer.user
        customer.delete()
        if user:
            user.delete()
        messages.success(request, "Cliente eliminado.")
        return redirect("operations:customers")
    return render(request, "operations/confirm_delete.html", {"object": customer, "title": "Eliminar cliente"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def orders_index(request):
    orders = Order.objects.select_related("customer").order_by("-received_at")
    return render(request, "operations/orders_index.html", {"orders": orders})


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
def order_update(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    form = OrderForm(request.POST or None, instance=order)
    if request.method == "POST" and form.is_valid():
        form.save(user=request.user)
        messages.success(request, "Pedido actualizado correctamente.")
        return redirect("operations:orders")
    return render(request, "operations/form_page.html", {"form": form, "title": "Editar pedido"})


@role_required(UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR)
def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Pedido eliminado.")
        return redirect("operations:orders")
    return render(request, "operations/confirm_delete.html", {"object": order, "title": "Eliminar pedido"})


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
