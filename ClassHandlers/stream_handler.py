from threading import Event, Lock, Thread
from queue import Queue
from ClassHandlers.camera_handler import CameraHandler

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
        """Run the detection and store frames in a queue."""
        self.running = True
        self.camera_handler.open_camera()
        try:
            while self.running:
                frame = self.camera_handler.read_frame()

                if frame is None:
                    break
                # Store the frame in the queue
                with self.frame_queue_lock:
                    if self.frame_queue.full():
                        self.frame_queue.get()  # Remove the oldest frame if the queue is full
                    self.frame_queue.put(frame)
                self.new_frame_event.set()

        # When everything done, close the camera
        finally:
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
