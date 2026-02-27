import json
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.render import render_view
from datetime import datetime
from finance.services.finanzas_service import FinanzasService

def finanzas_dashboard(request):
    usuario_id = request.session.get('usuario_id')
    nombre_usuario = request.session.get('usuario_nombre', 'Johann Yamil')
    
    if not usuario_id:
        return redirect('/acceso')

    categorias_obj = FinanzasService.obtener_categorias()
    transacciones_obj = FinanzasService.obtener_transacciones(usuario_id)
    resumen = FinanzasService.obtener_resumen_financiero(usuario_id)

    categorias_dict = [cat.to_dict() for cat in categorias_obj]
    transacciones_dict = [t.to_dict() for t in transacciones_obj]
    
    context = {
        "titulo": "Control de Gastos - Finance Buddie",
        "user_name": nombre_usuario,
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
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return JsonResponse({'status': 'error', 'message': 'Sesión inválida'}, status=401)
    
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            # CORRECCIÓN: Leemos 'categoria' que es el nombre del campo en el HTML
            # Si no viene, enviamos None para que el servicio lo maneje.
            cat_val = data.get('categoria') 
            
            FinanzasService.crear_transaccion(
                usuario_id, 
                cat_val, 
                data['tipo'], 
                data['monto']
            )
            return JsonResponse({'status': 'success', 'message': 'Transacción registrada'})

        elif request.method == 'PUT' and t_id:
            data = json.loads(request.body)
            cat_val = data.get('categoria')
            
            FinanzasService.actualizar_transaccion(
                t_id, 
                cat_val, 
                data['tipo'], 
                data['monto']
            )
            return JsonResponse({'status': 'success', 'message': 'Transacción actualizada'})

        elif request.method == 'DELETE' and t_id:
            FinanzasService.eliminar_transaccion(t_id)
            return JsonResponse({'status': 'success', 'message': 'Movimiento eliminado'})

    except Exception as e:
        print(f"Error backend: {e}") # Log para depuración
        return JsonResponse({'status': 'error', 'message': f"Error interno: {str(e)}"}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Acción no válida'}, status=400)

def metas_dashboard(request):
    usuario_id = request.session.get('usuario_id')
    nombre_usuario = request.session.get('usuario_nombre', 'Usuario')
    if not usuario_id: return redirect('/acceso')

    metas_ahorro = FinanzasService.obtener_metas_usuario(usuario_id)
    context = {
        "titulo": "Metas de Ahorro - Finance Buddie",
        "user_name": nombre_usuario,
        "metas_ahorro": metas_ahorro,
        "breadcrumbs": [
            {"name": "Finance Buddie", "url": "/"},
            {"name": "Metas de Ahorro", "url": "#"}
        ]
    }
    html = render_view('finanzas/metas.html', context)
    return HttpResponse(html)

@csrf_exempt
def gestionar_meta(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id: return JsonResponse({'status': 'error', 'message': 'Sesión inválida'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            FinanzasService.crear_meta(usuario_id, data['nombre'], data['monto_objetivo'])
            return JsonResponse({'status': 'success', 'message': 'Meta creada correctamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def chat_dashboard(request):
    usuario_id = request.session.get('usuario_id')
    nombre_usuario = request.session.get('usuario_nombre', 'Usuario')
    if not usuario_id: return redirect('/acceso')

    context = {
        "titulo": "Asistente IA - Finance Buddie",
        "user_name": nombre_usuario,
        "breadcrumbs": [
            {"name": "Finance Buddie", "url": "/"},
            {"name": "Asistente IA", "url": "#"}
        ]
    }
    html = render_view('finanzas/chat.html', context)
    return HttpResponse(html)