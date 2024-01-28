from MqttClient.MqttTopics import MqttTopics

class MqttConfig:
    """
    A class to represent the configuration settings for MQTT communication.

    This class holds configuration details necessary for establishing MQTT connections,
    such as broker address, subscription topics, publication topics, and image path
    used in the MQTT messaging.
    """

    def __init__(self, broker_address: str,
                 sub_topics: MqttTopics,
                 pub_topics: MqttTopics,
                 image_path: str):
        """
        Initializes a new MqttConfig instance.

        Parameters:
        - broker_address (str): The address of the MQTT broker.
        - sub_topics (MqttTopics): The topics to subscribe to.
        - pub_topics (MqttTopics): The topics to publish messages to.
        - image_path (str): The path where images are stored for sending over MQTT.

        Raises:
        - TypeError: If any of the parameters are not of the expected type.
        """
        if not isinstance(broker_address, str):
            raise TypeError("broker_address must be a string")
        if not isinstance(sub_topics, MqttTopics):
            raise TypeError("sub_topics must be an instance of MqttTopics")
        if not isinstance(pub_topics, MqttTopics):
            raise TypeError("pub_topics must be an instance of MqttTopics")
        if not isinstance(image_path, str):
            raise TypeError("image_path must be a string")

        self.broker_address = broker_address
        self.sub_topics = sub_topics
        self.pub_topics = pub_topics
        self.image_path = image_path

    def to_dict(self):
        """
        Converts the MqttConfig instance to a dictionary.

        This method can be useful for serialization, logging, or debugging purposes,
        as it provides a dictionary representation of the MQTT configuration.

        Returns:
        - dict: A dictionary containing the MQTT configuration.
        """
        return vars(self)  # Return the internal dictionary of the instance
