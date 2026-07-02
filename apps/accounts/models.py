from django.conf import settings
from django.db import models


def is_owner_user(user):
    return user.is_authenticated and user.username == getattr(settings, "OWNER_USERNAME", "75371089")


class UserProfile(models.Model):
    class Role(models.TextChoices):
        GENERAL_ADMIN = "admin_general", "Admin general"
        OPERATOR = "operador", "Gestion"
        CLIENT = "cliente", "Cliente"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    dni = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    must_change_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "perfil de usuario"
        verbose_name_plural = "perfiles de usuario"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
