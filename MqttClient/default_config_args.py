import os
from MqttClient.MqttTopics import MqttTopics


default_image_path = os.path.join(os.getcwd(), "test_image.jpg")
pub_topics = MqttTopics(detection="vehicle/detections", image="vehicle/image", pong="test/pong",
                        test_image="test/image")

sub_topics = MqttTopics(ping="test/ping")