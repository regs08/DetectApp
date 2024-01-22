import threading
from queue import Queue
import cv2
import time


from ClassModels.Configs.camera_config import CameraConfig


class CameraHandler:
    def __init__(self, config: CameraConfig):
        self.camera_id = config.camera_src
        self.width = config.width
        self.height = config.height
        self.dim = (self.width, self.height)
        self.stream_url = config.stream_url
        self.frame_queue = Queue(maxsize=10)  # Adjust based on your needs
        self.capture_thread = None
        self.running = False
        self.cap = None

    def open_camera(self):
        """Open the camera or video stream for capturing."""
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            self.cap = cv2.VideoCapture(self.stream_url or self.camera_id)
            if self.cap.isOpened():
                print(f"Successfully opened {'stream' if self.stream_url else 'camera'}.")
                return True
            else:
                print(f"Failed to open {'stream' if self.stream_url else 'camera'} on attempt {attempts + 1}/{max_attempts}")
                time.sleep(2)  # Wait for 2 seconds before retrying
                attempts += 1
        print(f"Unable to open {'stream' if self.stream_url else 'camera'} after {max_attempts} attempts")
        return False

    def start_capture(self):
        """Start capturing frames in a separate thread."""
        if self.open_camera():
            self.running = True
            self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
            self.capture_thread.start()
        else:
            raise ConnectionError("Could not open camera/stream for frame capture.")

    def _capture_frames(self):
        """Capture frames from the camera or stream and put them in a queue."""
        while self.running:
            success, frame = self.cap.read()
            if success:
                resized_frame = cv2.resize(frame, self.dim)
                if not self.frame_queue.full():
                    self.frame_queue.put(resized_frame)
                else:
                    print("Frame queue is full, dropping frame.")
            else:
                print("Failed to capture frame.")

    def get_frame(self):
        """Get the next frame from the queue."""
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        return None

    def stop_capture(self):
        """Stop the frame capture thread."""
        self.running = False
        if self.capture_thread is not None:
            self.capture_thread.join()
        self.close_camera()

    def close_camera(self):
        """Release the camera or stream resource."""
        if self.cap:
            self.cap.release()

    # Context manager methods can remain unchanged
    def __enter__(self):
        self.start_capture()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_capture()
