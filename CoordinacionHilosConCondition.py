import threading

contador=1
etapa=1
cond=threading.Condition()

def preparacion():
    global contador,etapa
    for _ in range(5):
        with cond:
            cond.wait_for(lambda: etapa==1)
            print(f"Preparación {contador} completada")
            etapa=2
            cond.notify_all()

def procesamiento():
    global contador,etapa
    for _ in range(5):
        with cond:
            cond.wait_for(lambda: etapa==2)
            print(f"Procesamiento {contador} completado")
            etapa = 3
            cond.notify_all()

def empaque():
    global contador,etapa
    for _ in range(5):
        with cond:
            cond.wait_for(lambda: etapa==3)
            print(f"Empaque {contador} completado")
            contador += 1 #Se avanza el contadorS
            etapa=1
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