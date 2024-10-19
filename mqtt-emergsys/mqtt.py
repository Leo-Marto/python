import paho.mqtt.client as mqtt

# MQTT Setup
mqtt_broker = "icuadrado.net"
mqtt_port = 1883
mqtt_username = "UsuarioSOS"
mqtt_password = "SOS2020"
mqtt_topic = "test/topic"

# Create a new MQTT client instance
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt=mqtt_client.connect(mqtt_broker, mqtt_port,)
mqtt_client.publish(mqtt_topic, "app iniciada")

# Callback when the MQTT client receives a message
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

def mqtt_subscribe():
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_broker, mqtt_port,)
    mqtt_client.subscribe(mqtt_topic)
    mqtt_client.loop_forever()  # Run the MQTT client in a blocking loop




