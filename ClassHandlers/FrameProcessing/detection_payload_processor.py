from ClassHandlers.FrameProcessing.process_frame_handler import ProcessFrame
from datetime import datetime
from ClassModels.payload import Payload
from tensorflow_lite_support.python.task.processor.proto import bounding_box_pb2
import numpy as np
import supervision as sv


class DetectionPayloadProcessor(ProcessFrame):
    def __int__(self, config):
        super().__init__(config)

    def extract_model_results(self, results):
        bboxes = []
        labels = []
        confs = []

        for detection in results.detections:
            # Draw bounding_box
            bboxes.append(self.bbox_to_numpy_xyxy(detection.bounding_box))

            # Draw label and score
            category = detection.categories[0]
            labels.append(category.category_name)
            confs.append(round(category.score, 2))

        return bboxes, labels, confs

    def process_detection_results(self, results, frame):
        bboxes, labels, confs = self.extract_model_results(results)
        payload = self.extract_log_payload(bboxes=bboxes, labels=labels, confs=confs, conf_thresh=self.conf_thresh)
        annotated_frame = self.annotate_frame(frame, bboxes, labels, confs)

        return payload, annotated_frame

    @staticmethod
    def extract_log_payload(bboxes, labels, confs, conf_thresh):
        payload = []

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for i, conf in enumerate(confs):
            # filter low confs
            if conf > conf_thresh:
                filename = f"{labels[i]}_{timestamp}.jpg"

                xmin, ymin, xmax, ymax = [int(coord) for coord in bboxes[i]]

                data = Payload(
                    entry='log',
                    event='detection',
                    label=labels[i],
                    confidence=conf,
                    xmin=xmin,
                    ymin=ymin,
                    xmax=xmax,
                    ymax=ymax,
                    filename=filename,
                    timestamp=timestamp
                )

                payload.append(data)
        if payload:
            payload_dicts = [p.to_dict() for p in payload]

            return payload_dicts
        return None

    def annotate_frame(self, image, bboxes, labels, confs):
        self.calculate_and_show_fps(image)

        # Checking for detections
        if len(bboxes) > 0:
            bboxes = np.array(bboxes)

            detections = sv.Detections(xyxy=np.array(bboxes),
                                       confidence=np.array(confs))

            # Annotating Frame
            box_annotator = sv.BoxAnnotator()
            # Box annotator doesnt add confidence values so adding them in here
            labels_with_conf = [f"{l} {c:.2f}" for l, c in zip(labels, confs)]
            annotated_frame = box_annotator.annotate(image, detections, labels=labels_with_conf)
            return annotated_frame

        return image

    @staticmethod
    def bbox_to_numpy_xyxy(bbox: bounding_box_pb2.BoundingBox):
        # Access the bounding box values from the BoundingBox object
        xmin = bbox.origin_x
        ymin = bbox.origin_y
        xmax = xmin + bbox.width
        ymax = ymin + bbox.height

        # Create a NumPy array [x1, y1, x2, y2]

        bbox_np = np.array([xmin, ymin, xmax, ymax])
        # Sometimes getting negative values changing them to zero
        bbox_np[bbox_np < 0] = 0
        return bbox_np

