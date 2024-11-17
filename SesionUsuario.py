import threading
import time

datos_sesion=threading.local()

class SesionUsuario:

    def iniciar_sesion(self, nombre_usuario):
        datos_sesion.nombre_usuario=nombre_usuario #Almacena el nombre del usuario en una variable local del hilo

    def mostrar_sesion(self):
        print(f"Sesión iniciada para el usuario {datos_sesion.nombre_usuario}")

def gestionar_sesion(nombre_usuario): #función principal
    datos_sesion=SesionUsuario() #Instancia del objeto de la clase
    datos_sesion.iniciar_sesion(nombre_usuario)
    datos_sesion.mostrar_sesion()

hilos = []
nombres_usuarios = ["Mario", "Pedro", "Luis", "Marcos", "Ana"]

for nombres in nombres_usuarios:
    hilo = threading.Thread(target=gestionar_sesion, args=(nombres,))
    time.sleep(1)
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

