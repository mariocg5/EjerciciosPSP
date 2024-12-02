import threading
import time
import random

corredor_listo=threading.Event()

def corredor(id_corredor):
    print(f"Corredor {id_corredor} en posicion, esperando señal de salida")
    corredor_listo.wait() #Espera a que se de la salida
    print(f"Corredor {id_corredor} ha llegado a la meta")

def iniciar_carrera():
    print("Señal de salida en breves instantes...")
    time.sleep(random.uniform(1, 3))
    corredor_listo.set()
    print("Salida!! Los corredores han comenzado la carrera")


corredores = []

for i in range(5):
    c = threading.Thread(target=corredor, args=(i, ))
    corredores.append(c)
    c.start()

salida = threading.Thread(target=iniciar_carrera)
salida.start()

for c in corredores:
    c.join()

salida.join()

print("Carrera finalizada!!")