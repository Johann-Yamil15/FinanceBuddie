# finance/models/Transaccion.py
from datetime import datetime

class Transaccion:
    def __init__(self, id, usuario_id, categoria_id, tipo, monto, fecha, categoria_nombre=""):
        self.id = id
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.tipo = tipo
        self.monto = monto
        self.fecha = fecha
        self.categoria = categoria_nombre  # Aquí guardamos el nombre para el HTML

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('Id'),
            usuario_id=data.get('UsuarioId'),
            categoria_id=data.get('CategoriaId'),
            tipo=data.get('Tipo'),
            monto=data.get('Monto'),
            fecha=data.get('Fecha'),
            # Tomamos 'CategoriaNombre' que viene del JOIN de SQL Server
            categoria_nombre=data.get('CategoriaNombre', 'Sin Categoría') 
        )

    def to_dict(self):
        # Damos formato a la fecha para que no salga con los milisegundos
        fecha_formateada = ""
        if isinstance(self.fecha, datetime):
            fecha_formateada = self.fecha.strftime("%d %b, %Y") # Ej: 22 Feb, 2026
        elif self.fecha:
            fecha_formateada = str(self.fecha)

        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
            "tipo": self.tipo,
            "monto": float(self.monto) if self.monto else 0.0,
            "fecha": fecha_formateada,
            "categoria": self.categoria # Esto es lo que lee {{ t.categoria }} en el HTML
        }