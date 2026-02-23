import os

def render_view(template_name, context={}):
    # 1. Usar la ruta absoluta del archivo actual para evitar errores en Render
    # Esto busca la carpeta 'views' partiendo desde donde esté 'core/render.py'
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(current_dir, 'views')
    
    # 2. Cargar el Layout
    layout_path = os.path.join(base_path, 'home', 'layout.html')
    
    try:
        with open(layout_path, 'r', encoding='utf-8') as f:
            layout = f.read()
    except FileNotFoundError:
        return f"Error Crítico: No se encontró el layout en {layout_path}".encode('utf-8')

    # 3. Leer la vista específica (ej: 'error/404.html')
    template_path = os.path.join(base_path, template_name)
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return f"Error: No se encontró la vista {template_name} en {template_path}".encode('utf-8')
    
    final_html = layout.replace('{{content}}', content)

    # 4. Lógica de breadcrumbs mejorada
    if 'breadcrumbs' in context:
        bc_html = ""
        for i, bc in enumerate(context['breadcrumbs']):
            is_last = i == len(context['breadcrumbs']) - 1
            if is_last:
                bc_html += f'<span class="bc-current">{bc["name"]}</span>'
            else:
                bc_html += f'<a href="{bc["url"]}" class="bc-item">{bc["name"]}</a>'
                bc_html += '<span class="bc-sep">/</span>'
        final_html = final_html.replace('{{breadcrumbs_placeholder}}', bc_html)
    else:
        # Si no hay breadcrumbs, ponemos un valor por defecto para que no se vea el {{placeholder}}
        final_html = final_html.replace('{{breadcrumbs_placeholder}}', 'Dashboard')

    # 5. Reemplazo de variables generales
    for key, value in context.items():
        placeholder = '{{' + key + '}}'
        final_html = final_html.replace(placeholder, str(value))
        
    return final_html.encode('utf-8')