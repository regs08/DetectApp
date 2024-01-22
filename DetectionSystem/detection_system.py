from ClassHandlers.payload_sender_handler import PayloadSenderHandler
from ClassHandlers.FrameProcessing.detection_payload_processor import DetectionPayloadProcessor
from ClassHandlers.stream_handler import StreamHandler
from ClassHandlers.camera_handler import CameraHandler
from ClassModels.Configs.detection_system_config import DetectionSystemConfig
from MqttClient.my_mqtt_client import MQTTClient
from model_logic.detector import ObjectDetector
from threading import Thread, Lock
from queue import Queue


class DetectionSystem:
    """
    Wrapper class to integrate our object detector, mqtt client, payload handler, and frame and payload processing
    our object detector will be responsible for detecting objects from a camera
    our detection payload processor will process the frame (annotate it) and the payload, extract the payload
    our payload handler will be responsible for sending the payload via the mqtt client

    todo introduce a more dynamic approach.
        Have some sort of controller (mqtt_client?) that can stop threads
        Would be useful to stop detection. modify config file, change model, change detection objectives on the fly
    todo look into threading and resource management

    todo error handiling

    """
    def __init__(self, detection_system_config: DetectionSystemConfig):
        self.detection_system_config = detection_system_config

        self.object_detector = None
        self.camera_handler = None
        self.payload_sender_handler = None
        self.stream_handler = None
        self.detection_payload_processor = None
        self.mqtt_client = None

        self.send_interval = 5
        self.processed_queue = Queue(maxsize=10)  # Adjust size as needed
        self.processed_queue_lock = Lock()

    def start_all_threads(self):
        self.start_mqtt_client_thread()
        self.start_stream_thread()
        self.start_payload_sender_handler_thread()
        self.start_payload_frame_processing()

    def create_system(self):
        self.create_camera_handler()
        self.create_mqtt_client()
        self.create_detection_payload_processor()
        self.create_object_detector()
        self.create_payload_sender()
        self.create_stream_handler()

    def start_payload_frame_processing(self):
        def process_payloads_frames():
            while True:
                self.stream_handler.new_frame_event.wait()
                self.stream_handler.new_frame_event.clear()
                # Check if there's a new frame in the queue
                if not self.stream_handler.frame_queue.empty():
                    with self.stream_handler.frame_queue_lock:
                        frame = self.stream_handler.frame_queue.get()
                        detection_result = self.object_detector.process_frame(frame)
                        # annotate the frame, and extract payload
                        payload, annotated_frame = \
                            self.detection_payload_processor.process_detection_results(detection_result, frame)

                    #add the frame to the processed queue
                    with self.processed_queue_lock:
                        if self.processed_queue.full():
                            self.processed_queue.get()  # Remove the oldest frame if the queue is full
                        encoded_frame = self.stream_handler.encode_frame(annotated_frame)
                        self.processed_queue.put(encoded_frame)

                    if annotated_frame.any():
                        # Appends a frame every 5 seconds. using logic from payload sender handler class
                        self.payload_sender_handler.append_frame(encoded_frame)
                    # Process the payload # appending a fixed amount to send every 5 seconds
                    if payload:
                        self.payload_sender_handler.append_payload(payload)

        Thread(target=process_payloads_frames, daemon=True).start()

    def create_object_detector(self):
        self.object_detector = ObjectDetector(model_config=self.detection_system_config.model_config)

    def create_camera_handler(self):
        self.camera_handler = CameraHandler(config=self.detection_system_config.camera_config)

    def create_stream_handler(self):
        try:
            if not self.camera_handler:
                raise ValueError("Camera handler is not initialized")

            self.stream_handler = StreamHandler(self.camera_handler)

        except ValueError as e:
            print(f"Error in create_stream_handler: {e}")

    def create_detection_payload_processor(self):
        self.detection_payload_processor = DetectionPayloadProcessor(config=self.detection_system_config)

    def create_mqtt_client(self):
        self.mqtt_client = MQTTClient(self.detection_system_config.mqtt_config)

    def create_payload_sender(self):
        self.payload_sender_handler = PayloadSenderHandler(mqtt_client=self.mqtt_client,
                                                           send_interval=self.send_interval)

    def start_stream_thread(self):
        self.stream_handler.start_stream_thread()

    def start_payload_sender_handler_thread(self):
        self.payload_sender_handler.start_payload_sender()

    def start_mqtt_client_thread(self):
        self.payload_sender_handler.mqtt_client.start_mqtt_client_thread()









