from tflite_support.task import core, processor, vision
from model_logic.base_model import BaseModel


class ObjectDetector(BaseModel):

    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)

    def initialize_model(self):
        """Initialize the object detector."""
        try:
            self.base_options = core.BaseOptions(
                file_name=self.model_config.model_path,
                use_coral=self.model_config.enable_edgetpu,
                num_threads=self.model_config.num_threads)
            self.detection_options = processor.DetectionOptions(
                max_results=self.model_config.max_results, score_threshold=0.3)
            self.options = vision.ObjectDetectorOptions(
                base_options=self.base_options, detection_options=self.detection_options)
            self.detector = vision.ObjectDetector.create_from_options(self.options)

        except Exception as e:
            print(f"Error initializing the object detector: {e}")
            raise

    def process_frame(self, frame):

        # convert to tflite format
        input_tensor = vision.TensorImage.create_from_array(frame)
        # get model results
        detection_result = self.detector.detect(input_tensor)

        return detection_result


