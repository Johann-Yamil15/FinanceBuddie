# finance/controllers/dashboard_controller.py
from django.http import HttpResponse
from core.render import render_view 

def home_dashboard(request):
    context = {
        'titulo': 'Panel Financiero - Finance Buddie',
        'user_name': 'Johann Yamil',
        'breadcrumbs': [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Dashboard', 'url': '/dashboard'}
        ],
    }
    
    # render_view ahora devuelve el HTML procesado por el motor de Django
    html_response = render_view('pages/index.html', context)
    return HttpResponse(html_response)