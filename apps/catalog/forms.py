from datetime import timedelta

from django import forms
from django.utils import timezone
from django.utils.text import slugify

from .models import Category, Product, ProductImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data]
        return [single_file_clean(data, initial)] if data else []


class ProductForm(forms.ModelForm):
    category_name = forms.CharField(label="Categoria", initial="Catalogo")
    discount_days = forms.IntegerField(
        label="Dias de descuento",
        min_value=1,
        required=False,
        help_text="Solo aplica si el precio baja y eliges descuento por tiempo limitado.",
    )
    gallery_images = MultipleFileField(label="Fotos adicionales", required=False)

    class Meta:
        model = Product
        fields = (
            "name",
            "category_name",
            "material",
            "description",
            "base_price",
            "previous_price",
            "discount_mode",
            "discount_days",
            "price_label",
            "image",
            "gallery_images",
            "is_active",
        )
        labels = {
            "name": "Nombre del producto",
            "material": "Material",
            "description": "Descripcion del material / producto",
            "base_price": "Precio actual S/.",
            "previous_price": "Precio anterior S/.",
            "discount_mode": "Si bajo el precio, sera",
            "price_label": "Texto de precio visible",
            "image": "Foto principal",
            "is_active": "Visible en catalogo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gallery_images"].widget.attrs.update({"multiple": True})

    def clean(self):
        cleaned = super().clean()
        previous_price = cleaned.get("previous_price")
        base_price = cleaned.get("base_price")
        discount_mode = cleaned.get("discount_mode")
        discount_days = cleaned.get("discount_days")
        if previous_price and base_price and base_price < previous_price:
            if discount_mode == Product.DiscountMode.NONE:
                self.add_error("discount_mode", "Si el precio baja, indica si es temporal o definitivo.")
            if discount_mode == Product.DiscountMode.TEMPORARY and not discount_days:
                self.add_error("discount_days", "Indica cuantos dias durara el descuento.")
        return cleaned

    def save(self, commit=True):
        category_name = self.cleaned_data.pop("category_name")
        discount_days = self.cleaned_data.pop("discount_days", None)
        gallery_images = self.cleaned_data.pop("gallery_images", [])
        category, _ = Category.objects.get_or_create(
            slug=slugify(category_name),
            defaults={"name": category_name},
        )
        product = super().save(commit=False)
        product.category = category
        if not product.slug:
            base_slug = slugify(product.name)
            slug = base_slug
            counter = 2
            while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = slug
        if product.discount_mode == Product.DiscountMode.TEMPORARY and discount_days:
            product.discount_ends_at = timezone.localdate() + timedelta(days=discount_days)
        elif product.discount_mode != Product.DiscountMode.TEMPORARY:
            product.discount_ends_at = None
        if not product.price_label:
            product.price_label = product.display_price
        if commit:
            product.save()
            self.save_m2m()
            for image in gallery_images:
                ProductImage.objects.create(product=product, image=image)
        return product
