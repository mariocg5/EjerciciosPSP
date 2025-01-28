# Usa la librería hashlib para crear una función que guarde una contraseña de forma segura (hash). º

import hashlib

def crear_password(mensaje):
    mensaje_encriptado=mensaje.encode()
    hash_mensaje=hashlib.sha256(mensaje_encriptado).hexdigest()
    print("hash del mensaje:", hash_mensaje)

if __name__ == '__main__':
    crear_password("admin")