# finance/urls.py
from django.urls import re_path
from .controllers.dashboard_controller import home_dashboard
from .controllers.error_controller import not_found_action
from .controllers.finanzas_controller import finanzas_dashboard

# 1. Tu lógica de diccionario (Se queda igual)
def get_route_handler(path, method):
    routes = {
        ('/', 'GET'): lambda request: home_dashboard(request),
        ('/finanzas', 'GET'): lambda request: finanzas_dashboard(request),
        
    }

    handler = routes.get((path, method))
    if handler:
        return handler, '200 OK'

    return not_found_action, '404 Not Found'

# 2. El "Puente" para Django
def master_dispatcher(request):
    """
    Esta función recibe TODAS las peticiones y las filtra 
    usando tu diccionario get_route_handler.
    """
    path = request.path
    method = request.method
    
    handler, status = get_route_handler(path, method)
    
    # Ejecuta la función encontrada (home_dashboard o not_found_action)
    return handler(request)

# 3. La variable que Django busca (OBLIGATORIA)
urlpatterns = [
    # Esta línea le dice a Django: "Cualquier cosa (^.*$) mándala al dispatcher"
    re_path(r'^.*$', master_dispatcher),
]