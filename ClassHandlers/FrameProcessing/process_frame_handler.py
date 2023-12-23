from abc import ABC, abstractmethod
import cv2

from ClassModels.Configs.detection_system_config import DetectionSystemConfig
from ClassHandlers.fps_utility import FPSUtility


class ProcessFrame(ABC):
    def __init__(self, config: DetectionSystemConfig, fps_utility=FPSUtility()):
        self.conf_thresh = config.model_config.conf_thresh
        self.frame_dim = (config.camera_config.width, config.camera_config.height)
        self.fps_utility = fps_utility

    @abstractmethod
    def extract_model_results(self, results):
        """
        :return: results of the model, e.g bbox, labels
        """
        pass

    def calculate_and_show_fps(self, frame):
        """Calculate and show the FPS on the frame."""
        self.fps_utility.update()
        fps_text = f'FPS = {self.fps_utility.get_fps():.1f}'
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)



