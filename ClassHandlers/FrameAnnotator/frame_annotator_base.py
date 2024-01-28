from abc import ABC, abstractmethod
import cv2
from ClassHandlers.FrameAnnotator.fps_utility import FPSUtility
from ClassModels.ResultClasses.results_base import ResultsBase


class FrameAnnotatorBase(ABC):
    def __init__(self, fps_utility=FPSUtility()):
        """
        Initialize the FrameAnnotator with a FPSUtility instance.

        :param fps_utility: An instance of FPSUtility to calculate and display frames per second.
        """

        self.fps_utility = fps_utility

    @abstractmethod
    def annotate_frame(self,results: ResultsBase, frame):
        """
        Abstract method to annotate a frame.
        This method must be implemented by subclasses of FrameAnnotator.

        :param frame: The frame to be annotated.
        :param results: results obtained from a model
        """
        pass

    def calculate_and_show_fps(self, frame):
        """
        Calculate and show the FPS on the frame using the FPSUtility instance.

        :param frame: The frame on which FPS is to be displayed.
        """
        self.fps_utility.update()
        fps_text = f'FPS = {self.fps_utility.get_fps():.1f}'
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
