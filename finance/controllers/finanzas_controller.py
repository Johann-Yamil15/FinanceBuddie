# finance/controllers/finanzas_controller.py
import json
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.render import render_view
from datetime import datetime
from finance.services.finanzas_service import FinanzasService

def finanzas_dashboard(request):
    print("\n" + ">>>" * 10)
    print(" [DEBUG] Cargando Dashboard de Finanzas...")
    
    # Verificamos qué hay en la sesión
    usuario_id = request.session.get('usuario_id')
    nombre_usuario = request.session.get('usuario_nombre', 'Johann Yamil')
    
    print(f" [DEBUG] Usuario ID en Sesión: {usuario_id}")
    print(f" [DEBUG] Nombre en Sesión: {nombre_usuario}")

    if not usuario_id:
        print(" [AUTH] No hay ID. Redirigiendo...")
        return redirect('/acceso')

    # 1. Datos del Service
    categorias_obj = FinanzasService.obtener_categorias()
    transacciones_obj = FinanzasService.obtener_transacciones(usuario_id)
    resumen = FinanzasService.obtener_resumen_financiero(usuario_id)

    print(f" [DEBUG] Transacciones encontradas: {len(transacciones_obj)}")
    print(f" [DEBUG] Resumen calculado: Balance {resumen['balance']}")

    # 2. Conversión
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
    usuario_id = request.session.get('usuario_id')
    
    print(f"\n [API] Petición {request.method} recibida")
    print(f" [API] Usuario ID detectado: {usuario_id}")

    if not usuario_id:
        print(" [ERROR API] Intento de posteo sin sesión activa.")
        return JsonResponse({'status': 'error', 'message': 'Sesión inválida'}, status=401)
    
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
