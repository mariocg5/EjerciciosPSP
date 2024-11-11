import threading


def imprimir_mensaje(mensaje,veces):
    for i in range(veces):
        print(f"{i+1}: {mensaje}")

hilo=threading.Thread(target=imprimir_mensaje, args=("Hola desde el hilo", 3))
hilo.start()
hilo.join()

print("El hilo ha terminado")