from flask import Flask, Response
from model_logic.detector import ObjectDetector
from MqttClient.my_mqtt_client import MQTTClient
import os

working_dir = os.getcwd()

model_path = os.path.join(working_dir, 'saved_models', 'efficientdet_lite0.tflite')
mqtt_client = MQTTClient()

app = Flask(__name__)
detector = ObjectDetector(model_path, mqtt_client=mqtt_client)

@app.route('/video')
def video():
    return Response(detector.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
