import unittest
import cv2
from ClassHandlers.FrameAnnotator.frame_annotator_detections import FrameAnnotatorDetections
from ClassModels.ResultClasses.tf_lite_results import TFLiteResults


class TestBaseFrameAnnotator(unittest.TestCase):
    def test_annotate_frame(self):
        # Setup
        import numpy as np

        bboxes = [[50, 50, 200, 200], [300, 300, 450, 450]]  # Original list of bounding boxes
        bboxes_np = [np.array(bbox) for bbox in bboxes]  # Convert each bbox to a NumPy array

        # bboxes_np is now a list of NumPy arrays
        labels = ['label1', 'label2']
        confs = [0.9, 0.75]

        results = TFLiteResults(boxes=bboxes_np, labels=labels, confs=confs)
        annotator = FrameAnnotatorDetections(results)

        # Create a black image (e.g., 640x480)
        image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Define some random boxes, labels, and confidences

        # Annotate the frame
        annotated_image = annotator.annotate_frame(frame=image)

        # Save the annotated image for visual inspection
        cv2.imwrite('annotated_test_image.jpg', annotated_image)

        # Assert (In this case, we check if the output is not None or has the same shape as input)
        self.assertIsNotNone(annotated_image)
        self.assertEqual(image.shape, annotated_image.shape)

        # Additional checks can include verifying the presence of annotations, but this usually requires manual inspection.

if __name__ == '__main__':
    unittest.main()
