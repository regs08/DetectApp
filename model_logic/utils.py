import numpy as np
from tflite_support.task import processor
import supervision as sv
from tensorflow_lite_support.python.task.processor.proto import bounding_box_pb2
from datetime import datetime
import json
from Payload.payload import Payload

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


def extract_detection_data(detection_result: processor.DetectionResult):
    bboxes = []
    labels = []
    confs = []

    for detection in detection_result.detections:
        # Draw bounding_box
        bboxes.append(bbox_to_numpy_xyxy(detection.bounding_box))

        # Draw label and score
        category = detection.categories[0]
        labels.append(category.category_name)
        confs.append(round(category.score, 2))

    return bboxes, labels, confs


def extract_payload(bboxes, labels, confs, conf_thresh):
    payload = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for i, conf in enumerate(confs):
        #filter low confs
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
        print(payload)
        payload_dicts =[p.to_dict() for p in payload]
        payload_json = json.dumps(payload_dicts)

        return payload_json
    return None


def annotate_frame(image, bboxes, labels, confs):

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


def process_detection_results(image, detection_result: processor.DetectionResult, conf_thresh):
    bboxes, labels, confs = extract_detection_data(detection_result)
    payload = extract_payload(bboxes=bboxes, labels=labels, confs=confs, conf_thresh=conf_thresh)
    annotated_frame = annotate_frame(image, bboxes, labels, confs)

    return payload, annotated_frame


def extract_classification_data():
    pass
