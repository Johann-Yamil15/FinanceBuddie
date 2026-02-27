from django.db import models

class MetaAhorro(models.Model):
    # Usamos IntegerField para mantener la simplicidad con tu sistema de sesiones actual
    usuario_id = models.IntegerField() 
    nombre = models.CharField(max_length=100)
    monto_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_limite = models.DateField(null=True, blank=True)

    @property
    def porcentaje_completado(self):
        if self.monto_objetivo > 0:
            return min(int((self.monto_actual / self.monto_objetivo) * 100), 100)
        return 0

    def __str__(self):
        return f"{self.nombre} - {self.porcentaje_completado}%"