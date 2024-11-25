import random
import threading
import time

semaforo = threading.Semaphore(3)

def acceder_estacionamiento(id_vehiculo):
    print(f"El vehiculo {id_vehiculo}, esta intentando entrar al estacionamiento")
    semaforo.acquire()
    print(f"El vehiculo {id_vehiculo}, ha entrado al estacionamiento")
    time.sleep(random.uniform(1,3))
    print(f"El vehiculo {id_vehiculo} ha salido del estacionamiento")
    semaforo.release()

coches=[]

for i in range (10):
    t = threading.Thread(target=acceder_estacionamiento, args={i})
    coches.append(t)
    t.start()

for coche in coches:
    coche.join()

print("Todos los coches han salido del estacionamiento")
