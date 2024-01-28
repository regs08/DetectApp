import os

class ModelConfig:
    """
    A class to represent the configuration settings for a machine learning model.

    This class holds the necessary configuration details for a model, such as its path,
    whether to use Edge TPU acceleration, the number of threads for computation, confidence
    threshold for detection, and the maximum number of results to return.
    """

    def __init__(self, model_path, enable_edgetpu=False, num_threads=1, conf_thresh=0.5, max_results=3):
        """
        Initializes a new ModelConfig instance.

        Parameters:
        - model_path (str): The file path to the machine learning model.
        - enable_edgetpu (bool, optional): Flag to enable Edge TPU acceleration. Defaults to False.
        - num_threads (int, optional): The number of threads to use for model computations. Defaults to 1.
        - conf_thresh (float, optional): The confidence threshold for detection. Defaults to 0.5.
        - max_results (int, optional): The maximum number of detection results to return. Defaults to 3.

        Raises:
        - AssertionError: If the model_path does not exist.
        """
        self.model_path = model_path
        assert os.path.exists(model_path), 'model path not found!'
        self.enable_edgetpu = enable_edgetpu
        self.num_threads = num_threads
        self.conf_thresh = conf_thresh
        self.max_results = max_results

    def __str__(self):
        """
        String representation of the ModelConfig instance.

        Returns:
        - str: A formatted string showing the model configuration settings.
        """
        return f"ModelConfig(model_path={self.model_path}, enable_edgetpu={self.enable_edgetpu}, num_threads={self.num_threads}, conf_thresh={self.conf_thresh}, max_results={self.max_results})"

    def to_dict(self):
        """
        Converts the ModelConfig instance to a dictionary.

        This method can be useful for serialization, logging, or debugging purposes,
        as it provides a dictionary representation of the model configuration.

        Returns:
        - dict: A dictionary containing the model configuration.
        """
        return vars(self)  # Return the internal dictionary of the instance
