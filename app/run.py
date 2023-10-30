from flask import Flask, Response
from model_logic.detector import ObjectDetector
import os
from logger.custom_logger import JsonFormatter
from logging.handlers import RotatingFileHandler
import logging


log_handler = RotatingFileHandler('logs/app.log', maxBytes=5*1024*1024, backupCount=5)
json_formatter = JsonFormatter()
log_handler.setFormatter(json_formatter)
logger = logging.getLogger("app-logger")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


# New logger setup for detection events
detection_log_handler = RotatingFileHandler('logs/detection_events.log', maxBytes=5*1024*1024, backupCount=5)
detection_log_handler.setFormatter(json_formatter)  # Using the same formatter, but you can choose a different one if needed
detection_logger = logging.getLogger("detection-logger")
detection_logger.addHandler(detection_log_handler)
detection_logger.setLevel(logging.INFO)

working_dir = os.getcwd()

model_path = os.path.join(working_dir, 'saved_models', 'efficientdet_lite0.tflite')
app = Flask(__name__)
# getting  connection issues along with theloggerris logging alldata and it seemsincorrectly
detector = ObjectDetector(model_path)

@app.route('/video')
def video():
    return Response(detector.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
