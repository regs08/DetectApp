from MqttClient.my_mqtt_client import MQTTClient
from ClassModels.payload import Payload
import json

my_client=MQTTClient()

test_payload = Payload(
                entry='log',
                event='detection',
                label='person',
                confidence=.99,
                xmin=100,
                ymin=100,
                xmax=100,
                ymax=100,
                filename='abc.jpg',
                timestamp='5-23-23'
            )
payload_arr = [test_payload.to_dict()]

json_payload = json.dumps(payload_arr).encode('utf-8')
my_client.publish_message(my_client.pub_topics['detection'], json_payload)
my_client.run()
