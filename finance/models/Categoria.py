# finance/models.py

# ==========================================
# MODELO: CATEGORÍA
# ==========================================
class Categoria:
    def __init__(self, id=None, nombre=None):
        self.id = id
        self.nombre = nombre

    @staticmethod
    def from_dict(data):
        if not data:
            return None
            
        return Categoria(
            id=data.get('Id') or data.get('id'),
            nombre=data.get('Nombre') or data.get('nombre')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }