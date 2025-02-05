import datetime
import os
import re
from crypt import methods

from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash  # Con esta libreria evito el salting
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request



app = Flask(__name__)

#Configuracion de la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

if not os.path.exists("secret.key"): # Creo un archivo donde guardo mi key que aunque se genera en los archivos del proyecto, posteriormente la guardaría en mi gitIgnore
    with open("secret.key", "wb") as key_file:
        key_file.write(Fernet.generate_key())

with open("secret.key", "rb") as key_file:
    SECRET_KEY = key_file.read()

fernet = Fernet(SECRET_KEY)

class Usuario(db.Model): #Modelo de la tabla de usuarios
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Contraseña encriptada
    intentos_fallidos = db.Column(db.Integer, default=0)  # Intentos de login fallidos
    bloqueado_hasta = db.Column(db.DateTime, nullable=True)  # Fecha de desbloqueo


class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remitente = db.Column(db.String(20), nullable=False)
    destinatario = db.Column(db.String(20), nullable=False)
    mensaje_cifrado = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Bienvenido a la API de gestión de mensajes"

@app.route('/api/usuarios/register', methods=['POST'])
def registrar_usuarios():
    datos = request.json
    if "usuario" not in datos or "password" not in datos: #Compruebo que el json tiene el usuario y la contraseña
        return jsonify({"error": "Los campos requeridos no se están pasando correctamente"}), 400

    user=datos["usuario"]
    password = datos["password"]

    if len (user) > 10 or len(user) < 3:
        return jsonify({"error": "El nombre de usuario debe tener entre 3 y 10 caracteres"}), 400
    if not re.match(PASSWORD_REGEX, password):
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial" }), 400

    pass_hash = generate_password_hash(password) #Genero un contraseña segura

    if Usuario.query.filter_by(username=user).first(): #Hace una búsqueda por usuario, si lo encuentra, es que ya está registrado
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    nuevo_usuario= Usuario(username=user, password_hash = pass_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"Mensaje": f"Usuario {user} registrado correctamente"}), 201

@app.route ('/api/usuarios/<string:nombre_usuario>', methods=['PUT'])
def actualizar_usuarios(nombre_usuario):
    datos = request.json
    if "usuario" not in datos:
        return jsonify(
            {"Error": "Los campos requeridos para el login del usuario no se están pasando correctamente"}), 400
    user=datos["usuario"]
    usuario= Usuario.query.filter_by(username=nombre_usuario).first()
    if not usuario:
        return jsonify({"Error": "Usuario no encontrado en la base de datos"}), 404

    usuario_existente = Usuario.query.filter_by(username=user).first()
    if usuario_existente:
        return jsonify({"Error" : "El usuario ya existe con ese nombre en la base de datos"})
    usuario.username = user
    db.session.commit()
    return jsonify({"message": f"El nombre de usuario ha sido actualizado a {user}"}), 200

@app.route ('/api/usuarios/<string:nombre_usuario>', methods=['DELETE'])
def borrar_usuarios(nombre_usuario):
    usuario = Usuario.query.filter_by(username=nombre_usuario).first()

    if not usuario:
        return jsonify({"Error": "Usuario no encontrado en la base de datos"}), 404

    db.session.delete(usuario)
    db.session.commit()

