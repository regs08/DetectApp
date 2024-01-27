from ClassHandlers.FrameAnnotator.frame_annotator_base import FrameAnnotatorBase
from ClassModels.ResultClasses.tf_lite_results import TFLiteResults
import numpy as np
import supervision as sv


class FrameAnnotatorDetections(FrameAnnotatorBase):
    def __int__(self, results: TFLiteResults, fps_utility):
        super().__init__(results, fps_utility)

    def annotate_frame(self, frame):
        self.calculate_and_show_fps(frame)

        # Checking for detections
        if len(self.results.boxes) > 0:
            bboxes = np.array(self.results.boxes)

            detections = sv.Detections(xyxy=np.array(self.results.boxes),
                                       confidence=np.array(self.results.confs))

            # Annotating Frame
            box_annotator = sv.BoxAnnotator()
            # Box annotator doesnt add confidence values so adding them in here
            labels_with_conf = [f"{l} {c:.2f}" for l, c in zip(self.results.labels, self.results.confs)]
            annotated_frame = box_annotator.annotate(frame, detections, labels=labels_with_conf)
            return annotated_frame

        return frame