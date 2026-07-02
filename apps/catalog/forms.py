from django import forms
from django.utils.text import slugify

from .models import Category, Product


class ProductForm(forms.ModelForm):
    category_name = forms.CharField(label="Categoria", initial="Catalogo")

    class Meta:
        model = Product
        fields = ("name", "category_name", "material", "description", "base_price", "price_label", "image", "is_active")
        labels = {
            "name": "Nombre del producto",
            "material": "Material",
            "description": "Descripcion del material / producto",
            "base_price": "Precio",
            "price_label": "Texto de precio visible",
            "image": "Foto",
            "is_active": "Visible en catalogo",
        }

    def save(self, commit=True):
        category_name = self.cleaned_data.pop("category_name")
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
        if commit:
            product.save()
            self.save_m2m()
        return product
