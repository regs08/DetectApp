# Import necessary classes and modules for the detection system
from ClassHandlers.payload_sender_handler import PayloadSenderHandler
from ClassHandlers.stream_handler import StreamHandler
from ClassHandlers.camera_handler import CameraHandler
from ClassModels.Configs.detection_system_config import DetectionSystemConfig
from MqttClient.my_mqtt_client import MQTTClient
from model_logic.detector import ObjectDetector
from threading import Thread, Lock
from queue import Queue

from ClassHandlers.FrameAnnotator.frame_annotator_detections import FrameAnnotatorDetections
from model_logic.process_model_restuls.process_model_results_tfod import ProcessModelResultsTFOD
from ClassHandlers.PayloadProcessing.payload_processor_tfod import PayloadProcessorTFOD


class DetectionSystem:
    """
    # Todo seperate methods/classes into groups whether they can be modified by the app(mqtt), only on the python side, or both
    DetectionSystem class integrates components for object detection and communication.
    It includes an object detector, MQTT client, payload handler, frame annotator, and payload processor.
    The system detects objects using a camera and communicates the results via MQTT.
    """

    def __init__(self, detection_system_config: DetectionSystemConfig):
        # Configuration and initial setup for the detection system
        self.detection_system_config = detection_system_config

        # Initial placeholders for various system components
        self.object_detector = None
        self.camera_handler = None
        self.payload_sender_handler = None
        self.stream_handler = None
        self.detection_payload_processor = None
        self.mqtt_client = None

        # Interval for sending data
        self.send_interval = 5
        # Queue to store processed frames with a maximum size
        self.processed_queue = Queue(maxsize=10)
        self.processed_queue_lock = Lock()

        # Instantiate utility classes for processing results and annotating frames
        self.result_processor = ProcessModelResultsTFOD()
        self.frame_annotator = FrameAnnotatorDetections()

    def start_all_threads(self):
        # Start various threads required for the system to function
        self.start_mqtt_client_thread()
        self.start_stream_thread()
        self.start_payload_sender_handler_thread()
        self.start_payload_frame_processing()

    def create_system(self):
        # Create and initialize all components of the detection system
        self.create_camera_handler()
        self.create_mqtt_client()
        self.create_payload_processor()
        self.create_object_detector()
        self.create_payload_sender()
        self.create_stream_handler()

    def start_payload_frame_processing(self):
        # Define and start the thread for processing payloads and frames
        def process_payloads_frames():
            while True:
                # Wait for a new frame event and then clear it
                self.stream_handler.new_frame_event.wait()
                self.stream_handler.new_frame_event.clear()

                # Process new frames if available
                if not self.stream_handler.frame_queue.empty():
                    with self.stream_handler.frame_queue_lock:
                        frame = self.stream_handler.frame_queue.get()
                        detection_result = self.object_detector.process_frame(frame)
                        wrapped_results = self.result_processor.extract_results(detection_result)
                        annotated_frame = self.frame_annotator.annotate_frame(results=wrapped_results, frame=frame)
                        payload = self.payload_processor.extract_log_payload(wrapped_results)

                    # Add the annotated frame to the processed queue
                    with self.processed_queue_lock:
                        if self.processed_queue.full():
                            self.processed_queue.get()  # Remove oldest frame if full
                        encoded_frame = self.stream_handler.encode_frame(annotated_frame)
                        self.processed_queue.put(encoded_frame)

                    # Send frame and payload at specified intervals
                    if annotated_frame.any():
                        # todo put sending images on hold for now
                        pass
                         #self.payload_sender_handler.append_frame(encoded_frame)
                    if payload:
                        self.payload_sender_handler.append_payload(payload)

        # Start the thread for processing payloads and frames
        Thread(target=process_payloads_frames, daemon=True).start()

    # Methods to create various components of the system
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

    def create_payload_processor(self):
        self.payload_processor = PayloadProcessorTFOD(self.detection_system_config.conf_thresh)

    def create_mqtt_client(self):
        self.mqtt_client = MQTTClient(self.detection_system_config.mqtt_config)

    def create_payload_sender(self):
        self.payload_sender_handler = PayloadSenderHandler(mqtt_client=self.mqtt_client,
                                                           send_interval=self.send_interval)

    # Methods to start different threads for camera streaming, payload sending, and MQTT client
    def start_stream_thread(self):
        self.stream_handler.start_stream_thread()

    def start_payload_sender_handler_thread(self):
        self.payload_sender_handler.start_payload_sender()

    def start_mqtt_client_thread(self):
        self.payload_sender_handler.mqtt_client.start_mqtt_client_thread()
