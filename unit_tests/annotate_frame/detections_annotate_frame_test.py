import unittest
import numpy as np
import cv2
from ClassHandlers.FrameProcessing.detections_frame_annotator import DetectionsFrameAnnotator


class TestBaseFrameAnnotator(unittest.TestCase):
    def test_annotate_frame(self):
        # Setup
        annotator = DetectionsFrameAnnotator()

        # Create a black image (e.g., 640x480)
        image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Define some random boxes, labels, and confidences
        bboxes = [[50, 50, 200, 200], [300, 300, 450, 450]]  # Example: [[xmin, ymin, xmax, ymax], ...]
        labels = ['label1', 'label2']
        confs = [0.9, 0.75]

        # Annotate the frame
        annotated_image = annotator.annotate_frame(image, bboxes, labels, confs)

        # Save the annotated image for visual inspection
        cv2.imwrite('annotated_test_image.jpg', annotated_image)

        # Assert (In this case, we check if the output is not None or has the same shape as input)
        self.assertIsNotNone(annotated_image)
        self.assertEqual(image.shape, annotated_image.shape)

        # Additional checks can include verifying the presence of annotations, but this usually requires manual inspection.

if __name__ == '__main__':
    unittest.main()
