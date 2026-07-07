from django.shortcuts import render
from django.templatetags.static import static


def home(request):
    featured_products = [
        {
            "name": "Carpa multicolor para local",
            "category": "Producto estrella",
            "price": "Cotizar segun medida",
            "image_url": static("img/trabajos/carpa-multicolor-local-comercial.webp"),
            "alt": "Carpa multicolor instalada en local comercial",
        },
        {
            "name": "Toldo comercial de fachada",
            "category": "Mas consultado",
            "price": "Cotizar segun fachada",
            "image_url": static("img/trabajos/toldo-cevicheria-el-tio-frontal.webp"),
            "alt": "Toldo comercial instalado en fachada de negocio",
        },
        {
            "name": "Lona para camion de carga",
            "category": "Transporte",
            "price": "Cotizar segun camion",
            "image_url": static("img/trabajos/lona-azul-camion-grande.webp"),
            "alt": "Lona azul confeccionada para camion de carga",
        },
        {
            "name": "Carpa roja para exterior",
            "category": "Instalacion",
            "price": "Cotizar instalacion",
            "image_url": static("img/trabajos/carpa-roja-instalacion-campo.webp"),
            "alt": "Carpa roja instalada en zona exterior",
        },
        {
            "name": "Toldo para restaurante",
            "category": "A medida",
            "price": "Cotizar personalizado",
            "image_url": static("img/trabajos/toldo-azul-pescados-mariscos.webp"),
            "alt": "Toldo azul instalado en local de pescados y mariscos",
        },
        {
            "name": "Lona verde de transporte",
            "category": "Trabajo a medida",
            "price": "Cotizable",
            "image_url": static("img/trabajos/lona-verde-camion-transporte.webp"),
            "alt": "Lona verde para camion de transporte",
        },
    ]
    featured_jobs = [
        {
            "title": "Carpa multicolor para local comercial",
            "image_url": static("img/trabajos/carpa-multicolor-local-comercial.webp"),
            "alt": "Carpa multicolor instalada frente a local comercial en Pichanaki",
        },
        {
            "title": "Carpa roja instalada en campo",
            "image_url": static("img/trabajos/carpa-roja-instalacion-campo.webp"),
            "alt": "Instalacion de carpa roja para trabajo en campo",
        },
        {
            "title": "Toldo azul para pescados y mariscos",
            "image_url": static("img/trabajos/toldo-azul-pescados-mariscos.webp"),
            "alt": "Toldo azul instalado en local de pescados y mariscos",
        },
        {
            "title": "Lona azul para camion de carga",
            "image_url": static("img/trabajos/lona-azul-camion-grande.webp"),
            "alt": "Lona azul confeccionada para camion de carga grande",
        },
    ]
    return render(
        request,
        "public/home.html",
        {
            "featured_jobs": featured_jobs,
            "featured_products": featured_products,
        },
    )
