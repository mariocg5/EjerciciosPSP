import threading

lock=threading.Lock()

def esPrimo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def primosEncontrados(rango):
    primos_encontrados =[]
    for numero in rango:
        if esPrimo(numero):
            primos_encontrados.append(numero)
    with lock:
            print(f"Primos encontrados en el rango {rango[0]} ----- {rango[-1]} =  {primos_encontrados}")

num=int(input("Introduce un número:"))

rangoTotal= range(num, 10000)
numHilos = 10
primosPorHilo = len(rangoTotal) // numHilos

hilos=[]

for i in range(numHilos):
    inicio = i*primosPorHilo
    if i<numHilos-1:
        fin = (i+1) * primosPorHilo
    else:
        fin = len(rangoTotal)
    rango=rangoTotal[inicio:fin]
    hilo = threading.Thread(target=primosEncontrados, args=(rango,))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()