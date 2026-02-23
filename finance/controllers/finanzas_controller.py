# finance/controllers/finanzas_controller.py
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.render import render_view
from datetime import datetime
from finance.services.finanzas_service import FinanzasService


def finanzas_dashboard(request):
    # Por el momento forzamos el ID 1 (Johann).
    # En el futuro esto vendrá de: request.session.get('usuario_id')
    usuario_id = 1

    # 1. Obtenemos los datos puros desde nuestro Service
    categorias_obj = FinanzasService.obtener_categorias()
    transacciones_obj = FinanzasService.obtener_transacciones(usuario_id)
    resumen = FinanzasService.obtener_resumen_financiero(usuario_id)

    # 2. Convertimos los objetos a diccionarios para que el HTML los lea fácilmente
    categorias_dict = [cat.to_dict() for cat in categorias_obj]
    transacciones_dict = [t.to_dict() for t in transacciones_obj]

    # 3. Armamos el contexto real
    context = {
        "titulo": "Control de Gastos - Finance Buddie",
        "user_name": "Johann Yamil",

        # Formateamos los números con comas y 2 decimales (ej: 1,950.00)
        "balance_total": f"{resumen['balance']:,.2f}",
        "ingresos": f"{resumen['ingresos']:,.2f}",
        "gastos": f"{resumen['gastos']:,.2f}",
        "porcentaje_ahorro": str(resumen['porcentaje_ahorro']),

        "fecha_actual": datetime.now().strftime("%d %b, %Y"),
        "categorias": categorias_dict,
        "transacciones": transacciones_dict,
        "breadcrumbs": [
            {"name": "Finance Buddie", "url": "/"},
            {"name": "Finanzas", "url": "#"}
        ]
    }

    html = render_view('finanzas/finanzas.html', context)
    return HttpResponse(html)


@csrf_exempt
def gestionar_transaccion(request, t_id=None):
    """Endpoint único para CRUD de transacciones vía Fetch API"""
    usuario_id = 1

    try:
        # CREAR: POST /finanzas/gestion/
        if request.method == 'POST':
            data = json.loads(request.body)
            FinanzasService.crear_transaccion(
                usuario_id,
                data['categoria_id'],
                data['tipo'],
                data['monto']
            )
            return JsonResponse({'status': 'success', 'message': 'Transacción registrada'})

        # EDITAR: PUT /finanzas/gestion/<id>/
        elif request.method == 'PUT' and t_id:
            data = json.loads(request.body)
            FinanzasService.actualizar_transaccion(
                t_id,
                data['categoria_id'],
                data['tipo'],
                data['monto']
            )
            return JsonResponse({'status': 'success', 'message': 'Transacción actualizada'})

        # ELIMINAR: DELETE /finanzas/gestion/<id>/
        elif request.method == 'DELETE' and t_id:
            FinanzasService.eliminar_transaccion(t_id)
            return JsonResponse({'status': 'success', 'message': 'Movimiento revertido y eliminado'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Acción no válida'}, status=400)
