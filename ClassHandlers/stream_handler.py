from threading import Event, Lock, Thread
from queue import Queue
from ClassHandlers.camera_handler import CameraHandler
import time
import cv2

class StreamHandler:
    """
    A base class for handling real-time video streaming from a camera.

    This class uses a camera handler to capture video frames and process them in real time.
    It manages the stream in a separate thread and stores frames in a queue for further processing.
    """

    def __init__(self, camera_handler: CameraHandler):
        """
        Initializes the StreamHandler with a given CameraHandler.

        Parameters:
        - camera_handler (CameraHandler): An instance of CameraHandler to manage the camera operations.
        """
        self.camera_handler = camera_handler
        self.web_dim = (self.camera_handler.width, self.camera_handler.height)
        self.frame_queue = Queue(maxsize=10)  # Buffer for storing video frames
        self.frame_queue_lock = Lock()  # Lock for thread-safe queue operations

        self.new_frame_event = Event()  # Event to signal the arrival of a new frame

        self.running = False  # Flag to control the streaming loop
        self.stream_thread = None  # Thread for handling the stream

    def run_stream(self):
        """
        Captures video frames and stores them in a queue.

        This method runs a loop that continuously captures frames from the camera and stores
        them in a queue. It handles errors such as stream disconnection and frame read failures.
        """
        self.running = True
        self.camera_handler.open_camera()

        while self.running:
            # Camera reconnection logic
            if not self.camera_handler.cap.isOpened():
                print("Stream disconnected, attempting to reconnect.")
                try:
                    self.camera_handler.open_camera()
                except ConnectionError as e:
                    print(f"Reconnection failed: {e}")
                    time.sleep(2)  # Wait before retrying
                    continue

            frame = self.camera_handler.read_frame()
            if frame is None:
                print("Frame read failed, skipping frame.")
                time.sleep(0.1)
                continue

            # Frame queue management
            with self.frame_queue_lock:
                if self.frame_queue.full():
                    self.frame_queue.get()  # Remove the oldest frame
                self.frame_queue.put(frame)

            self.new_frame_event.set()  # Signal that a new frame is available

        self.camera_handler.close_camera()  # Close camera when streaming stops

    def start_stream_thread(self):
        """
        Starts the video streaming in a separate thread.

        This method launches a thread that runs the video streaming loop. It ensures that
        only one streaming thread is active at a time.
        """
        if self.stream_thread is None or not self.stream_thread.is_alive():
            self.stream_thread = Thread(target=self.run_stream)
            self.stream_thread.start()

    def stop_stream(self):
        """
        Stops the video streaming thread.

        This method sets the running flag to False, stopping the streaming loop, and waits
        for the thread to finish.
        """
        self.running = False
        if self.stream_thread:
            self.stream_thread.join()

    @staticmethod
    def encode_frame(frame):
        """
        Encodes a video frame into JPEG format.

        This static method encodes a given frame into JPEG format for transmission or storage.
        It returns the encoded frame as bytes.

        Parameters:
        - frame: The frame to be encoded.

        Returns:
        - The encoded frame as bytes, or None if the frame is None.
        """
        if frame is None:
            print("Error: Frame is None")
            return
        _, buffer = cv2.imencode('.jpg', frame)

        return buffer.tobytes()
