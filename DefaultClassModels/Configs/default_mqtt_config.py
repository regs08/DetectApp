from ClassModels.Configs.mqtt_config import MqttConfig
from DefaultClassModels.Topics.default_topics import sub_topics, pub_topics
import os


default_image_path = os.path.join(os.getcwd(), "test_image.jpeg")

default_mqtt_config = MqttConfig(broker_address="localhost",
                                 sub_topics=sub_topics,
                                 pub_topics=pub_topics,
                                 image_path=default_image_path)