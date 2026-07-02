from django import forms

from apps.catalog.models import Product

from .models import Customer, Order, OrderItem, Payment


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("dni", "name", "phone", "address", "notes")
        labels = {
            "dni": "DNI",
            "name": "Nombre completo",
            "phone": "Telefono",
            "address": "Direccion",
            "notes": "Notas",
        }


class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(label="Producto", queryset=Product.objects.filter(is_active=True), required=False)
    item_description = forms.CharField(label="Detalle del trabajo")
    quantity = forms.DecimalField(label="Cantidad", initial=1, min_value=1)
    unit_price = forms.DecimalField(label="Precio unitario", min_value=0)
    payment_amount = forms.DecimalField(label="Monto recibido / adelanto", min_value=0, initial=0)
    payment_method = forms.ChoiceField(label="Metodo de pago", choices=Payment.Method.choices)

    class Meta:
        model = Order
        fields = ("customer", "work_type", "description", "status", "total", "advance", "estimated_delivery", "notes")
        labels = {
            "customer": "Cliente",
            "work_type": "Tipo de trabajo",
            "description": "Descripcion general",
            "status": "Estado",
            "total": "Total",
            "advance": "Adelanto",
            "estimated_delivery": "Entrega estimada",
            "notes": "Notas",
        }
        widgets = {"estimated_delivery": forms.DateInput(attrs={"type": "date"})}

    def save(self, user=None, commit=True):
        order = super().save(commit=False)
        if user and user.is_authenticated:
            order.received_by = user
        if commit:
            is_new = order.pk is None
            order.save()
            product = self.cleaned_data.get("product")
            if is_new:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    description=self.cleaned_data["item_description"],
                    quantity=self.cleaned_data["quantity"],
                    unit_price=self.cleaned_data["unit_price"],
                    subtotal=self.cleaned_data["quantity"] * self.cleaned_data["unit_price"],
                )
            else:
                item = order.items.first()
                if item:
                    item.product = product
                    item.description = self.cleaned_data["item_description"]
                    item.quantity = self.cleaned_data["quantity"]
                    item.unit_price = self.cleaned_data["unit_price"]
                    item.subtotal = self.cleaned_data["quantity"] * self.cleaned_data["unit_price"]
                    item.save()
            amount = self.cleaned_data["payment_amount"]
            if is_new and amount > 0:
                Payment.objects.create(
                    order=order,
                    amount=amount,
                    method=self.cleaned_data["payment_method"],
                    note="Pago registrado al crear pedido",
                )
        return order
