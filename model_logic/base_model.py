from abc import ABC, abstractmethod
from ClassModels.Configs.model_config import ModelConfig

class BaseModel(ABC):
    """A base class for real-time vision model logic using a camera (default webcamera)"""

    def __init__(self, model_config: ModelConfig):
        """
        Initializes the BaseModel with a given configuration.

        Args:
            model_config (ModelConfig): Configuration settings for the model.
        """
        self.model_config = model_config  # Store the configuration settings
        self.initialize_model()  # Call to the method to initialize the model

    @abstractmethod
    def initialize_model(self):
        """
        Abstract method to initialize the model.
        This method must be implemented by all subclasses of BaseModel.
        """
        pass

    @abstractmethod
    def process_frame(self, frame):
        """
        Abstract method to process a single frame.
        This method must be implemented by all subclasses and is intended to
        contain the logic for processing each frame captured from the camera.

        Args:
            frame: The frame to be processed.
        """
        pass
