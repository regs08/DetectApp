import numpy as np
from ClassModels.ResultClasses.results_base import ResultsBase


class TFLiteResults(ResultsBase):
    def __init__(self, boxes: np.ndarray, labels: list[str], confs: list[float]):
        """
        Initialize the TFLiteResults with detection output.

        :param boxes: A NumPy array of bounding boxes, each box represented as [xmin, ymin, xmax, ymax].
        :param labels: A list of labels corresponding to the detected objects.
        :param confs: A list of confidence scores corresponding to the detected objects.
        """
        if not isinstance(boxes, np.ndarray):
            raise TypeError("boxes must be a NumPy array")
        if not all(isinstance(label, str) for label in labels):
            raise TypeError("labels must be a list of strings")
        if not all(isinstance(conf, float) for conf in confs):
            raise TypeError("confs must be a list of floats")

        self.boxes = boxes
        self.labels = labels
        self.confs = confs

    def __getitem__(self, key):
        """
        Allow direct indexing into the class to access boxes, labels, and confs.
        """
        if key == 'boxes':
            return self.boxes
        elif key == 'labels':
            return self.labels
        elif key == 'confs':
            return self.confs
        else:
            raise KeyError("Invalid key. Use 'boxes', 'labels', or 'confs'.")