# finance/services/finanzas_service.py
from django.db import connection
# Importamos la CLASE Categoria desde el ARCHIVO Categoria
from finance.models.Categoria import Categoria 

# Importamos la CLASE Transaccion desde el ARCHIVO Transaccion
from finance.models.Transaccion import Transaccion

class FinanzasService:
    
    @staticmethod
    def _dictfetchall(cursor):
        """Retorna todas las filas de un cursor como un diccionario"""
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def obtener_categorias():
        with connection.cursor() as cursor:
            # Traemos todas las categorías ordenadas alfabéticamente
            cursor.execute("SELECT Id, Nombre FROM Categorias ORDER BY Nombre")
            filas = FinanzasService._dictfetchall(cursor)
        
        # Convertimos las filas de SQL a objetos Python usando tu modelo
        return [Categoria.from_dict(fila) for fila in filas]

    @staticmethod
    def obtener_transacciones(usuario_id):
        with connection.cursor() as cursor:
            # Hacemos un JOIN para traer el nombre de la categoría junto con la transacción
            query = """
                SELECT 
                    t.Id, t.UsuarioId, t.CategoriaId, t.Tipo, t.Monto, t.Fecha,
                    c.Nombre AS CategoriaNombre
                FROM Transacciones t
                JOIN Categorias c ON t.CategoriaId = c.Id
                WHERE t.UsuarioId = %s
                ORDER BY t.Fecha DESC
            """
            cursor.execute(query, [usuario_id])
            filas = FinanzasService._dictfetchall(cursor)
        
        return [Transaccion.from_dict(fila) for fila in filas]

    @staticmethod
    def obtener_resumen_financiero(usuario_id):
        with connection.cursor() as cursor:
            query = """
                SELECT Tipo, SUM(Monto) as Total 
                FROM Transacciones 
                WHERE UsuarioId = %s 
                GROUP BY Tipo
            """
            cursor.execute(query, [usuario_id])
            filas = FinanzasService._dictfetchall(cursor)

        ingresos = 0.0
        gastos = 0.0
        
        for fila in filas:
            if fila['Tipo'] == 'ingreso' and fila['Total'] is not None:
                ingresos = float(fila['Total'])
            elif fila['Tipo'] == 'gasto' and fila['Total'] is not None:
                gastos = float(fila['Total'])

        balance = ingresos - gastos
        porcentaje = round(((ingresos - gastos) / ingresos) * 100) if ingresos > 0 else 0

        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": balance,
            "porcentaje_ahorro": porcentaje
        }
    @staticmethod
    def crear_transaccion(usuario_id, categoria_id, tipo, monto):
        with connection.cursor() as cursor:
            query = """
                INSERT INTO Transacciones (UsuarioId, CategoriaId, Tipo, Monto, Fecha)
                VALUES (%s, %s, %s, %s, GETDATE())
            """
            cursor.execute(query, [usuario_id, categoria_id, tipo, monto])

    @staticmethod
    def actualizar_transaccion(t_id, categoria_id, tipo, monto):
        with connection.cursor() as cursor:
            query = """
                UPDATE Transacciones 
                SET CategoriaId = %s, Tipo = %s, Monto = %s 
                WHERE Id = %s
            """
            cursor.execute(query, [categoria_id, tipo, monto, t_id])

    @staticmethod
    def eliminar_transaccion(t_id):
        with connection.cursor() as cursor:
            # Al borrar la fila, el SUM(Monto) del resumen ignorará este valor,
            # logrando el efecto contable de "devolver" el dinero.
            cursor.execute("DELETE FROM Transacciones WHERE Id = %s", [t_id])