from django.contrib import admin

from .models import DailyBusinessSnapshot


@admin.register(DailyBusinessSnapshot)
class DailyBusinessSnapshotAdmin(admin.ModelAdmin):
    list_display = ("date", "total_sales", "active_orders", "delivered_orders", "average_ticket", "top_category")
    list_filter = ("date",)

# Register your models here.
