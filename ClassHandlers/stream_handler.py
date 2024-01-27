from threading import Event, Lock, Thread
from queue import Queue
from ClassHandlers.camera_handler import CameraHandler
import time
import cv2


class StreamHandler:
    """A base class for real-time vision model logic using a camera (default webcamera)"""

    def __init__(self, camera_handler: CameraHandler):
        self.camera_handler = camera_handler
        self.web_dim = (self.camera_handler.width, self.camera_handler.height)
        self.frame_queue = Queue(maxsize=10)  # Adjust size as needed
        self.frame_queue_lock = Lock()

        self.new_frame_event = Event()

        self.running = False
        self.stream_thread = None

    def run_stream(self):
        """Run the stream and store frames in a queue with error handling."""
        self.running = True
        self.camera_handler.open_camera()

        while self.running:
            # Check if the stream/camera is open; try to reopen if it's not
            if not self.camera_handler.cap.isOpened():
                print("Stream disconnected, attempting to reconnect.")
                try:
                    self.camera_handler.open_camera()
                except ConnectionError as e:
                    print(f"Reconnection failed: {e}")
                    time.sleep(2)  # Wait for 2 seconds before retrying
                    continue

            frame = self.camera_handler.read_frame()
            if frame is None:
                print("Frame read failed, skipping frame.")
                time.sleep(0.1)  # Brief pause before attempting next frame
                continue

            # Store the frame in the queue
            with self.frame_queue_lock:
                if self.frame_queue.full():
                    self.frame_queue.get()  # Remove the oldest frame if the queue is full
                self.frame_queue.put(frame)

            self.new_frame_event.set()

        # When the stream is stopped, ensure the camera is closed
        self.camera_handler.close_camera()

    def start_stream_thread(self):
        """Starts the detection in a separate thread."""
        if self.stream_thread is None or not self.stream_thread.is_alive():
            self.stream_thread = Thread(target=self.run_stream)
            self.stream_thread.start()

    def stop_stream(self):
        """Stops the detection thread."""
        self.running = False
        if self.stream_thread:
            self.stream_thread.join()

    @staticmethod
    def encode_frame(frame):
        """Encode the frame into JPEG format."""
        if frame is None:
            print("Error: Frame is None")
            return
        _, buffer = cv2.imencode('.jpg', frame)

        return buffer.tobytes()
