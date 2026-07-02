from django.contrib import admin

from .models import InventoryItem, InventoryMovement


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("product", "stock", "unit", "minimum_stock", "updated_at")
    search_fields = ("product__name",)


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "reason", "order", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__name", "reason", "order__tracking_code")

# Register your models here.
