from django.db import connection
from django.contrib.auth.hashers import make_password, check_password

class AuthService:
    @staticmethod
    def register_user(nombre, ap, am, email, fecha_nac, password):
        try:
            with connection.cursor() as cursor:
                # 1. Verificar si ya existe en TU tabla
                cursor.execute("SELECT Id FROM Usuarios WHERE Email = %s", [email])
                if cursor.fetchone():
                    return False, "El correo ya está registrado"

                # 2. Insertar en TU tabla
                sql = """
                    INSERT INTO Usuarios (Nombre, ApellidoP, ApellidoM, Email, FechaNacimiento, PasswordHash)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                hashed_pwd = make_password(password)
                cursor.execute(sql, [nombre, ap, am, email, fecha_nac, hashed_pwd])
                
            return True, "Registro exitoso en tabla Usuarios"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def login_user(request, email, password):
        try:
            with connection.cursor() as cursor:
                # Buscar en TU tabla
                cursor.execute("SELECT Id, Nombre, Email, PasswordHash FROM Usuarios WHERE Email = %s", [email])
                row = cursor.fetchone()
                
                if row:
                    # row[3] es el PasswordHash
                    if check_password(password, row[3]):
                        # --- SESIÓN MANUAL ---
                        # Guardamos los datos en la sesión sin usar la tabla auth_user
                        request.session['usuario_id'] = row[0]
                        request.session['usuario_nombre'] = row[1]
                        request.session['usuario_email'] = row[2]
                        return True, row
            return False, None
        except Exception as e:
            print(f"Error login: {e}")
            return False, None