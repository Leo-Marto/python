from flask import Flask, request, jsonify
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

hostenv = os.getenv('HOST_DB')
userenv = os.getenv('USER_DB')
passwordenv = os.getenv('PASS_DB')
databaseenv = os.getenv('DATABASE_DB')

print(hostenv)
print(userenv)
print(passwordenv)
print(databaseenv)

app = Flask(__name__)

db = mysql.connector.connect(
    host=hostenv,  # Cambiar según tu configuración
    user=userenv,       # Cambiar según tu usuario de MySQL
    password=passwordenv,       # Cambiar según tu password de MySQL
    database=databaseenv  # Base de datos que creaste
)

cursor = db.cursor()

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    usuario = data['usuario']
    mail = data['mail']
    password = data['password']

    query = "INSERT INTO usuarios (usuario, mail, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (usuario, mail, password))
    db.commit()

    return jsonify({"message": "Usuario agregado exitosamente"}), 201


# Ruta para obtener todos los usuarios (READ)
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario[0],
            "usuario": usuario[1],
            "mail": usuario[2],
            "password": usuario[3]  # Evitar enviar contraseñas en respuestas reales
        })

    return jsonify(result), 200

# Ruta para actualizar un usuario (UPDATE)
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.json
    print(data)
    usuario = data.get('usuario')
    mail = data.get('mail')
    password = data.get('password')

    query = "UPDATE usuarios SET usuario=%s, mail=%s, password=%s WHERE id=%s"
    cursor.execute(query, (usuario, mail, password, id))
    db.commit()

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200


# Ruta para eliminar un usuario (DELETE)
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    query = "DELETE FROM usuarios WHERE id=%s"
    cursor.execute(query, (id,))
    db.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200


if __name__ == '__main__':
    app.run(debug=True)