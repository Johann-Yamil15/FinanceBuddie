# finance/urls.py
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
import re
from .controllers.dashboard_controller import home_dashboard
from .controllers.error_controller import not_found_action
from .controllers.finanzas_controller import finanzas_dashboard, gestionar_transaccion
from .controllers.auth_controller import auth_page, login_action, register_action, logout_action
from .controllers.estadisticas_controller import estadisticas_dashboard

def get_route_handler(path, method):
    clean_path = path.rstrip('/') if path != '/' else path
    routes = {
        ('/', 'GET'): lambda request: home_dashboard(request),
        ('/finanzas', 'GET'): lambda request: finanzas_dashboard(request),
        ('/estadisticas', 'GET'): lambda request: estadisticas_dashboard(request),
        
        # --- Rutas de Autenticación ---
        ('/acceso', 'GET'): lambda request: auth_page(request), 
        ('/login', 'POST'): lambda request: login_action(request),
        ('/register', 'POST'): lambda request: register_action(request),
        ('/logout', 'GET'): lambda request: logout_action(request),

        # --- API Endpoints ---
        ('/api/finanzas', 'POST'): lambda request: gestionar_transaccion(request),
    }
  

    # Intentar match exacto primero (GET y POST general)
    handler = routes.get((clean_path, method))
    if handler:
        return handler

    # --- Manejo de Rutas con ID (PUT y DELETE) ---
    # Ejemplo: /api/finanzas/5
    match = re.match(r'^/api/finanzas/(\+?\d+)$', path)
    if match:
        t_id = int(match.group(1))
        if method == 'PUT':
            return lambda request: gestionar_transaccion(request, t_id)
        if method == 'DELETE':
            return lambda request: gestionar_transaccion(request, t_id)

    return not_found_action

@csrf_exempt
def master_dispatcher(request):
    path = request.path
    method = request.method
    
    handler = get_route_handler(path, method)
    return handler(request)

urlpatterns = [
    re_path(r'^.*$', master_dispatcher),
]