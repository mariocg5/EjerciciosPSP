
import requests
from config import API_KEY

ciudad = "Valladolid"
# URL de la API
url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"

# Realizamos una solicitud GET para obtener información de la API
response = requests.get(url)

# Imprimimos el código de estado de la respuesta
if response.status_code==200:
    print("Solicitud realizada con éxito")
    datos = response.json()

    temperatura = datos["main"]["temp"] - 273
    descripcion = datos["weather"][0]["description"]

    print(f"ciudad: {ciudad}")
    print(f"Temperatura: {temperatura}")
    print(f"Descripcion del cielo: {descripcion}")

else:
    print("No se ha podido realizar la solicitud")
