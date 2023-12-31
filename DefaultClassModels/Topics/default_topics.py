from MqttClient.MqttTopics import MqttTopics


pub_topics = MqttTopics(detection="vehicle/detections", image="vehicle/image", pong="test/pong",
                        test_image="setup/image")

sub_topics = MqttTopics(test_ping="test/ping", test_image="test/image" )