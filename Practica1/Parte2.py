import os
import sys


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

        buffer=os.read(fdPadreAHijo[0],80).decode("utf-8") #Leo el mensaje del padre
        mensajeHijo=buffer.upper() #Lo convierto a mayúsculas

        #3
        os.write(fdHijoAPadre[1],mensajeHijo.encode("utf-8")) #El hijo escribe el mensaje al padre

        os.close(fdPadreAHijo[0])
        os.close(fdHijoAPadre[1])


    else:
        #Codigo del proceso padre
        #1
        os.close(fdPadreAHijo[0]) #Cierro lectura del padre
        os.close(fdHijoAPadre[1]) #Cierro escriturad del hijo

        mensajePadre = "Hola, que tal. \n"
        os.write(fdPadreAHijo[1], mensajePadre.encode("utf-8")) #El padre escribe el mensaje
        os.close(fdPadreAHijo[1])#Cierro escritura

        #4
        buffer=os.read(fdHijoAPadre[0],80).decode("utf-8") #El padre lee el mensaje del hijo
        print(f"El padre recibe el mensaje del hijo: {buffer}")

        os.wait()

if __name__ == "__main__":
    main()


