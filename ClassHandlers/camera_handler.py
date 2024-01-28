import cv2
from ClassModels.Configs.camera_config import CameraConfig
"""
Wrapper class for cv2 camera's interface designed to be passed into a ML model class
With the wrapped class we can use different camera's and their inputs more ambiguously e.g camera handler getting 
input from a stream, and a camera handler getting input directly from a webcam. 
"""


class CameraHandler:
    def __init__(self, config:CameraConfig):
        self.camera_src = config.camera_src
        self.width = config.width
        self.height = config.height
        self.dim = (self.width, self.height)

        self.cap = None

    def open_camera(self):
        """Open the camera for capturing."""
        self.cap = cv2.VideoCapture(self.camera_src)
        if not self.cap.isOpened():
            print(f"Failed to open camera with ID {self.camera_src}")
        else:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read_frame(self):
        """Read a single frame from the camera."""
        if self.cap:
            success, frame = self.cap.read()
            if success:

                return cv2.resize(frame, self.dim)
            else:
                print("Failed to read frame from camera.")
        return None

    def close_camera(self):
        """Release the camera resource."""
        if self.cap:
            self.cap.release()

    def __enter__(self):
        """Enable usage with the context manager."""
        self.open_camera()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the camera is released when exiting the context."""
        self.close_camera()