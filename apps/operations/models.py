from django.db import models

from apps.catalog.models import Product
from apps.orders.models import Order


class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=30, default="und")
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "inventario"
        verbose_name_plural = "inventario"

    def __str__(self):
        return f"{self.product.name}: {self.stock} {self.unit}"


class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "entrada", "Entrada"
        OUT = "salida", "Salida"
        ADJUST = "ajuste", "Ajuste"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="inventory_movements")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=220)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="inventory_movements")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "movimiento de inventario"
        verbose_name_plural = "movimientos de inventario"

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.product.name}"

# Create your models here.
