import subprocess
import time
import win32clipboard

def comprobarPortapapeles(tiempo):
    print("Se verificará durante 30 segundos si el contenido del portapapeles cambia")
    ultimoContenido=None
    comprobar = True
    tiempoInicio=time.time()
    while comprobar:
        win32clipboard.OpenClipboard()
        try:
            contenidoActual=win32clipboard.GetClipboardData()
            if ultimoContenido != contenidoActual:
                print("El contenido del portapapeles ha cambiado: ")
                print(contenidoActual)
                ultimoContenido=contenidoActual
            else:
                print("No se ha cambiado nada")
        except Exception as e:
            print("Error al acceder al portapapeles:", e)
        finally:
            win32clipboard.CloseClipboard()
        time.sleep(5) #Tiempo que pasa entre comprobaciones
        if time.time() - tiempoInicio > tiempo:
            print("Tiempo límite alcanzado. Saliendo del programa.")
            comprobar=False

def copiarPortapapeles():
    p1 = subprocess.Popen('ftp', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    comandos = [b"verbose\n",
                b"open test.rebex.net\n",
                b"demo\n",
                b"password\n",
                b"ls\n",
                b"get readme.txt\n"]

    for cmd in comandos:
        p1.stdin.write(cmd)

    respuesta = p1.communicate(timeout=5)[0]

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(respuesta)
    win32clipboard.CloseClipboard()\

    win32clipboard.OpenClipboard()
    datos = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    print("El contenido del portapapeles es: " + datos)
    comprobarPortapapeles(30) #Durante 30 segundos se ejecuta el metodo, después, se cierra automáticamente
def main():
    copiarPortapapeles()

if __name__ == "__main__":
    main()