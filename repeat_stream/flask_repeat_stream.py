import cv2
from flask import Flask, Response, render_template
import os
"""
script to run a looped 6 second video to emulate a live feed 
"""
app = Flask(__name__)

video_dir = os.getcwd()
video_filename = "pinot_noir_six_sec.mp4"

video_path = os.path.join(video_dir, video_filename)


def generate_video(video_path):
    while True:  # Loop the video file indefinitely
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break  # If no frames are left, break and restart the video

            # Encode the frame in JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Yield each frame in the multipart/x-mixed-replace content-type
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        cap.release()

@app.route('/')
def index():
    return render_template('index.html')  # Assuming 'index.html' in your templates directory

@app.route('/video')
def video():
    return Response(generate_video(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
