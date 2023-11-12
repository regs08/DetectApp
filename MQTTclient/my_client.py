import paho.mqtt.client as mqtt
from app.config import BROKER_ADDRESS, IMAGE_TOPIC, DETECTION_TOPIC, PING_TOPIC
# Configuration
from MQTTclient.mqtt_config import MQTTConfig

client_config = MQTTConfig(broker_address=BROKER_ADDRESS, topics={'ping': PING_TOPIC})

class MqttClient:

    def __init__(self, mqtt_config):
        self.broker_address = mqtt_config.broker_address
        self.client = mqtt.Client(self.broker_address)
        self.topics = mqtt_config.topics
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        for topic in self.topics:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        # Check if the message is a ping message
        if msg.topic == self.topics['ping']:
            message = msg.payload.decode()

            self.on_ping(message)

    def on_ping(self, message):
        # message = msg.payload.decode()
        print(f"Received ping message: {message}")

        # If we receive "ping", respond with "pong"
        if message == "ping":
            self.client.publish(PING_TOPIC, "pong")

    def loop(self):
        self.client.loop_forever()



client = MqttClient(client_config)

# Set the callbacks
client.client.on_connect = client.on_connect
client.client.on_message = client.on_message

# Connect to the MQTT broker
client.client.connect(client.broker_address)

# Start the loop
client.loop()
