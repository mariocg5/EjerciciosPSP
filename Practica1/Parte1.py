import psutil


def listarProcesos():
    try:
        procesos_encontrados = []
        procesos_no_encontrados = []

        proceso_nombres = input("Ingresa el nombre de un proceso separado por comas: ").split(',') #separado por comas
        proceso_nombres = [nombre.strip() for nombre in proceso_nombres]  # quito espacios en blanco

        for nombre in proceso_nombres:
            encontrado = False
            for proceso in psutil.process_iter():
                if proceso.name() == nombre:
                    encontrado = True
                    memoria_proceso = proceso.memory_info()
                    memoriaVirtual = memoria_proceso.vms / (1024 * 1024)
                    memoriaFisica = memoria_proceso.rss / (1024 * 1024)

                    procesos_encontrados.append((proceso.name(), proceso.pid, memoriaFisica, memoriaVirtual))

            if not encontrado:
                procesos_no_encontrados.append(nombre)

        if procesos_no_encontrados:
            print("Los siguientes procesos no están en ejecución:")
            for nombre in procesos_no_encontrados:
                print(f"Nombre: {nombre}")

        if procesos_encontrados:
            i=1
            print("Los procesos en ejecución son:")
            for nombre, pid, memFisica, memVirtual in procesos_encontrados:
                print(
                    f"{i} Nombre: {nombre}, PID: {pid}, Memoria Física: {memFisica} MB, Memoria Virtual: {memVirtual} MB")
                i=i+1

            procesoFinalizar = int(input("Ingresa el numero del proceso en ejecución que quieres finalizar "))
            if procesoFinalizar <= 0 or procesoFinalizar > len(procesos_encontrados):
                print("EL número de proceso que has introducido no es válido")
            else:
                procFin = procesos_encontrados[procesoFinalizar - 1][1]  # pongo el 1 ya que el metodo psutil necesita la referencia del PID para poder eliminarlo
                procFinNombre = procesos_encontrados[procesoFinalizar - 1][0] #el 0 de la tupla es la referencia al nombre
                proceso = psutil.Process(procFin)
                proceso.terminate()
                proceso.wait()
                print(f"El proceso con nombre {procFinNombre} y PID {procFin} se ha finalizado")

    except psutil.NoSuchProcess:
        print("El proceso con ese PID no existe.")
    except psutil.AccessDenied:
        print("No se tiene el permiso para acceder a este proceso.")
    except Exception as e:
        print(f"Error: {e}")


listarProcesos()
