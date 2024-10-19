from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime
from mysql.connector import Error
import database as db
import bcrypt
import mqtt as mqtt

load_dotenv()

SECRET_KEY_TOKEN=os.getenv('SECRET_KEY_TOKEN')
app = Flask(__name__)



cursor = db.database.cursor()


# Alta de instalador

@app.route('/instalador', methods=['POST'])
def add_instalador():
    try:
        data = request.json
        nombre = data['nombre']
        mail = data['mail']
        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Formatear la fecha en el formato deseado
        fecha = fecha_actual.strftime('%Y-%m-%d')

        passutf = data['password'].encode('utf-8')
        password = bcrypt.hashpw(passutf, bcrypt.gensalt())  # Hashing the password
        
        query = 'SELECT * FROM instalador WHERE mail=%s'
        cursor.execute(query,(mail,))
        listainst = cursor.fetchall()


        if listainst:
            usuarios=listainst[0]
            print(usuarios)
            mensaje= "Instalador ya registrado"
            status = 400

        else:
                        
            query = "INSERT INTO instalador (nombre, mail, password, fecha_alta) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, mail, password, fecha))
            db.database.commit()
            mensa= {
                "nombre": nombre,
                "mail": mail
            }
            mensaje = str(mensa)
            status = 201

        return jsonify({"message": mensaje }), status

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


# Validar Instalador


@app.route('/instalador', methods=['GET'])
def val_instalador():
    try:
        data = request.json
        print(data)
        mail = data.get('mail')
        passres = data.get('password')
        print(passres)
 
        passutf = data['password'].encode('utf-8')
        print(passutf)
        query = 'SELECT nombre, mail, password FROM instalador WHERE mail=%s'
        cursor.execute(query,(mail,))
        validar = cursor.fetchall()
        print(validar)

        
        if validar:
                valpass=validar[0]
                print(valpass[2])
                if bcrypt.checkpw(passutf, valpass[2].encode('utf-8')):
                    mensa = {
                                    'info':{ "nombre":valpass[0],
                                            "mail":valpass[1]

                                    }
                            }
                    mensaje= jwt.encode(mensa, SECRET_KEY_TOKEN, algorithm='HS256')
                    status = 201
                else: 
                    mensaje="contraseña invalida"
                    status = 300

        else:
                mensaje="Usuario no valido"           
                status = 301
    
        return jsonify({"message": mensaje }), status

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


# Alta de barrio



@app.route('/barrio', methods=['POST'])
def add_barrio():
    try:
        headers=request.headers
        token=headers['token']
        data = request.json
        mail_inst = data['mail_inst']
        mail_admin = data['mail_admin']
        nom_barrio = data['nom_barrio']
        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Formatear la fecha en el formato deseado
        fecha = fecha_actual.strftime('%Y-%m-%d')

        query = 'SELECT * FROM barrios WHERE nombre=%s and mailadmin=%s'
        cursor.execute(query,(nom_barrio,mail_admin,))
        listabarrio = cursor.fetchall()

        if listabarrio:

            print("Barrio ya existe")
            mensaje= "barrio ya existe"
            status = 400

        else:

            query = 'SELECT nombre,mail FROM instalador WHERE mail=%s'
            cursor.execute(query,(mail_inst,))
            datosinst = cursor.fetchall()
            datos=datosinst[0]
            mensa = {
                            'info':{ "nombre":datosinst[0][0],
                                    "mail":datosinst[0][1]

                            }
                    }
            mensaje= jwt.encode(mensa, SECRET_KEY_TOKEN, algorithm='HS256')

            if token==mensaje:
                query = "INSERT INTO barrios (nombre, mailadmin, mailinst, fecha_alta) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nom_barrio, mail_admin, mail_inst, fecha))
                db.database.commit()
                mensa= {
                    "nom_barrio": nom_barrio,
                    "mail_admin": mail_admin,
                    "fecha_alta": fecha
                }
                mensaje = str(mensa)
                status = 201


            else:
                mensaje = "Token no valido"
                status = 300            
            


        return jsonify({"message": mensaje }), status

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
    nombre = data['nombre']
    mail = data['mail']
    password = data['password']
    passutf = data['password'].encode('utf-8')
    password = bcrypt.hashpw(passutf, bcrypt.gensalt())  # Hashing the password
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%Y-%m-%d')
    query = 'SELECT * FROM usuarios WHERE mail=%s'
    cursor.execute(query,(mail,))
    listausuarios = cursor.fetchall()


    if listausuarios:
        mensaje= "usuario existente"
        status = 300

    else:
        query = "INSERT INTO usuarios (nombre, mail, password, fecha_alta) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, mail, password, fecha))
        db.database.commit()
        mensa= {
            "nombre": nombre,
            "mail": mail,
            "fecha_alta": fecha
        }
        mensaje = str(mensa)
        status = 201
    

    return jsonify({"message": mensaje }), status

#Validar usuario

@app.route('/valusuario', methods=['GET'])
def val_usuario():
    data = request.json
    mail = data.get('mail')
    passres = data.get('password')
    passutf = passres.encode('utf-8')

 
    query = "SELECT nombre, mail,password FROM usuarios WHERE mail=%s"
    cursor.execute(query, (mail,))
    validar=cursor.fetchall()
 
    if validar:
        valpass=validar[0]
        if bcrypt.checkpw(passutf, valpass[2].encode('utf-8')):
            mensaje="contraseña valida"
            crea_token={
                "info":{
                    "nombre":valpass[0],
                    "mail":valpass[1]
                }
            }
            mensaje= jwt.encode(crea_token, SECRET_KEY_TOKEN, algorithm='HS256')
            status=200

        else: 
            status=300
            mensaje="contraseña invalida"

    else:
        status=300
        mensaje="Usuario no valido"           
    
    return jsonify({"message": mensaje }), status




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