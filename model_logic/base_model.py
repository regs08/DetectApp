from abc import ABC, abstractmethod

from ClassModels.Configs.model_config import ModelConfig


class BaseModel(ABC):
    """A base class for real-time vision model logic using a camera (default webcamera)"""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.initialize_model()

    @abstractmethod
    def initialize_model(self):
        """Initialize the model. Must be overridden by subclasses."""
        pass

    @abstractmethod
    def process_frame(self, frame):
        pass
