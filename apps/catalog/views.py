from urllib.parse import quote

from django.shortcuts import render
from django.templatetags.static import static

from .models import Product


def catalog_index(request):
    db_products = Product.objects.filter(is_active=True).select_related("category")
    if db_products.exists():
        products = []
        for product in db_products:
            image = product.image.url if product.image else static("img/producto-1.webp")
            message = quote(f"Hola quiero consultar por {product.name}")
            products.append(
                {
                    "name": product.name,
                    "category": product.category.name,
                    "description": product.description,
                    "price_label": product.price_label or f"S/ {product.base_price}",
                    "image_url": image,
                    "alt": product.name,
                    "whatsapp_url": f"https://wa.me/51960163257?text={message}",
                }
            )
        return render(request, "catalog/index.html", {"products": products})

    products = [
        {
            "name": "Toldera reforzada",
            "category": "Venta",
            "description": "Lona resistente para frente de negocio o vivienda.",
            "price_label": "S/ 280 desde",
            "image": "img/producto-1.webp",
            "alt": "Toldera azul a medida",
        },
        {
            "name": "Carpa comercial",
            "category": "Venta",
            "description": "Carpa para ferias, ventas y uso diario.",
            "price_label": "S/ 450 desde",
            "image": "img/producto-2.webp",
            "alt": "Carpa para comercio",
        },
        {
            "name": "Reparacion de lona",
            "category": "Servicio",
            "description": "Costuras, parches, refuerzos y cambio de piezas.",
            "price_label": "S/ 60 desde",
            "image": "img/producto-3.webp",
            "alt": "Reparacion de lona",
        },
        {
            "name": "Confeccion especial",
            "category": "A medida",
            "description": "Trabajo personalizado segun medida, uso y material.",
            "price_label": "S/ 120 desde",
            "image": "img/producto-4.webp",
            "alt": "Confeccion personalizada",
        },
        {
            "name": "Instalacion en campo",
            "category": "Instalacion",
            "description": "Montaje, tensionado y revision de estructura.",
            "price_label": "S/ 90 desde",
            "image": "img/producto-5.webp",
            "alt": "Instalacion de toldera",
        },
        {
            "name": "Trabajo personalizado",
            "category": "Proyecto",
            "description": "Soluciones para medidas especiales, negocios y eventos.",
            "price_label": "Cotizable",
            "image": "img/producto-6.webp",
            "alt": "Trabajo personalizado de carpa",
        },
    ]
    for product in products:
        message = quote(f"Hola quiero consultar por {product['name']}")
        product["whatsapp_url"] = f"https://wa.me/51960163257?text={message}"
        product["image_url"] = static(product["image"])
    return render(request, "catalog/index.html", {"products": products})

# Create your views here.
