import psutil

def listarProcesos():
    try:
        encontrado = False
        procesos = []
        notepad_proceso=None
        for proceso in psutil.process_iter():
            nombreProceso=proceso.name()
            IDproceso=proceso.pid

            if nombreProceso=='Notepad.exe':
                encontrado=True
                notepad_proceso=(nombreProceso,IDproceso)
            else:
                procesos.append((nombreProceso,IDproceso))

        for proc in procesos:
            print(proc[0], '-----', proc[1])

        if encontrado:
            print("El proceso Notepad está en ejecución")
            print(notepad_proceso[0], '----', notepad_proceso[1])
        else:
            print('El proceso Notepad no está en ejecución')


    except Exception as e:
        print(f"Error: {e}")

def finalizarProceso():
    encontrado=False
    procesoEncontrado=None
    try:
        pid_user=int(input("Ingresa el PID de un proceso que deseé terminar"))

        for proceso in psutil.process_iter():
            if pid_user==proceso.pid:
                encontrado=True
                procesoEncontrado = proceso

        if encontrado:
            print(f"Proceso encontrado: {procesoEncontrado.name()} ´con PID:  {procesoEncontrado.pid}")
            procesoEncontrado.terminate()
            print("El proceso se ha eliminado")
        else:
            print(f"El proceso con PID: {pid_user} no se ha encontrado")

    except psutil.NoSuchProcess:
        print("El proceso con ese PID no existe.")
    except psutil.AccessDenied:
        print("No se tiene el permiso para finalizar este proceso.")
    except Exception as e:
        print(f"Error: {e}")

def usoMemoriayCPU():
    try:
        for proceso in psutil.process_iter():
            try:
                IDproceso = proceso.pid
                nombreProceso=proceso.name()
                cpu=proceso.cpu_percent(interval=1)
                memoria = proceso.memory_info()
                #Al llamar a .memory_info nos da muchos atributos, en este caso solo nos interesarían la rss y la vms
                rss = memoria.rss/(1024*1024) #memoria física pasada a MB
                vms = memoria.vms/(1024*1024) #memoria virtual pasada a MB

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): #Ignoro los procesos a los que no puedo acceder
                continue
            print(f"Nombre: {nombreProceso}, PID: {IDproceso}, uso de CPU: {cpu}%, uso de memoria: {rss} MB de Memoria física, {vms} MB de Memoria virtual")

    except Exception as e:
        print(f"Error: {e}")


def main():
    continuar=True
    while continuar:
        print("-----MENÚ-----: ")
        print("1. Listar procesos ")
        print("2. Finalizar un proceso")
        print("3. Conocer el uso de CPU y memoria de cada proceso")
        print("4. Para salir")

        opcion=input("Elige entre estas 3 opciones: ")

        if opcion=='1':
            listarProcesos()
        elif opcion=='2':
            finalizarProceso()
        elif opcion=='3':
            usoMemoriayCPU()
        elif opcion=='4':
            print("Adiós")
            continuar=False
        else:
            print("Por favor, ingrese un número válido")


if __name__=="__main__":
    main()

