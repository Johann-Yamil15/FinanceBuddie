# ==========================================
# MODELO: TRANSACCIÓN
# ==========================================
class Transaccion:
    def __init__(self, id=None, usuario_id=None, categoria_id=None, tipo=None, monto=None, fecha=None, categoria_nombre=None):
        self.id = id
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.tipo = tipo
        self.monto = monto
        self.fecha = fecha

        # Dato extra (viene del JOIN para mostrar el texto en vez del número de ID)
        self.categoria_nombre = categoria_nombre

    @staticmethod
    def from_dict(data):
        if not data:
            return None

        return Transaccion(
            id=data.get('Id') or data.get('id'),
            usuario_id=data.get('UsuarioId') or data.get('usuario_id'),
            categoria_id=data.get('CategoriaId') or data.get('categoria_id'),
            tipo=data.get('Tipo') or data.get('tipo'),
            monto=data.get('Monto') or data.get('monto'),
            fecha=data.get('Fecha') or data.get('fecha'),
            categoria_nombre=data.get(
                'CategoriaNombre') or data.get('categoria_nombre')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
            "tipo": self.tipo,
            "monto": float(self.monto) if self.monto is not None else 0.0,
            "fecha": str(self.fecha) if self.fecha else None,
            "categoria_nombre": self.categoria_nombre
        }
