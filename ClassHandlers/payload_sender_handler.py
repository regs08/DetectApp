import json
import time
from threading import Thread, Lock
from MqttClient.my_mqtt_client import MQTTClient

class PayloadSenderHandler:
    """
    Class to handle sending of payloads and pictures via MQTT.

    This class is designed to buffer and send serialized payloads and pictures at
    regular intervals using an MQTT client. It operates in a separate thread to
    handle the sending process asynchronously.
    """

    def __init__(self, mqtt_client: MQTTClient, send_interval=5):
        """
        Initializes the PayloadSenderHandler.

        Parameters:
        - mqtt_client (MQTTClient): An instance of MQTTClient for sending messages.
        - send_interval (int, optional): Time interval in seconds between consecutive sends.
                                         Defaults to 5 seconds.
        """
        self.mqtt_client = mqtt_client
        self.pub_topics = self.mqtt_client.pub_topics
        self.payload_buffer = []  # Buffer for payloads to be sent
        self.frame_buffer = []    # Buffer for pictures to be sent
        self.last_payload_send_time = 0
        self.last_picture_send_time = 0
        self.send_interval = send_interval
        self.buffer_lock = Lock()  # Lock for thread safety in buffer operations

    def append_frame(self, frame):
        """
        Appends a frame to the frame buffer.

        Currently used for testing the sending of frames. The buffer will store the
        latest frame only.

        Parameters:
        - frame: The frame to be added to the buffer.
        """
        with self.buffer_lock:
            if len(self.frame_buffer) == 0:
                self.frame_buffer.append(frame)

    def serialize_payload(self, payload):
        """
        Serializes the payload before sending via MQTT.

        TODO: Reconsider where serialization of the payload should take place.

        Parameters:
        - payload: The payload to be serialized.

        Returns:
        - A list of serialized payload dictionaries.
        """
        payload_dicts = [p.to_dict() for p in payload]
        return payload_dicts

    def append_payload(self, payload):
        """
        Appends a serialized payload to the payload buffer.

        Parameters:
        - payload: The payload to be appended.
        """
        with self.buffer_lock:
            serialized_payload = self.serialize_payload(payload)
            self.payload_buffer.extend(serialized_payload)

    def send_payload(self):
        """
        Sends payloads from the payload buffer via MQTT.

        This method combines all payloads in the buffer into a single JSON string and
        publishes it to the MQTT topic designated for detections.
        """
        with self.buffer_lock:
            if self.payload_buffer:
                combined_payload = json.dumps(self.payload_buffer)
                self.mqtt_client.publish_message(topic=self.pub_topics['detection'],
                                                 message=combined_payload.encode('utf-8'))
                self.payload_buffer = []

    def send_picture(self):
        """
        Sends the oldest picture from the frame buffer via MQTT.

        This method publishes the oldest picture in the buffer to the MQTT topic
        designated for images.
        """
        with self.buffer_lock:
            if self.frame_buffer:
                frame = self.frame_buffer.pop(0)
                # todo put sending frames on hold
                #self.mqtt_client.publish_message(topic=self.mqtt_client.pub_topics['image'], message=frame)

    def should_send_payload(self, current_time):
        """
        Determines if it's time to send the payload.

        Parameters:
        - current_time (float): The current time in seconds.

        Returns:
        - bool: True if the current time exceeds the interval since the last payload send, False otherwise.
        """
        return current_time - self.last_payload_send_time > self.send_interval

    def should_send_frame(self, current_time):
        """
        Determines if it's time to send a frame.

        Parameters:
        - current_time (float): The current time in seconds.

        Returns:
        - bool: True if the current time exceeds the interval since the last frame send, False otherwise.
        """
        return current_time - self.last_picture_send_time > self.send_interval

    def update_last_send_time(self, current_time):
        """
        Updates the last payload send time.

        Parameters:
        - current_time (float): The current time in seconds.
        """
        self.last_payload_send_time = current_time

    def update_last_frame_send_time(self, current_time):
        """
        Updates the last frame send time.

        Parameters:
        - current_time (float): The current time in seconds.
        """
        self.last_picture_send_time = current_time

    def start_payload_sender(self):
        """
        Starts a thread to send payloads and pictures at regular intervals.

        This method launches a daemon thread that continuously checks whether it's
        time to send payloads or pictures and sends them if needed. It sleeps for 1 second
        between checks to prevent high CPU usage.
        """
        def send_payloads_and_pictures():
            while True:
                current_time = time.time()
                if self.should_send_payload(current_time):
                    self.send_payload()
                    self.update_last_send_time(current_time)
                if self.should_send_frame(current_time):
                    self.send_picture()
                    self.update_last_frame_send_time(current_time)
                    self.frame_buffer = []

                time.sleep(1)  # Sleep to prevent high CPU usage

        Thread(target=send_payloads_and_pictures, daemon=True).start()
