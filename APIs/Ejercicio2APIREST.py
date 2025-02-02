import hashlib
import re
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
app = Flask(__name__)


#Configuracion de la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

class Usuario(db.Model): #Modelo de la tabla de usuarios
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Contraseña encriptada
    mensaje_usuario = db.Column(db.String(255), nullable=False, default="")

# Crear la base de datos y la tabla si no existen
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

    pass_encriptada = password.encode()
    pass_hash = generate_password_hash(pass_encriptada)

    if Usuario.query.filter_by(username=user).first():
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    nuevo_usuario= Usuario(username=user, password_hash = pass_hash, mensaje_usuario="")
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"Mensaje": f"Usuario {user} registrado correctamente"}), 201

if __name__ == '__main__':
    """
    Arranca el servidor Flask en el puerto 5000 con modo debug activado.
    Esto permite ver los errores y recargar automáticamente los cambios en el código.
    """
    app.run(debug=True, port=5000)  # Ejecuta el servidor en http://127.0.0.1:5000
