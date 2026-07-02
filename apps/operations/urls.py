from django.urls import path

from . import views

app_name = "operations"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("productos/", views.products_index, name="products"),
    path("productos/nuevo/", views.product_create, name="product_create"),
    path("productos/<int:product_id>/editar/", views.product_update, name="product_update"),
    path("productos/<int:product_id>/eliminar/", views.product_delete, name="product_delete"),
    path("clientes/", views.customers_index, name="customers"),
    path("clientes/nuevo/", views.customer_create, name="customer_create"),
    path("clientes/<int:customer_id>/editar/", views.customer_update, name="customer_update"),
    path("clientes/<int:customer_id>/eliminar/", views.customer_delete, name="customer_delete"),
    path("pedidos/", views.orders_index, name="orders"),
    path("pedidos/nuevo/", views.order_create, name="order_create"),
    path("pedidos/<int:order_id>/editar/", views.order_update, name="order_update"),
    path("pedidos/<int:order_id>/eliminar/", views.order_delete, name="order_delete"),
    path("tickets/<int:order_id>/", views.ticket_print, name="ticket"),
]
