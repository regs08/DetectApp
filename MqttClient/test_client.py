from MqttClient.my_mqtt_client import MQTTClient
from ClassModels.payload import Payload
from DefaultClassModels.Configs.default_mqtt_config import default_mqtt_config
import json


my_client=MQTTClient(config=default_mqtt_config)

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
    #todo make a timestamp class that adheres to ISO 8601 "YYYY-MM-DDTHH:mm:ssZ"
                timestamp='2023-05-23T00:00:00Z'
            )
payload_arr = [test_payload.to_dict()]

json_payload = json.dumps(payload_arr).encode('utf-8')
my_client.publish_message('logs', json_payload)
my_client.run()
