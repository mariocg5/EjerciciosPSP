import threading


def procesar_usuario(ID,nombre,edad):
    print(f"Usuario ID: {ID}, nombre: {nombre}, Edad: {edad}")

hilos = []
nombres=["Mario", "Pedro", "Abel", "Nacho", "Ángel"]
edades=[26,20,21,19,22]

for i in range(5):
    hilo=threading.Thread(target=procesar_usuario, args= (i+1,), kwargs={ 'nombre' : nombres[i], 'edad': edades[i] })
    hilos.append(hilo)
    hilo.start()
    hilo.join()

for hilo in hilos:
    hilo.join()

print("Todos los hilos han terminado")
