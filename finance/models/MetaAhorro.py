from django.db import models

class MetaAhorro(models.Model):
    # Asegúrate de que los nombres de los campos coincidan con tu SQL o usa db_column
    usuario_id = models.IntegerField(db_column='UsuarioId') 
    nombre = models.CharField(max_length=100, db_column='Nombre')
    monto_objetivo = models.DecimalField(max_digits=18, decimal_places=2, db_column='MontoObjetivo')
    monto_actual = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, db_column='MontoActual')
    # En tu SQL se llama FechaCreacion, no fecha_limite
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='FechaCreacion')

    class Meta:
        db_table = 'MetasAhorro'  # Este es el nombre exacto en tu SQL
        managed = False           # Indica que Django no debe intentar crear/modificar esta tabla

    @property
    def porcentaje_completado(self):
        if self.monto_objetivo > 0:
            return min(int((self.monto_actual / self.monto_objetivo) * 100), 100)
        return 0

    def __str__(self):
        return f"{self.nombre} - {self.porcentaje_completado}%"