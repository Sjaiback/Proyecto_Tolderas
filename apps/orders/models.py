from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string

from apps.catalog.models import Product


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer")
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=240, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def ensure_login_user(self):
        from apps.accounts.models import UserProfile

        if self.user_id:
            return self.user
        user, created = User.objects.get_or_create(
            username=self.dni,
            defaults={
                "first_name": self.name,
                "is_staff": False,
                "is_superuser": False,
            },
        )
        if created:
            user.set_password(self.dni)
            user.save()
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "role": UserProfile.Role.CLIENT,
                "dni": self.dni,
                "phone": self.phone,
                "must_change_password": True,
            },
        )
        self.user = user
        self.save(update_fields=["user"])
        return user


class Order(models.Model):
    class WorkType(models.TextChoices):
        SALE = "venta", "Venta"
        REPAIR = "reparacion", "Reparacion"
        CUSTOM = "confeccion", "Confeccion"
        INSTALL = "instalacion", "Instalacion"

    class Status(models.TextChoices):
        RECEIVED = "recibido", "Recibido"
        IN_PROGRESS = "en_proceso", "En proceso"
        READY = "listo", "Listo"
        DELIVERED = "entregado", "Entregado"
        CANCELLED = "cancelado", "Cancelado"

    tracking_code = models.CharField(max_length=30, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    work_type = models.CharField(max_length=20, choices=WorkType.choices)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_orders",
    )
    received_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-received_at"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return f"{self.tracking_code} - {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            while True:
                code = f"ER-{get_random_string(6, allowed_chars='0123456789')}"
                if not Order.objects.filter(tracking_code=code).exists():
                    self.tracking_code = code
                    break
        self.balance = self.total - self.advance
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True)
    description = models.CharField(max_length=220)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "item de pedido"
        verbose_name_plural = "items de pedido"

    def __str__(self):
        return self.description


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "efectivo", "Efectivo"
        YAPE = "yape", "Yape"
        TRANSFER = "transferencia", "Transferencia"
        OTHER = "otro", "Otro"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH)
    paid_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=220, blank=True)

    class Meta:
        ordering = ["-paid_at"]
        verbose_name = "pago"
        verbose_name_plural = "pagos"

    def __str__(self):
        return f"{self.order.tracking_code} - S/ {self.amount}"


class Ticket(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="ticket")
    number = models.CharField(max_length=40, unique=True)
    content = models.TextField()
    printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ticket"
        verbose_name_plural = "tickets"

    def __str__(self):
        return self.number

# Create your models here.
