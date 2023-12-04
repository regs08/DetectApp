from MqttClient.MqttTopics import MqttTopics
from MqttClient.default_config_args import sub_topics, pub_topics, default_image_path


class MqttConfig:
    def __init__(self, broker_address: str = "localhost",
                 sub_topics: MqttTopics = sub_topics,
                 pub_topics: MqttTopics = pub_topics,
                 image_path: str = default_image_path):
        if not isinstance(broker_address, str):
            raise TypeError("broker_address must be a string")
        if not isinstance(sub_topics, MqttTopics):
            raise TypeError("topics must be a list of MqttTopics")
        if not isinstance(image_path, str):
            raise TypeError("image_path must be a string")

        self.broker_address = broker_address
        self.sub_topics = sub_topics
        self.pub_topics = pub_topics
        self.image_path = image_path
