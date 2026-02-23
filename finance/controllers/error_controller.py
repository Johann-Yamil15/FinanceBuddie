# finance/controllers/error_controller.py
from django.http import HttpResponseNotFound
from core.render import render_view

def not_found_action(request):
    context = {
        "titulo": "404 - No Encontrado",
        "user_name": "Johann Yamil",
        "path": request.path,
        "breadcrumbs": [
            {"name": "Finance Buddie", "url": "/"},
            {"name": "Error 404", "url": "#"}
        ],
    }
    
    html_content = render_view('error/404.html', context)
    
    # Enviamos el contenido procesado con el status 404
    return HttpResponseNotFound(html_content)