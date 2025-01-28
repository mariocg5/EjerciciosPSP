# Crea un sistema donde solo el administrador pueda acceder a un recurso sensible.

usuarios ={"admin" : {"password":"admin123","rol":"administrador"},
           "mario" : {"password": "mario123", "rol": "usuario"}}

def autenticar(usuario,password):
    if usuario in usuarios and usuarios[usuario]["password"]==password:
        return True
    return False

def autorizar_acceso(usuario,recurso):
    rol=usuarios[usuario]["rol"]
    if rol=="administrador" and recurso =="RecursoSensible":
        return True
    return False

usuario= input("Introduce el nombre del usuario: ")
pwd = input("Introduce la contraseña: ")

if autenticar(usuario,pwd):
    recurso = "RecursoSensible"
    if autorizar_acceso(usuario,recurso):
        print(f"Acceso concedido a {recurso}")
    else:
        print("No tienes permiso para acceder al recurso sensible")
else:
    print("Error de autenticación")
