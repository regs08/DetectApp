import json
import time
from threading import Thread, Lock
from MqttClient.my_mqtt_client import MQTTClient


class PayloadSenderHandler:
    def __init__(self, mqtt_client: MQTTClient, send_interval=5):
        self.mqtt_client = mqtt_client
        self.pub_topics = self.mqtt_client.pub_topics
        self.payload_buffer = []
        self.frame_buffer = []
        self.last_payload_send_time = 0
        self.last_picture_send_time = 0
        self.send_interval = send_interval
        self.buffer_lock = Lock()  # Lock for thread safety

    def append_frame(self, frame):
        """
        appends the frame after one is sent out. Just using to test sending frames now
        :param frame:
        :return:
        """
        with self.buffer_lock:
            if len(self.frame_buffer) == 0:
                self.frame_buffer.append(frame)

    def append_payload(self, payload):
        with self.buffer_lock:
            self.payload_buffer.extend(payload)

    def send_payload(self):
        with self.buffer_lock:
            if self.payload_buffer:
                combined_payload = json.dumps(self.payload_buffer)
                self.mqtt_client.publish_message(topic=self.pub_topics['detection'],
                                                 message=combined_payload.encode('utf-8'))
                self.payload_buffer = []

    def send_picture(self):
        with self.buffer_lock:
            if self.frame_buffer:
                frame = self.frame_buffer.pop(0)  # Send the oldest picture

                self.mqtt_client.publish_message(topic=self.mqtt_client.pub_topics['image'], message=frame)

    def should_send_payload(self, current_time):
        return current_time - self.last_payload_send_time > self.send_interval

    def should_send_frame(self, current_time):
        return current_time - self.last_picture_send_time > self.send_interval

    def update_last_send_time(self, current_time):
        self.last_payload_send_time = current_time

    def update_last_frame_send_time(self, current_time):
        self.last_picture_send_time = current_time

    def start_payload_sender(self):
        """Starts a thread that sends payloads and pictures every 5 seconds."""
        def send_payloads_and_pictures():
            while True:
                current_time = time.time()
                if self.should_send_payload(current_time):
                    self.send_payload()
                    self.update_last_send_time(current_time)
                if self.should_send_frame(current_time):
                    print('sending frame.. ')
                    self.send_picture()
                    self.update_last_frame_send_time(current_time)
                    self.frame_buffer = []

                time.sleep(1)  # Sleep to prevent high CPU usage

        Thread(target=send_payloads_and_pictures, daemon=True).start()

