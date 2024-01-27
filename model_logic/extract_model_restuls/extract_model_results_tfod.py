from model_logic.extract_model_restuls.extract_model_results_base import ExtractModelResultsBase
from ClassModels.ResultClasses.tf_lite_results import TFLiteResults
from tensorflow_lite_support.cc.task.processor.proto import detections_pb2, bounding_box_pb2
import numpy as np


class ExtractModelResultsTFOD(ExtractModelResultsBase):
    def extract_results(self, results) -> TFLiteResults:
        """
        Extracts the results from TensorFlow Lite object detection model output.

        :param results: A DetectionResult object obtained from TensorFlow Lite's detection model.
        :return: TFLiteResults object containing extracted boxes, labels, and confidence scores.
        """
        if not isinstance(results, detections_pb2.DetectionResult):
            raise TypeError("Results must be of type detections_pb2.DetectionsResult")

        bboxes = []  # List to store bounding boxes
        labels = []  # List to store labels
        confs = []   # List to store confidence scores

        for detection in results.detections:
            # Extract and convert the bounding box to a NumPy array format
            bboxes.append(self.bbox_to_numpy_xyxy(detection.bounding_box))

            # Extract category information for the detected object
            category = detection.categories[0]
            labels.append(category.category_name)  # Add label to list
            confs.append(round(category.score, 2))  # Add confidence score to list

        # Return an instance of TFLiteResults with extracted information
        return TFLiteResults(boxes=bboxes, labels=labels, confs=confs)

    @staticmethod
    def bbox_to_numpy_xyxy(bbox: bounding_box_pb2.BoundingBox):
        """
        Converts a bounding box object to a NumPy array.

        :param bbox: A BoundingBox object from TensorFlow Lite detection results.
        :return: A NumPy array representing the bounding box in [xmin, ymin, xmax, ymax] format.
        """
        # Extract coordinates and dimensions of the bounding box
        xmin = bbox.origin_x
        ymin = bbox.origin_y
        xmax = xmin + bbox.width
        ymax = ymin + bbox.height

        # Create a NumPy array with the bounding box coordinates
        bbox_np = np.array([xmin, ymin, xmax, ymax])

        # Replace any negative values with zero
        bbox_np[bbox_np < 0] = 0
        return bbox_np
