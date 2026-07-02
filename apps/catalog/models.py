from decimal import Decimal

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name


class Product(models.Model):
    class DiscountMode(models.TextChoices):
        NONE = "none", "Sin descuento"
        TEMPORARY = "temporary", "Por tiempo limitado"
        DEFINITIVE = "definitive", "Definitivo"

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    material = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_label = models.CharField(max_length=80, blank=True)
    discount_mode = models.CharField(max_length=20, choices=DiscountMode.choices, default=DiscountMode.NONE)
    discount_ends_at = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.name

    @property
    def display_price(self):
        return f"S/. {Decimal(self.base_price):.2f}"

    @property
    def has_discount(self):
        return bool(self.previous_price and Decimal(self.previous_price) > Decimal(self.base_price))

    @property
    def discount_percent(self):
        if not self.has_discount or not self.previous_price:
            return 0
        previous_price = Decimal(self.previous_price)
        base_price = Decimal(self.base_price)
        discount = (previous_price - base_price) / previous_price * Decimal("100")
        return int(discount.quantize(Decimal("1")))

    @property
    def main_image_url(self):
        if self.image:
            return self.image.url
        first_gallery_image = self.images.first()
        if first_gallery_image:
            return first_gallery_image.image.url
        return ""


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/")
    caption = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "imagen de producto"
        verbose_name_plural = "imagenes de producto"

    def __str__(self):
        return f"Imagen {self.product.name}"

# Create your models here.
