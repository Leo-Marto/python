import paho.mqtt.client as mqtt
import database as db


mqtt_broker = "icuadrado.net"
mqtt_port = 1883
mqtt_username = "UsuarioSOS"
mqtt_password = "SOS2020"
mqtt_topic = "test/topic"

cursor = db.database.cursor()

# Definir lo que sucede cuando te conectas al broker MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con código: {rc}")
    # Suscribirse a un tópico específico
    client.subscribe("tu/topico")
    client.subscribe("altaplacas")

# Definir lo que sucede cuando llega un mensaje al tópico suscrito
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

    altaplacas(msg.payload.decode())

def altaplacas(mac):
    # Suponiendo que cursor y db están inicializados globalmente
    query = 'SELECT * FROM placas WHERE mac=%s'
    cursor.execute(query, (mac,))
    busquedaplaca = cursor.fetchall()

    if busquedaplaca:
        placas = busquedaplaca[0][0]  # Accede al valor específico si es necesario
        print(str(placas) + " ya está cargada en el sistema")


    else:
        query = "INSERT INTO placas (mac) VALUES (%s)"
        cursor.execute(query, (mac,))
        db.database.commit()



# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configurar las funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker MQTT
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port,)
# Iniciar el bucle que escucha de forma continua los mensajes del broker
client.loop_forever()