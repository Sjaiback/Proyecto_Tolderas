# Proyecto Tolderas

Sistema Django para Tolderas y Carpas el Ruso.

## Rutas principales

- `/` web publica
- `/catalogo/` catalogo de productos
- `/rastreo/` consulta de pedido por codigo
- `/panel/` panel operativo del taller
- `/inteligencia/` inteligencia de negocio
- `/admin/` administracion Django

## Base de datos local

La configuracion se lee desde `.env`.

```env
POSTGRES_DB=TallerTolderaBDD
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-password-local
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Comandos

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Apps

- `apps.public`: paginas publicas
- `apps.catalog`: categorias y productos
- `apps.orders`: clientes, pedidos, pagos y tickets
- `apps.operations`: inventario y movimientos
- `apps.analytics`: snapshots y metricas
