import paho.mqtt.client as mqtt
from app.config import BROKER_ADDRESS, IMAGE_TOPIC, DETECTION_TOPIC, PING_TOPIC
# Configuration



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(PING_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message}")

    # If we receive "ping", respond with "pong"
    if message == "ping":
        client.publish(PING_TOPIC, "pong")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()
