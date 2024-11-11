import threading


def mostrar_informacion(nombre,edad):
    print(f"Nombre: {nombre} -- Edad: {edad}")

hilo=threading.Thread(target=mostrar_informacion, kwargs={'nombre': "Mario", 'edad': 25})
hilo.start()
hilo.join()
print("El hilo ha finalizado")