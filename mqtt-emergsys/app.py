from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
import database as db
import bcrypt
import mqtt as mqtt

load_dotenv()


app = Flask(__name__)



cursor = db.database.cursor()


# Alta de instalador

@app.route('/inst', methods=['POST'])
def add_instalador():
    try:
        data = request.json
        nombre = data['nombre']
        mail = data['mail']
        passutf = data['password'].encode('utf-8')
        password = bcrypt.hashpw(passutf, bcrypt.gensalt())  # Hashing the password
        query = "INSERT INTO instalador (nombre, mail, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, mail, password))
        db.database.commit()
        mensa= {
            "nombre": nombre,
            "mail": mail
        }
        mensaje = str(mensa)
        status = 201
        mqtt.mqtt_client.publish("test/topic", mensaje)

        return jsonify(mensaje), status

    except Error as e:
        # Handle MySQL errors
        db.rollback()  # Undo changes if an error occurs
        print(f"Database error: {e}")
        return jsonify({"error": "Database error occurred"}), 500

    except KeyError as e:
        # Handle missing keys in the JSON data
        print(f"Key error: {e}")
        return jsonify({"error": f"Missing key: {str(e)}"}), 400

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        if 'cursor' in locals():  # Check if cursor exists before closing
            cursor.close()  # Close the cursor if it was created





@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    usuario = data['usuario']
    mail = data['mail']
    direccion = data['direccion']
    telefono = data['telefono']
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
        query = "INSERT INTO usuarios (usuario, mail, password, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (usuario, mail, password, direccion, telefono))
        db.database.commit()
        mensa= {
            "usuario": usuario,
            "mail": mail,
            "password": password,
            "direccion": direccion,
            "telefono": telefono
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
            mensaje="contraseña invalida"

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
            "password": usuario[3], 
            "direccion": usuario[4], 
            "telefono": usuario[5] 
        })

    return jsonify(result), 200

# Ruta para actualizar un usuario (UPDATE)
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.json
    print(data)
    usuario = data.get('usuario')
    mail = data.get('mail')
    direccion = data.get('direccion')
    telefono = data.get('telefono')
    passutf = data.get('password').encode('utf-8')
    password = bcrypt.hashpw(passutf, bcrypt.gensalt())  # Hashing the password
    query = "UPDATE usuarios SET usuario=%s, mail=%s, password=%s, direccion=%s, telefono=%s WHERE id=%s"
    cursor.execute(query, (usuario, mail, password, direccion, telefono, id))
    db.database.commit()

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200


# Ruta para eliminar un usuario (DELETE)
@app.route('/usuarios/<string:mail>', methods=['DELETE'])
def delete_usuario(mail):
    #data = request.json
    print(mail)

    query = "SELECT id FROM usuarios WHERE mail=%s"
    cursor.execute(query, (mail,))
    validar=cursor.fetchall()
    if validar:
        query = "DELETE FROM usuarios WHERE mail=%s"
        cursor.execute(query, (mail,))
        db.database.commit()
        mensaje= "Usuario eliminado"
    else:
        mensaje= "Usuario inexistente"

    return jsonify({"message": mensaje }), 200


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, port=8082)