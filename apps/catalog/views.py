from urllib.parse import quote

from django.shortcuts import render
from django.templatetags.static import static

from .models import Product


def catalog_index(request):
    db_products = Product.objects.filter(is_active=True).select_related("category")
    if db_products.exists():
        products = []
        for product in db_products:
            image = product.main_image_url or static("img/trabajos/carpa-multicolor-local-comercial.webp")
            message = quote(f"Hola quiero consultar por {product.name}")
            products.append(
                {
                    "name": product.name,
                    "category": product.category.name,
                    "description": product.description,
                    "price_label": product.price_label or product.display_price,
                    "image_url": image,
                    "alt": product.name,
                    "whatsapp_url": f"https://wa.me/51960163257?text={message}",
                    "discount_percent": product.discount_percent,
                    "has_discount": product.has_discount,
                    "previous_price": product.previous_price,
                }
            )
        return render(request, "catalog/index.html", {"products": products})

    products = [
        {
            "name": "Carpa multicolor para negocio",
            "category": "Venta",
            "description": "Carpa llamativa para locales, pollerias, ferias y puntos de venta.",
            "price_label": "Cotizar segun medida",
            "image": "img/trabajos/carpa-multicolor-local-comercial.webp",
            "alt": "Carpa multicolor instalada en local comercial",
        },
        {
            "name": "Toldo comercial para fachada",
            "category": "Venta",
            "description": "Toldo frontal para proteger y resaltar la entrada de un negocio.",
            "price_label": "Cotizar segun fachada",
            "image": "img/trabajos/toldo-cevicheria-el-tio-frontal.webp",
            "alt": "Toldo comercial para cevicheria instalado en fachada",
        },
        {
            "name": "Lona para camion de carga",
            "category": "Transporte",
            "description": "Lonas resistentes para cubrir carga, proteger mercaderia y soportar uso diario.",
            "price_label": "Cotizar segun camion",
            "image": "img/trabajos/lona-azul-camion-grande.webp",
            "alt": "Lona azul confeccionada para camion de carga",
        },
        {
            "name": "Toldo para pescaderia o restaurante",
            "category": "A medida",
            "description": "Toldos personalizados con colores y forma adaptada al tipo de negocio.",
            "price_label": "Cotizar personalizado",
            "image": "img/trabajos/toldo-azul-pescados-mariscos.webp",
            "alt": "Toldo azul instalado en local de pescados y mariscos",
        },
        {
            "name": "Carpa roja para exteriores",
            "category": "Instalacion",
            "description": "Carpa para sombra y proteccion en espacios abiertos o zonas de trabajo.",
            "price_label": "Cotizar instalacion",
            "image": "img/trabajos/carpa-roja-instalacion-campo.webp",
            "alt": "Carpa roja instalada en zona exterior",
        },
        {
            "name": "Lona verde para transporte",
            "category": "Proyecto",
            "description": "Confeccion de lona a medida para unidades de transporte y reparto.",
            "price_label": "Cotizable",
            "image": "img/trabajos/lona-verde-camion-transporte.webp",
            "alt": "Lona verde para camion de transporte",
        },
    ]
    for product in products:
        message = quote(f"Hola quiero consultar por {product['name']}")
        product["whatsapp_url"] = f"https://wa.me/51960163257?text={message}"
        product["image_url"] = static(product["image"])
        product["discount_percent"] = 0
        product["has_discount"] = False
        product["previous_price"] = None
    return render(request, "catalog/index.html", {"products": products})
