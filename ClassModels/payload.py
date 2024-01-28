class Payload:
    """
    A class to represent a payload structure.

    This class encapsulates all the necessary attributes of a detection or event, such as
    the detected object's label, the confidence of detection, coordinates of the detected
    object in the image, and additional metadata like filename and timestamp.
    """

    def __init__(self, entry, event, label, confidence, xmin, ymin, xmax, ymax, filename, timestamp):
        """
        Initializes the Payload object with detection/event data.

        Parameters:
        - entry (str): Type of entry (e.g., 'log', 'event').
        - event (str): Type of event (e.g., 'detection').
        - label (str): Label of the detected object.
        - confidence (float): Confidence score of the detection.
        - xmin (int): X-coordinate of the top left corner of the bounding box.
        - ymin (int): Y-coordinate of the top left corner of the bounding box.
        - xmax (int): X-coordinate of the bottom right corner of the bounding box.
        - ymax (int): Y-coordinate of the bottom right corner of the bounding box.
        - filename (str): Name of the file associated with this payload.
        - timestamp (str): Timestamp of when the event occurred.
        """
        self.entry = entry
        self.event = event
        self.label = label
        self.confidence = confidence
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.filename = filename
        self.timestamp = timestamp

    def __iter__(self):
        """
        Iterator method for iterating over the attributes of the Payload object.

        This method allows the Payload object to be iterated over, yielding each attribute
        in the order they are defined. This can be useful for serialization or display purposes.
        """
        for attr in [self.entry, self.event, self.label, self.confidence, self.xmin, self.ymin, self.xmax, self.ymax, self.filename, self.timestamp]:
            yield attr

    def to_dict(self):
        """
        Converts the Payload object into a dictionary.

        This method is useful for serialization, especially when sending data over a network
        or storing it in a format that requires key-value pairs.

        Returns:
        - dict: A dictionary representation of the Payload object.
        """
        return {
            "entry": self.entry,
            "event": self.event,
            "label": self.label,
            "confidence": self.confidence,
            "xmin": self.xmin,
            "ymin": self.ymin,
            "xmax": self.xmax,
            "ymax": self.ymax,
            "filename": self.filename,
            "timestamp": self.timestamp
        }
