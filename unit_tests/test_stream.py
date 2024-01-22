from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)


def generate_frames():
    # Open a video capture from your camera or a different video file/stream
    cap = cv2.VideoCapture("http://127.0.0.1:5000/video")

    while True:
        success, frame = cap.read()
        if not success:
            break  # Exit the loop if unable to capture
        else:
            # Process the frame, e.g., convert to grayscale for simplicity
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Encode the processed frame in JPEG format
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()

            # Yield each frame in the multipart/x-mixed-replace content-type
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video')
def video():
    # Serve the video stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    # Serve a simple webpage with the video stream
    return render_template('index.html')  # Ensure you have an index.html file in your templates directory


if __name__ == '__main__':
    app.run(debug=True, port=8000)

