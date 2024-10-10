from flask import Flask, request, jsonify
from dotenv import load_dotenv
import database as db
import bcrypt
import mqtt as mqtt

load_dotenv()


app = Flask(__name__)



cursor = db.database.cursor()



@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    usuario = data['usuario']
    mail = data['mail']
    passutf = data['password'].encode('utf-8')
    password = bcrypt.hashpw(passutf, bcrypt.gensalt())  # Hashing the password
    query = 'SELECT * FROM usuarios WHERE mail=%s'
    cursor.execute(query,(mail,))
    listausuarios = cursor.fetchall()


    if listausuarios:
        usuarios=listausuarios[0]
        print(usuarios)
        mensaje= str(usuarios)
        status = 304
        mqtt.mqtt_client.publish("test/topic", mensaje)

    else:
        query = "INSERT INTO usuarios (usuario, mail, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (usuario, mail, password))
        db.database.commit()
        mensa= {
            "usuario": usuario,
            "mail": mail,
            "password": password
        }
        mensaje = str(mensa)
        status = 201
        mqtt.mqtt_client.publish("test/topic", mensaje)
    

    return jsonify(mensaje), status

#Validar usuario

@app.route('/validar', methods=['GET'])
def val_usuario():
    data = request.json
    print(data)
    mail = data.get('mail')
    passres = data.get('password')
    print(passres)
    passutf = passres.encode('utf-8')
    print(passutf)

 
    query = "SELECT password FROM usuarios WHERE mail=%s"
    cursor.execute(query, (mail,))
    validar=cursor.fetchall()
 
    if validar:
        valpass=validar[0]
        print(valpass[0])
        if bcrypt.checkpw(passutf, valpass[0].encode('utf-8')):
            mensaje="contraseña valida"
    else:
        mensaje="Usuario no valido"           
    
    return jsonify({"message": mensaje }), 200




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
    passutf = data.get('password').encode('utf-8')
    password = bcrypt.hashpw(passutf, bcrypt.gensalt())  # Hashing the password
    query = "UPDATE usuarios SET usuario=%s, mail=%s, password=%s WHERE id=%s"
    cursor.execute(query, (usuario, mail, password, id))
    db.database.commit()

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200


# Ruta para eliminar un usuario (DELETE)
@app.route('/usuarios/<string:mail>', methods=['DELETE'])
def delete_usuario(mail):
    #data = request.json
    print(mail)
    query = "DELETE FROM usuarios WHERE mail=%s"
    cursor.execute(query, (mail,))
    db.database.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, port=8082)