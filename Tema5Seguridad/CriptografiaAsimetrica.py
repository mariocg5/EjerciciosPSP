# Implementa un programa que cifre un mensaje con clave pública y lo descifre con clave privada.

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

private_key=rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key=private_key.public_key()

pem_privada = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
pem_publica = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
print("Clave privada:")
print(pem_privada.decode())
print("Clave pública:")
print(pem_publica.decode())

mensaje=input("Introduce un mensaje para cifrar: ")
mensaje_bytes=mensaje.encode()

mensaje_cifrado = public_key.encrypt( #Utilizo la clave publica para encriptar el mensaje
    mensaje_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
print(f"Mensaje cifrado: {mensaje_cifrado}")


mensaje_descifrado = private_key.decrypt( #El servidor utilizaría la clave privada para desencriptarlo
    mensaje_cifrado,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
print(f"Mensaje descifrado: {mensaje_descifrado.decode()}")
