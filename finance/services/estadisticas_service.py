from django.db import connection

class EstadisticasService:
    
    @staticmethod
    def _dictfetchall(cursor):
        """Convierte los resultados de SQL a una lista de diccionarios"""
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def obtener_comparativa_mensual(usuario_id):
        """
        Calcula Ingresos vs Gastos del mes actual vs mes anterior
        """
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    SUM(CASE WHEN Tipo = 'ingreso' AND MONTH(Fecha) = MONTH(GETDATE()) THEN Monto ELSE 0 END) as ingresos_actual,
                    SUM(CASE WHEN Tipo = 'gasto' AND MONTH(Fecha) = MONTH(GETDATE()) THEN Monto ELSE 0 END) as gastos_actual,
                    SUM(CASE WHEN Tipo = 'ingreso' AND MONTH(Fecha) = MONTH(DATEADD(month, -1, GETDATE())) THEN Monto ELSE 0 END) as ingresos_pasado,
                    SUM(CASE WHEN Tipo = 'gasto' AND MONTH(Fecha) = MONTH(DATEADD(month, -1, GETDATE())) THEN Monto ELSE 0 END) as gastos_pasado
                FROM Transacciones
                WHERE UsuarioId = %s AND YEAR(Fecha) = YEAR(GETDATE())
            """
            cursor.execute(query, [usuario_id])

            return EstadisticasService._dictfetchall(cursor)[0] # Usamos el helper de tu otro service o cópialo aquí

    @staticmethod
    def obtener_gastos_por_categoria(usuario_id):
        """Datos para la gráfica de Dona"""
        with connection.cursor() as cursor:
            query = """
                SELECT c.Nombre as categoria, SUM(t.Monto) as total
                FROM Transacciones t
                JOIN Categorias c ON t.CategoriaId = c.Id
                WHERE t.UsuarioId = %s AND t.Tipo = 'gasto'
                GROUP BY c.Nombre
                ORDER BY total DESC
            """
            cursor.execute(query, [usuario_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def obtener_tendencia_6_meses(usuario_id):
        """Datos para la gráfica de Líneas/Barras"""
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    FORMAT(Fecha, 'MMM') as mes,
                    MONTH(Fecha) as mes_num,
                    SUM(CASE WHEN Tipo = 'ingreso' THEN Monto ELSE 0 END) as ingresos,
                    SUM(CASE WHEN Tipo = 'gasto' THEN Monto ELSE 0 END) as gastos
                FROM Transacciones
                WHERE UsuarioId = %s AND Fecha >= DATEADD(month, -5, GETDATE())
                GROUP BY FORMAT(Fecha, 'MMM'), MONTH(Fecha), YEAR(Fecha)
                ORDER BY YEAR(Fecha) ASC, mes_num ASC
            """
            cursor.execute(query, [usuario_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def obtener_insights_avanzados(usuario_id):
        """
        Calcula datos curiosos: Día más caro, Categoría estrella y ahorro promedio
        """
        with connection.cursor() as cursor:
            # Día de la semana con más gasto
            cursor.execute("""
                SELECT TOP 1 DATENAME(weekday, Fecha) as dia
                FROM Transacciones
                WHERE UsuarioId = %s AND Tipo = 'gasto'
                GROUP BY DATENAME(weekday, Fecha)
                ORDER BY SUM(Monto) DESC
            """, [usuario_id])
            res_dia = cursor.fetchone()
            
            # Gasto más alto registrado
            cursor.execute("""
                SELECT MAX(Monto) FROM Transacciones WHERE UsuarioId = %s AND Tipo = 'gasto'
            """, [usuario_id])
            res_max = cursor.fetchone()

            return {
                "dia_mas_gasto": res_dia[0] if res_dia else "N/A",
                "max_gasto": float(res_max[0]) if res_max and res_max[0] else 0.0
            }
        
    @staticmethod
    def _dictfetchall(cursor):
        """Retorna todas las filas de un cursor como un diccionario"""
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]