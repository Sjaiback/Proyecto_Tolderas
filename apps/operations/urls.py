from django.urls import path

from . import views

app_name = "operations"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("productos/nuevo/", views.product_create, name="product_create"),
    path("clientes/nuevo/", views.customer_create, name="customer_create"),
    path("pedidos/nuevo/", views.order_create, name="order_create"),
    path("tickets/<int:order_id>/", views.ticket_print, name="ticket"),
]
