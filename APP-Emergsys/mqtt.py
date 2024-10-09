import paho.mqtt.client as mqtt

# MQTT Broker information
broker = "icuadrado.net"  # Use your broker URL or IP
port = 1883
topic = "test/topic"
username = "UsuarioSOS"
password = "SOS2020"

# Create a new MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(username, password)

# Connect to the broker
client.connect(broker, port)

# Publish a message to the topic
message = "Hola desde python!"
client.publish(topic, message)

# Disconnect from the broker
client.disconnect()

print(f"Published message: '{message}' to topic '{topic}' with authentication.")