@app.route ('/api/usuarios/login', methods=['POST'])
def autenticar_usuarios():
    datos = request.json

    if "usuario" not in datos or "password" not in datos:
        return jsonify({"Error" : "Los campos requeridos para el login del usuario no se están pasando correctamente"}),400

    user=datos["usuario"]
    password=datos["password"]

    if len (user) > 10 or len(user)<3 :
        return jsonify({"Error":"El nombre del usuario debe tener entre 3 y 10 caracteres"}),400
    if not re.match(PASSWORD_REGEX,password):
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial" }), 400

    usuario= Usuario.query.filter_by(username=user).first() #Busco el nombre del usuario en la base de datos

    if not usuario:
        return jsonify({"Error" : "Usuario no encontrado en la base de datos"}),404

    if usuario.bloqueado_hasta:
        ahora = datetime.datetime.now()
        if ahora < usuario.bloqueado_hasta:
            return jsonify({"error": "Cuenta bloqueada, intente más tarde"}), 403
        else:
            #Desbloquear usuario si el tiempo ha pasado
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = None
            db.session.commit()

    if not check_password_hash(usuario.password_hash, password):
        usuario.intentos_fallidos +=1

        if usuario.intentos_fallidos > 3:
            usuario.bloqueado_hasta = datetime.datetime.now() + datetime.timedelta(minutes=5)
            db.session.commit()
            return jsonify({"Error": "Demasiados intentos fallidos, cuenta bloqueada 5 minutos"}), 401

        db.session.commit()
        return jsonify({"Error" : f"Contraseña incorrecta. Intentos restantes: {3-usuario.intentos_fallidos}"}),401

    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    db.session.commit()

    return jsonify({"Mensaje" : "Inicio de sesión correcto" }),200

@app.route("/api/usuarios/listar", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()

    if not usuarios:
        return jsonify({"Mensaje": "No hay usuarios registrados"}), 404

    usuarios_lista = []
    for usuario in usuarios:
        usuarios_lista.append({
            "id": usuario.id,
            "usuario": usuario.username,
        })

    return jsonify({"usuarios": usuarios_lista}), 200

@app.route("/api/usuarios/send", methods=["POST"])
def enviar_mensaje():
    datos = request.json

    if "remitente" not in datos or "destinatario" not in datos or "mensaje" not in datos:
        return jsonify({"Error": "Faltan datos requeridos (remitente, destinatario, mensaje)"}), 400

    remitente = datos["remitente"]
    destinatario = datos["destinatario"]
    mensaje = datos["mensaje"]

    usuario_remitente = Usuario.query.filter_by(username=remitente).first()
    usuario_destinatario = Usuario.query.filter_by(username=destinatario).first()

    if not usuario_remitente:
        return jsonify({"Error": f"El usuario remitente '{remitente}' no existe"}), 404
    if not usuario_destinatario:
        return jsonify({"Error": f"El usuario destinatario '{destinatario}' no existe"}), 404

    #Cifrar el mensaje
    mensaje_cifrado = fernet.encrypt(mensaje.encode()).decode()

    #Guardar en la tabla `Mensaje`
    nuevo_mensaje = Mensaje(remitente=remitente, destinatario=destinatario, mensaje_cifrado=mensaje_cifrado)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    return jsonify({"Mensaje": f"Mensaje enviado correctamente de {remitente} a {destinatario}"}), 200

@app.route("/api/usuarios/messages/<string:user>", methods=["GET"])
def recibir_mensaje(user): #Meto en la ruta el nombre del usuario que recibe el mensaje
    usuario = Usuario.query.filter_by(username=user).first()

    if not usuario:
        return jsonify({"Error": "Usuario no encontrado"}), 404

    mensajes = Mensaje.query.filter_by(destinatario=user).all()

    if not mensajes:
        return jsonify({"Mensaje": "No tienes mensajes nuevos"}), 200

    mensajes_lista = []
    for mensaje in mensajes:
        mensaje_desencriptado = fernet.decrypt(mensaje.mensaje_cifrado.encode()).decode()
        mensajes_lista.append({
            "remitente": mensaje.remitente,
            "mensaje": mensaje_desencriptado
        })

    for mensaje in mensajes: # Borrar mensajes después de leerlos
        db.session.delete(mensaje)
    db.session.commit()

    return jsonify({"mensajes": mensajes_lista}), 200

if __name__ == '__main__':
    """
    Arranca el servidor Flask en el puerto 5000 con modo debug activado.
    Esto permite ver los errores y recargar automáticamente los cambios en el código.
    """
    app.run(debug=True, port=5000)  # Ejecuta el servidor en http://127.0.0.1:5000
