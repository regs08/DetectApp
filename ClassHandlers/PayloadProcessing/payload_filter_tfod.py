from ClassHandlers.PayloadProcessing.payload_filter import PayloadFilter
from ClassModels.ResultClasses.tf_lite_results import TFLiteResults


class PayloadFilterTFOD(PayloadFilter):
    """
    A basic payload filter class for TensorFlow Lite Object Detection results.

    This class extends the PayloadFilter to specifically handle filtering of results
    from TensorFlow Lite object detection models. Currently, it provides basic filtering
    functionality with plans for more sophisticated features in future updates.
    """

    def __init__(self, results: TFLiteResults):
        """
        Initialize the filter with TensorFlow Lite Object Detection results.

        Ensures that the provided results are specifically for TensorFlow Lite object
        detection models, leveraging the type checking from the base PayloadFilter class.

        Parameters:
        - results (TFLiteResults): The object detection results to be filtered.
        """
        super().__init__(results)  # Corrected the call to the superclass constructor

    def filter_by_conf(self, conf_thresh):
        """
        Filters the results based on a confidence threshold.

        This method checks if the confidence level of the results exceeds the provided
        threshold. It's a basic implementation with potential for more comprehensive
        filtering logic in future updates.

        Parameters:
        - conf_thresh (float): The confidence threshold for filtering the results.

        Returns:
        - bool: True if the results' confidence is greater than the threshold, False otherwise.
        """
        if self.results.conf > conf_thresh:
            return True
        else:
            return False
