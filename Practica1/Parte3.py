import asyncio
import subprocess
import time
from os import system


def NotepadSincrono ():
    tiempoInicio=time.time()
    try:
        subprocess.run(['Notepad.exe', ])
    except subprocess.CalledProcessError as e:
        print(e.output)
    tiempoTotal=time.time() - tiempoInicio
    print(f"Tiempo de ejecución Síncrona: {tiempoTotal} segundos") #Entiendo que este mensaje se deberia de mostrar tras cerrar el Notepad pero me sale nada más se ejecuta el proceso

async def NotepadAsincrono():
    tiempoInicio = time.time()
    try:
        await asyncio.create_subprocess_exec('Notepad.exe')
    except subprocess.CalledProcessError as e:
        print(e.output)
    tiempoTotal = time.time() - tiempoInicio
    print(f"Tiempo de ejecución Asíncrona: {tiempoTotal} segundos")

async def main():
        print("1. Ejecutar Notepad de manera sincrona ")
        print("2. Ejecutar Notepad de manera asíncrona")

        opcion= input("Introduce un numero para realizar una de las ejecuciones")
        if opcion=='1':
            NotepadSincrono()
        elif opcion=='2':
            await NotepadAsincrono()
            system('Pause')
        else:
            print("La opción introducida no es válida")

asyncio.run(main())
