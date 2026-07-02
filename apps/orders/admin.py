from django.contrib import admin

from .models import Customer, Order, OrderItem, Payment, Ticket


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "address", "created_at")
    search_fields = ("name", "phone", "address")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("tracking_code", "customer", "work_type", "status", "total", "advance", "balance", "received_at")
    list_filter = ("work_type", "status", "received_at")
    search_fields = ("tracking_code", "customer__name", "customer__phone", "description")
    inlines = [OrderItemInline, PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "method", "paid_at")
    list_filter = ("method", "paid_at")
    search_fields = ("order__tracking_code", "note")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("number", "order", "printed", "created_at")
    list_filter = ("printed", "created_at")
    search_fields = ("number", "order__tracking_code")

# Register your models here.
