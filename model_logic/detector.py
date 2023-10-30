import cv2
from model_logic import utils
from tflite_support.task import core, processor, vision
from model_logic.base_model import BaseModel
import paho.mqtt.client as mqtt
import json
import logging
import time

from app.config import BROKER_ADDRESS, DETECTION_TOPIC, IMAGE_TOPIC



detection_logger = logging.getLogger("detection-logger")


class ObjectDetector(BaseModel):
    last_sent_time = 0
    image_count = 0

    def initialize_model(self):
            """Initialize the object detector."""
            try:
                self.base_options = core.BaseOptions(
                    file_name=self.model_path, use_coral=self.enable_edgetpu, num_threads=self.num_threads)
                self.detection_options = processor.DetectionOptions(
                    max_results=self.max_results, score_threshold=0.3)
                self.options = vision.ObjectDetectorOptions(
                    base_options=self.base_options, detection_options=self.detection_options)
                self.detector = vision.ObjectDetector.create_from_options(self.options)

                self.mqtt_client = mqtt.Client("ObjectDetectorPublisher")
                self.mqtt_client.connect(BROKER_ADDRESS)

            except Exception as e:
                print(f"Error initializing the object detector: {e}")
                raise

    def handle_detections(self, payload, frame):
        """Handles the detected objects by publishing to MQTT and saving images."""

        self.mqtt_client.publish(topic=DETECTION_TOPIC, payload=payload.encode('utf-8'))
        detection_logger.info(payload)

        # Test method to see how sending picutres functiosn
        self.test_send_pictures(frame=frame, payload=payload)

    def process_frame(self, frame):
        """Run object detection and annotate the frame."""
        frame = cv2.resize(frame, self.web_dim, interpolation=cv2.INTER_AREA)
        input_tensor = vision.TensorImage.create_from_array(frame)
        detection_result = self.detector.detect(input_tensor)

        payload, annotated_frame = utils.process_detection_results(frame, detection_result, conf_thresh=self.conf_thresh)

        if payload:
            self.handle_detections(payload, frame)

        self.calculate_and_show_fps(annotated_frame)

        return annotated_frame

    def test_send_pictures(self, frame, payload):
        """
        test method in sending picturers with mqtt. sends out maximum 2 pictures every 10 seconds
        :param frame: frame of the detection
        :param msg: payload
        :return:
        """
        current_time = time.time()

        payload = json.loads(payload)

        # Check if 10 seconds have passed since the last image was sent
        if current_time - ObjectDetector.last_sent_time > 10:
            print("10seconds past ready to send...")
            ObjectDetector.image_count = 0
            ObjectDetector.last_sent_time = current_time
        for i, pl in enumerate(payload):
            if payload[i]['label'] == "person" and ObjectDetector.image_count < 2:
                print('sending image to be saved on app')
                _, jpeg_cropped = cv2.imencode('.jpg', frame)
                self.mqtt_client.publish(IMAGE_TOPIC, jpeg_cropped.tobytes())
                ObjectDetector.image_count += 1



