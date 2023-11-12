

class MQTTConfig():
    def __init__(self, broker_address: str, topics: dict):
        self.broker_address = broker_address
        self.topics = topics

