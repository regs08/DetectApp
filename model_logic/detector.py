from tflite_support.task import core, processor, vision
from model_logic.base_model import BaseModel

class ObjectDetector(BaseModel):
    def __init__(self, *args, **kwargs):
        """
        Initialize the ObjectDetector class by calling the initialization of the base class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)  # Call the constructor of the base class

    def initialize_model(self):
        """
        Initialize the object detector model with the configuration parameters.
        Sets up the model options and creates an object detector instance.
        """
        try:
            # Set base options for the model
            self.base_options = core.BaseOptions(
                file_name=self.model_config.model_path,  # Model file path
                use_coral=self.model_config.enable_edgetpu,  # Use Coral device if enabled
                num_threads=self.model_config.num_threads)  # Number of threads for processing

            # Detection specific options
            self.detection_options = processor.DetectionOptions(
                max_results=self.model_config.max_results,  # Maximum number of detection results
                score_threshold=0.3)  # Score threshold for detection

            # Combined options for the object detector
            self.options = vision.ObjectDetectorOptions(
                base_options=self.base_options,
                detection_options=self.detection_options)

            # Create the object detector instance
            self.detector = vision.ObjectDetector.create_from_options(self.options)

        except Exception as e:
            print(f"Error initializing the object detector: {e}")
            raise

    def process_frame(self, frame):
        """
        Process a single frame for object detection.

        Args:
            frame: The frame (image) to be processed.

        Returns:
            The detection results after processing the frame.
        """
        # Convert the input frame to the tensor format expected by the model
        input_tensor = vision.TensorImage.create_from_array(frame)

        # Perform detection on the input frame
        detection_result = self.detector.detect(input_tensor)

        # Return the results of the detection
        return detection_result
