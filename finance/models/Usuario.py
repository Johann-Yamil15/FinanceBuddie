# finance/models.py
from datetime import datetime

# ==========================================
# MODELO: USUARIO
# ==========================================
class Usuario:
    def __init__(self, id=None, nombre=None, ap=None, am=None, email=None, fecha_nac=None, password_hash=None):
        self.id = id
        self.nombre = nombre
        self.ap = ap
        self.am = am
        self.email = email
        self.fecha_nac = fecha_nac
        self.password_hash = password_hash

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        
        return Usuario(
            id=data.get('Id') or data.get('id'),
            nombre=data.get('Nombre') or data.get('nombre'),
            ap=data.get('ApellidoP') or data.get('ap'),
            am=data.get('ApellidoM') or data.get('am'),
            email=data.get('Email') or data.get('email'),
            fecha_nac=data.get('FechaNacimiento') or data.get('fecha_nac'),
            password_hash=data.get('PasswordHash') or data.get('password_hash')
        )

    def to_dict(self, include_password=False):
        user_dict = {
            "id": self.id,
            "nombre": self.nombre,
            "ap": self.ap,
            "am": self.am,
            "email": self.email,
            "fecha_nac": str(self.fecha_nac) if self.fecha_nac else None,
        }
        if include_password:
            user_dict["password_hash"] = self.password_hash
        return user_dict