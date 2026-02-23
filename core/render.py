from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

def render_view(template_name, context={}):
    # 1. Renderizamos el contenido específico (ej: finanzas.html)
    # Esto procesa los {% for %}, {% if %}, etc.
    content = render_to_string(template_name, context)
    context['content'] = mark_safe(content)

    # 2. Lógica de breadcrumbs (Generación de HTML manual)
    if 'breadcrumbs' in context:
        bc_html = ""
        for i, bc in enumerate(context['breadcrumbs']):
            is_last = i == len(context['breadcrumbs']) - 1
            if is_last:
                bc_html += f'<span class="bc-current">{bc["name"]}</span>'
            else:
                bc_html += f'<a href="{bc["url"]}" class="bc-item">{bc["name"]}</a>'
                bc_html += '<span class="bc-sep">/</span>'
        # Guardamos el HTML generado en el contexto
        context['breadcrumbs_placeholder'] = mark_safe(bc_html)
    else:
        context['breadcrumbs_placeholder'] = mark_safe('<span class="bc-current">Dashboard</span>')

    # 3. Renderizamos el layout final
    # Dentro de layout.html debes tener {{ breadcrumbs_placeholder }}
    return render_to_string('pages/layout.html', context)