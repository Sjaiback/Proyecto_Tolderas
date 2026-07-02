from django.db import models


class DailyBusinessSnapshot(models.Model):
    date = models.DateField(unique=True)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active_orders = models.PositiveIntegerField(default=0)
    delivered_orders = models.PositiveIntegerField(default=0)
    average_ticket = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    top_category = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "snapshot diario"
        verbose_name_plural = "snapshots diarios"

    def __str__(self):
        return f"Resumen {self.date}"

# Create your models here.
