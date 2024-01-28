from ClassHandlers.FrameAnnotator.frame_annotator_base import FrameAnnotatorBase
from ClassModels.ResultClasses.tf_lite_results import TFLiteResults
import numpy as np
import supervision as sv

class FrameAnnotatorDetections(FrameAnnotatorBase):
    def __init__(self, results: TFLiteResults):
        """
        Initialize the FrameAnnotatorDetections with detection results.

        :param results: An instance of TFLiteResults containing bounding boxes, labels, and confidence scores.
        """
        super().__init__(results)  # Initialize the superclass with the results

    def annotate_frame(self, frame):
        """
        Annotate the given frame with detection information.

        :param frame: The frame to be annotated.
        :return: The frame with annotations (bounding boxes and labels).
        """
        # Calculate and display the frames per second on the frame
        self.calculate_and_show_fps(frame)

        # Check if there are any detections to annotate
        if len(self.results.boxes) > 0:
            # Convert bounding boxes to a NumPy array
            np_bboxes = np.array(self.results.boxes)

            # Create Detections object with bounding boxes and confidence scores
            detections = sv.Detections(xyxy=np_bboxes, confidence=np.array(self.results.confs))

            # Initialize a BoxAnnotator for drawing bounding boxes
            box_annotator = sv.BoxAnnotator()

            # Combine labels with confidence scores for display
            labels_with_conf = [f"{l} {c:.2f}" for l, c in zip(self.results.labels, self.results.confs)]

            # Annotate the frame with bounding boxes and labels
            annotated_frame = box_annotator.annotate(frame, detections, labels=labels_with_conf)

            # Return the annotated frame
            return annotated_frame

        # If no detections, return the original frame
        return frame
