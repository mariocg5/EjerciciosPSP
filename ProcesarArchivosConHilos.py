import threading
import time



class ProcesadorArchivo(threading.Thread):
    def __init__(self, nombre, numLineas):
        super().__init__()
        self.nombre = nombre
        self.numLineas = numLineas

    def run(self):
        """Este método se ejecuta al iniciar el hilo."""
        for i in range(1, self.numLineas+1):
            print(f"Procesando {self.nombre} - Línea {i}")
            time.sleep(1)

archivo1 = "Hola \n hola \nHola \n hola"
archivo2 = "Hola \n hola \nHola"
archivo3 = "Hola \n hola \nHola \n hola"
archivo4 = "Hola \n hola \nHola \n hola \nHola \n hola"
archivo5 = "Hola \n hola \nHola "

listaArchivos = [(archivo1, "archivo1"), (archivo2, "archivo2"),(archivo3, "archivo3"),
                 (archivo4, "archivo4"),(archivo5, "archivo5")
]

hilos = []

for contenido, nombre in listaArchivos:
    numLineas = contenido.count('\n') + 1 #Cada vez que se encuentre un salto de linea lo cuenta y se suma 1 porque después del último salto de linea hay una última linea
    hilo = ProcesadorArchivo(nombre=nombre, numLineas=numLineas)
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

print("Todos los archivos han sido procesados.")
