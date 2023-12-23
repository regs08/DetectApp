
class Payload:
    def __init__(self, entry, event, label, confidence, xmin, ymin, xmax, ymax, filename, timestamp):
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
        for attr in [self.entry, self.event, self.label, self.confidence, self.xmin, self.ymin, self.xmax, self.ymax, self.filename, self.timestamp]:
            yield attr

    def to_dict(self):
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


