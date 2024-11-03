import os
import sys
from pathlib import Path

#He comprobado que funciona en replit.com

def main():
    fdPadreAHijo=os.pipe()
    fdHijoAPadre=os.pipe()
    pid=os.fork()

    if pid < 0:
        print("No se ha podido crear el proceso hijo")
        sys.exit(1)

    elif pid==0:
        #Codigo del proceso hijo
        #2
        os.close(fdPadreAHijo[1]) #Cierro escritura en el padre
        os.close(fdHijoAPadre[0]) #Cierro lectura del hijo

        buffer=os.read(fdPadreAHijo[0],1024).decode("utf-8") #Leo el mensaje del padre

        #3
        lineas=buffer.splitlines()
        numLineas=len(lineas)
        num_palabras=sum(len(linea.split() for linea in lineas))

        mensajeHijo=f"Número de lineas del archivo: {numLineas}, número de palabras: {num_palabras}"
        os.write(fdHijoAPadre[1],mensajeHijo.encode("utf-8")) #El hijo escribe el mensaje al padre

        os.close(fdPadreAHijo[0])
        os.close(fdHijoAPadre[1])


    else:
        #Codigo del proceso padre
        #1
        os.close(fdPadreAHijo[0]) #Cierro lectura del padre
        os.close(fdHijoAPadre[1]) #Cierro escriturad del hijo

        archivoNuevo= Path("archivo.txt")
        if archivoNuevo.exists():
            archivo=archivoNuevo.read_text() #Metodo para leer el archivo
            os.write(fdPadreAHijo[1], archivo.encode("utf-8")) #El padre escribe el mensaje
            os.close(fdPadreAHijo[1])#Cierro escritura
        else:
            print("El archivo no existe")


        #4
        buffer=os.read(fdHijoAPadre[0],1024).decode("utf-8") #El padre lee el mensaje del hijo
        print(f"El padre recibe el mensaje del hijo que ha contado las líneas y las palabras del archivo: {buffer}")
        os.close(fdHijoAPadre[0])

        os.wait()

if __name__ == "__main__":
    main()


