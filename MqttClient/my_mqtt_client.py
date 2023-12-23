import cv2
import paho.mqtt.client as mqtt
from ClassModels.Configs.mqtt_config import MqttConfig
from threading import Thread

class MQTTClient:

    def __init__(self, config: MqttConfig):

        self.config = config
        self.client = mqtt.Client()
        self.sub_topics = self.config.sub_topics
        self.pub_topics = self.config.pub_topics
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.config.broker_address)
        self.thread = Thread(target=self.start_loop)

    def start_mqtt_client_thread(self):
        self.thread.start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # Subscribe to topics from the config
        for _, topic_name in self.sub_topics.items():
            self.client.subscribe(topic_name)  # Subscribe to the topic name

    def on_message(self, client, userdata, msg):
        print(f"Received message on {msg.topic}")
        #print(f"Payload: {msg.payload.decode('utf-8')}")

        # Check if the topic is 'ping'
        if msg.topic == self.sub_topics['test_ping'] and msg.payload.decode('utf-8') == "ping":

            print("Ping received, sending Pong...")
            self.publish_message(self.pub_topics['pong'], "pong")

        if msg.topic == self.sub_topics['test_image'] and msg.payload.decode('utf-8') == "image":
            self.publish_test_image()

    def publish_test_image(self):
        image_path = self.config.image_path
        try:
            # Read and encode the image
            image = cv2.resize(cv2.imread(image_path), (200, 200))
            if image is None:
                raise FileNotFoundError(f"Unable to read the image at {image_path}")

            _, jpeg_image = cv2.imencode('.jpeg', image)
            self.client.publish(self.pub_topics['test_image'], jpeg_image.tobytes())
            print(f"Image published to topic {self.pub_topics['test_image']}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def publish_message(self, topic, message):
        self.client.publish(topic, message, retain=False)

    def start_loop(self):
        self.client.loop_start()

    def stop_loop(self):
        self.client.loop_stop()

    def run(self):
        self.client.loop_forever()



