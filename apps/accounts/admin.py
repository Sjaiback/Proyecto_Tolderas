from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "dni", "phone", "must_change_password", "created_at")
    list_filter = ("role", "must_change_password")
    search_fields = ("user__username", "user__first_name", "user__last_name", "dni", "phone")
