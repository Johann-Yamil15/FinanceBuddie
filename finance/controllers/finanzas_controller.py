# finance/controllers/finanzas_controller.py
from django.http import HttpResponse
from core.render import render_view
from datetime import datetime

def finanzas_dashboard(request):
    # En el futuro, aquí capturarás filtros de request.GET
    context = {
        "titulo": "Control de Gastos - Finance Buddie",
        "user_name": "Johann Yamil",
        "balance_total": "1,950.00",
        "porcentaje_ahorro": "12",
        "ingresos": "2,400.00",
        "gastos": "450.00",
        "fecha_actual": datetime.now().strftime("%d %b, %Y"),
        "categorias": ["Comida", "Compras", "Entretenimiento", "Transporte", "Servicios", "Salud", "Educación"],
        "transacciones": [
            {"icon": "utensils", "categoria": "Comida", "fecha": "Hoy", "monto": "15.00", "tipo": "gasto"},
            {"icon": "bus", "categoria": "Transporte", "fecha": "Hoy", "monto": "5.50", "tipo": "gasto"},
            {"icon": "briefcase", "categoria": "Honorarios", "fecha": "22 Feb", "monto": "1,200.00", "tipo": "ingreso"},
            {"icon": "shopping-cart", "categoria": "Compras", "fecha": "21 Feb", "monto": "85.00", "tipo": "gasto"},
        ],
        "breadcrumbs": [
            {"name": "Finance Buddie", "url": "/"},
            {"name": "Finanzas", "url": "#"}
        ]
    }
    
    html = render_view('finanzas/finanzas.html', context)
    return HttpResponse(html)