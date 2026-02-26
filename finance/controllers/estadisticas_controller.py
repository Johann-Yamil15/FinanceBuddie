import json
from django.shortcuts import redirect
from django.http import HttpResponse
from core.render import render_view
from finance.services.estadisticas_service import EstadisticasService

def estadisticas_dashboard(request):
    # 1. Validación de sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/acceso')

    # 2. Obtención de datos desde el nuevo EstadisticasService
    comparativa = EstadisticasService.obtener_comparativa_mensual(usuario_id)
    categorias_gastos = EstadisticasService.obtener_gastos_por_categoria(usuario_id)
    tendencia = EstadisticasService.obtener_tendencia_6_meses(usuario_id)
    insights = EstadisticasService.obtener_insights_avanzados(usuario_id)

    # 3. Lógica del "Score Financiero" (Análisis rápido)
    ingresos_act = float(comparativa['ingresos_actual'] or 0)
    gastos_act = float(comparativa['gastos_actual'] or 0)
    
    if ingresos_act > 0:
        ratio_gasto = (gastos_act / ingresos_act) * 100
        if ratio_gasto <= 50:
            score_text, score_class = "Excelente", "text-success"
        elif ratio_gasto <= 80:
            score_text, score_class = "Estable", "text-primary"
        else:
            score_text, score_class = "Crítico", "text-danger"
    else:
        score_text, score_class = "Sin datos", "text-muted"

    # 4. Preparación de datos para Chart.js (Formatos JSON)
    labels_dona = [c['categoria'] for c in categorias_gastos]
    values_dona = [float(c['total']) for c in categorias_gastos]

    labels_linea = [t['mes'] for t in tendencia]
    ingresos_linea = [float(t['ingresos']) for t in tendencia]
    gastos_linea = [float(t['gastos']) for t in tendencia]

    # Gráfica de Barras/Líneas: Tendencia
    labels_linea = [t['mes'] for t in tendencia]
    ingresos_linea = [float(t['ingresos']) for t in tendencia]
    gastos_linea = [float(t['gastos']) for t in tendencia]

    # 5. Armado del Contexto
    context = {
        "titulo": "Análisis Estadístico - Finance Buddie",
        "user_name": request.session.get('usuario_nombre', 'Johann Yamil'),
        
        # Tarjetas de Insights
        "comparativa": comparativa,
        "max_gasto": f"{insights['max_gasto']:,.2f}",
        "dia_pico": insights['dia_mas_gasto'],
        "score_text": score_text,
        "score_class": score_class,

        # Datos para los Scripts de las gráficas
        "chart_categorias": {
            "labels": labels_dona,
            "values": values_dona
        },
        "chart_tendencia": {
            "labels": labels_linea,
            "ingresos": ingresos_linea,
            "gastos": gastos_linea
        },

        "breadcrumbs": [
            {"name": "Finance Buddie", "url": "/"},
            {"name": "Estadísticas", "url": "#"}
        ]
    }

    html = render_view('finanzas/estadisticas.html', context)
    return HttpResponse(html)