from django.shortcuts import render
from django.templatetags.static import static


def home(request):
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
    return render(request, "public/home.html", {"featured_jobs": featured_jobs})
