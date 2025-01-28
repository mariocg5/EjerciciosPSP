#~Escribe un programa que solicite al usuario un nombre de usuario y contraseña.
# Valida que el nombre no contenga caracteres peligrosos (por ejemplo, ;, --, <, >).

repetir = True
usuario = "Mario"
password = "mario1234"
caracteresPeligrosos= [":","-",">","<"]

while repetir:
   user= input("Introduce un nombre de usuario")
   passwd= input("Introduce una contraseña: ")
   if any(letra in user for letra in caracteresPeligrosos ):
       print("El nombre contiene caracteres peligrosos")
   else:
       if user == usuario and passwd == password:
           print("Login correcto")
           repetir=False
       else:
           print("Login incorrecto")



