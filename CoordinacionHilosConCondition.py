import threading

contador = 1
cond = threading.Condition()

def preparacion():
    global contador
    for _ in range(5):
        with cond:
            cond.wait_for(lambda: contador == 1) #Cuando el contador sea 1, se ejecuta
            print(f"Preparación {contador} completada")
            contador = contador + 1
            cond.notify_all()

def procesamiento():
    global contador
    for _ in range(5):
        with cond:
            cond.wait_for(lambda: contador == 2)#Cuando el contador sea 2, se ejecuta
            print(f"Procesamiento {contador} completado")
            contador = contador + 1
            cond.notify_all()

def empaque():
    global contador
    for _ in range(5):
        with cond:
            cond.wait_for(lambda: contador == 3) #Cuando el contador sea 3, se ejecuta
            print(f"Empaque {contador} completado")
            contador = 1  # Reinicia el contador para el siguiente ciclo
            cond.notify_all()


t1 = threading.Thread(target=preparacion)
t2 = threading.Thread(target=procesamiento)
t3 = threading.Thread(target=empaque)
t1.start()
t2.start()
t3.start()


with cond:
    cond.notify()

t1.join()
t2.join()
t3.join()
