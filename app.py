from flask import Flask, Response, render_template
from DefaultClassModels.Configs.default_detection_system_config import default_detection_system_config
from DetectionSystem.detection_system import DetectionSystem

app = Flask(__name__)

detection_system = DetectionSystem(default_detection_system_config)
detection_system.create_system()
detection_system.start_all_threads()

@app.route('/')
def index():
    return render_template('index.html')  # Assuming 'index.html' in your templates directory

@app.route('/video')
def video():
    def generate():
        while True:
            with detection_system.processed_queue_lock:
                if not detection_system.processed_queue.empty():
                    frame = detection_system.processed_queue.get()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


