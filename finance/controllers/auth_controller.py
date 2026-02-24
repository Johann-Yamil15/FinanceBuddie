from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..services.auth_service import AuthService

def auth_page(request):
    """Renderiza la vista de Login/Registro"""
    return render(request, 'auth/login.html')

def logout_action(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/acceso')

import json # <-- Asegúrate de tener esto en tus imports

def login_action(request):
    if request.method == 'POST':
        print("\n" + "="*50)
        print(" [LOGIN] Intentando iniciar sesión...")
        
        # 1. Intentamos leer los datos como Formulario Tradicional
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 2. Si vienen vacíos, significa que JavaScript los envió como JSON (Fetch)
        if not email and not password:
            try:
                data = json.loads(request.body)
                email = data.get('email')
                password = data.get('password')
                print(" [DEBUG] Datos recibidos en formato JSON.")
            except Exception as e:
                print(f" [ERROR] No se pudo leer el cuerpo de la petición: {e}")

        print(f" [DEBUG] Email detectado: {email}")
        print(f" [DEBUG] Password detectada: {'Sí (Oculta)' if password else 'VACÍO/NULA'}")

        # 3. Validar con el Service
        if email and password:
            success, user = AuthService.login_user(request, email, password)
            if success:
                print(f" [SUCCESS] Login correcto para {email}. Redirigiendo...")
                # Si usas Fetch en JS, a veces es mejor responder con JSON y que JS haga el window.location
                # Pero si tu JS maneja bien el redirect de Django, dejamos esto:
                return redirect('/finanzas') 
            else:
                print(" [WARNING] Contraseña incorrecta o usuario no encontrado.")
        else:
            print(" [ERROR] Faltan datos. Email o Password llegaron vacíos.")

        return JsonResponse({'status': 'error', 'message': 'Credenciales inválidas'}, status=401)

def register_action(request):
    """Maneja la petición del formulario de registro con logs de consola."""
    if request.method == 'POST':
        print("\n" + "="*50)
        print(" [REGISTRO] Iniciando proceso de registro...")
        
        # Capturamos datos
        datos = {
            'nombre': request.POST.get('nombre'),
            'ap': request.POST.get('ap'),
            'am': request.POST.get('am'),
            'email': request.POST.get('email'),
            'fecha_nac': request.POST.get('fecha_nac'),
            'password': request.POST.get('password')
        }
        
        print(f" [DEBUG] Datos recibidos: {datos['nombre']} ({datos['email']})")
        print(f" [DEBUG] Apellidos: {datos['ap']} {datos['am']} | Fecha Nac: {datos['fecha_nac']}")

        # Intentamos crear el usuario
        try:
            success, result = AuthService.register_user(
                datos['nombre'], datos['ap'], datos['am'], 
                datos['email'], datos['fecha_nac'], datos['password']
            )
            
            if success:
                print(f" [SUCCESS] Usuario creado exitosamente: {result}")
                
                # Intentamos loguear
                log_success, user = AuthService.login_user(request, datos['email'], datos['password'])
                
                if log_success:
                    print(f" [LOGIN] Sesión iniciada automáticamente para: {datos['email']}")
                    print(" [REDIRECT] Redirigiendo a /finanzas...")
                    print("="*50 + "\n")
                    return redirect('/finanzas')
                else:
                    print(" [ERROR] Usuario creado pero falló el inicio de sesión automático.")
            else:
                print(f" [WARNING] Error en validación de registro: {result}")
                return JsonResponse({'status': 'error', 'message': result}, status=400)

        except Exception as e:
            print(f" [FATAL ERROR] Excepción no controlada en registro: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'}, status=500)

    print(" [ERROR] Se intentó acceder a register_action sin método POST")
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)