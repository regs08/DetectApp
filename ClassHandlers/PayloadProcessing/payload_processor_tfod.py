from ClassHandlers.PayloadProcessing.payload_processor_base import PayloadProcessorBase
from ClassModels.ResultClasses.tf_lite_results import TFLiteResults
from ClassModels.payload import Payload

from typing import Optional, List, Union
from datetime import datetime

class PayloadProcessorTFOD(PayloadProcessorBase):
    """
    Payload processor for TensorFlow Lite Object Detection results.

    This class extends PayloadProcessorBase and is specifically designed to process
    results from TensorFlow Lite object detection models. It filters and converts the
    detection results into a structured payload format.
    """

    def __init__(self, conf_thresh):
        """
        Initialize the payload processor with a confidence threshold.

        The confidence threshold is used to filter out detections with low confidence.

        Parameters:
        - conf_thresh (float): The confidence threshold for filtering detections.
        """
        super().__init__()  # Corrected call to the superclass constructor
        self.conf_thresh = conf_thresh

    def extract_log_payload(self, results: TFLiteResults) -> Union[List[Payload], None]:
        """
        Extracts a payload from TensorFlow Lite Object Detection results.

        This method processes each detection in the results, filtering them based on the
        confidence threshold. It then formats the detections into a structured payload.

        Parameters:
        - results (TFLiteResults): The object detection results to process.

        Returns:
        - List[dict] or None: A list of dictionaries representing the processed payloads
          for each detection, or None if no payloads were generated.
        """
        payloads_from_detection = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for i, conf in enumerate(results.confs):
            if conf > self.conf_thresh:
                filename = f"{results.labels[i]}_{timestamp}.jpg"

                xmin, ymin, xmax, ymax = [int(coord) for coord in results.boxes[i]]

                payload = Payload(
                    entry='log',
                    event='detection',
                    label=results.labels[i],
                    confidence=conf,
                    xmin=xmin,
                    ymin=ymin,
                    xmax=xmax,
                    ymax=ymax,
                    filename=filename,
                    timestamp=timestamp
                )

                payloads_from_detection.append(payload)

        if payloads_from_detection:
            #payload_dicts = [p.to_dict() for p in payloads_from_detection]
            return payloads_from_detection
        return None
