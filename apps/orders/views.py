from django.shortcuts import render

from .models import Order


def tracking(request):
    code = request.GET.get("codigo", "ER-2407").strip().upper() or "ER-2407"
    db_order = Order.objects.filter(tracking_code=code).select_related("customer").first()
    if db_order:
        status_order = [
            Order.Status.RECEIVED,
            Order.Status.IN_PROGRESS,
            Order.Status.READY,
            Order.Status.DELIVERED,
        ]
        labels = {
            Order.Status.RECEIVED: "Recibido",
            Order.Status.IN_PROGRESS: "En confeccion",
            Order.Status.READY: "Listo para entrega",
            Order.Status.DELIVERED: "Entregado",
        }
        current_index = status_order.index(db_order.status) if db_order.status in status_order else 0
        steps = []
        for index, status in enumerate(status_order):
            state = "active" if index == current_index else "done" if index < current_index else ""
            steps.append({"label": labels[status], "state": state})
        order = {
            "code": db_order.tracking_code,
            "title": db_order.description,
            "total": db_order.total,
            "advance": db_order.advance,
            "balance": db_order.balance,
            "steps": steps,
        }
        return render(request, "orders/tracking.html", {"code": code, "order": order})

    order = {
        "code": code if code == "ER-2407" else "ER-2407",
        "title": "Toldera reforzada para local",
        "total": "380",
        "advance": "150",
        "balance": "230",
        "steps": [
            {"label": "Recibido", "state": "done"},
            {"label": "En confeccion", "state": "done"},
            {"label": "Listo para entrega", "state": "active"},
            {"label": "Entregado", "state": ""},
        ],
    }
    return render(request, "orders/tracking.html", {"code": code, "order": order})

# Create your views here.
