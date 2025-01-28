# Implementa un programa que cifre un mensaje usando cryptography (Fernet) y lo guarde en un archivo.
# Desencripta y muestra el contenido del archivo.

from cryptography.fernet import Fernet

def generar_clave():
    return Fernet.generate_key()

def cifrar_mensaje(mensaje, clave, archivo_cifrado):
    fernet=Fernet(clave) #Genero una objeto de tipo Fernet
    mensaje_cifrado=fernet.encrypt(mensaje.encode()) #Lo encripto y lo guardo en una variable

    with open(archivo_cifrado, 'wb') as archivo: archivo.write(mensaje_cifrado) #Guardo el mensaje cifrado en un archivo
    print(f"Mensaje cifrado en {archivo_cifrado}")
    return mensaje_cifrado

def descifrar_mensaje(clave, archivo_cifrado):
    fernet=Fernet(clave) #Genero la clave para poder desencriptar el mensaje

    with open(archivo_cifrado,'rb') as archivo: mensaje_cifrado= archivo.read() #Abro el archivo con el mensaje encriptado
    mensaje_descifrado = fernet.decrypt(mensaje_cifrado).decode()
    return mensaje_descifrado

if __name__ =='__main__':
    clave=generar_clave()  # Genero la clave
    archivo_cifrado ='archivoCifrado.txt'

    mensaje_cifrado = cifrar_mensaje("Hola",clave,archivo_cifrado)
    print(f"Mensaje cifrado: {mensaje_cifrado}")

    mensaje_descifrado= descifrar_mensaje(clave,archivo_cifrado)
    print(f"Mensaje descifrado: {mensaje_descifrado}")