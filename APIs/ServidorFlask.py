

from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios =[ {"id":1, "nombre":"Pepe", "edad":25}, {"id":2, "nombre":"Ana", "edad":30}]

@app.route('/')
def home():
    """ruta principal de la API. Cuando el usuario accede a esta ruta se le muestra el mensaje de bienvenida"""
    return "Bienvenido a la API de usuarios en local"

@app.route('/api/usuarios',methods=['GET'])
def obtener_usuarios():
    """Este endpoint devuelve la lista completa de usuarios almacenados en la base de datos simulaada"""
    return jsonify(usuarios)

@app.route('/api/usuarios/<int:usuario_id>',methods=['GET'])
def obtener_usuarios_por_id(usuario_id):
    """Este endpoint busca a un usuario especifico por su ID, si lo encuentra devolverá el usuario, si no, devuelve NONE"""
    usuario=next((u for u in usuarios if u["id"]==usuario_id),None)
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"Error", "Usuario no encontrado"}), 404

@app.route('/api/usuarios/<int:usuario_id>',methods=['PUT'])
def actualizar_usuario(usuario_id):
    """Este endpoint permite actualizar los datos de los usuarios a partir de un JSON enviado por el cliente
    con los campos que se desean modificar"""
    usuario=next((u for u in usuarios if u["id"]==usuario_id),None)
    if usuario:
        datos=request.get_json() #Guardamos todos los datos del usuario que buscamos
        usuario["nombre"] = datos.get("nombre", usuario["nombre"]) #Actualizamos solo los campos del JSON
        usuario["edad"] = datos.get("edad", usuario["edad"])
        return jsonify(usuario)
    else:
        return jsonify({"Error", "Usuario no encontrado"}), 404

@app.route('/api/usuarios',methods=['POST'])
def crear_usuario():
    """Este endpoint permite agregar un nuevo usuario a la base de datos de datos.
    El cliente debe enviar los datos en un json"""
    datos = request.get_json()
    nuevo_usuario={
        "id" :len(usuarios)+1,
        "nombre":datos["nombre"],
        "edad":datos["edad"]
    }
    usuarios.append(nuevo_usuario)
    return jsonify(nuevo_usuario),201

@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    """Este endpoint permite eliminar a un usuario especifico por su ID"""
    global usuarios #Creamos una variable global
    usuarios = [u for u in usuarios if u["id"]!= usuario_id] #Almacenamos en una lista los clientes que no se han eliminado

    return jsonify({"mensaje": "Usuario eliminado"}), 200
if __name__ == '__main__':
    """
    Arranca el servidor Flask en el puerto 5000 con modo debug activado.
    Esto permite ver los errores y recargar automáticamente los cambios en el código.
    """
    app.run(debug=True, port=5000)  # Ejecuta el servidor en http://127.0.0.1:5000
