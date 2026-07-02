from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-general/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-general/usuarios/", views.users_index, name="users"),
    path("admin-general/usuarios/nuevo/", views.user_create, name="user_create"),
    path("admin-general/usuarios/<int:user_id>/editar/", views.user_edit, name="user_edit"),
    path("admin-general/descargar-bdd/", views.database_download, name="database_download"),
]
