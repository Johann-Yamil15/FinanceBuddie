from django.http import HttpResponse
from django.shortcuts import redirect
from core.render import render_view 

def home_dashboard(request):
    # 1. Validamos sesión (Igual que en Finanzas)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/acceso')

    # 2. Obtenemos datos de la sesión para el Layout
    context = {
        'titulo': 'Panel Financiero - Finance Buddie',
        'user_name': request.session.get('usuario_nombre', 'Usuario'),
        'user_email': request.session.get('usuario_email', 'correo@ejemplo.com'),
        'breadcrumbs': [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Dashboard', 'url': '/dashboard'}
        ],
    }
    
    html_response = render_view('pages/index.html', context)
    return HttpResponse(html_response)

# En auth_controller.py
def logout_action(request):
    request.session.flush() # Borra TODA la sesión (ID, Nombre, Email)
    return redirect('/acceso')