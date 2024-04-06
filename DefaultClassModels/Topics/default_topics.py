from ClassModels.MqttTopics import MqttTopics


pub_topics = MqttTopics(detection="logs", image="vehicle/image", pong="test/pong",
                        test_image="setup/image")

sub_topics = MqttTopics(test_ping="test/ping", test_image="test/image" )