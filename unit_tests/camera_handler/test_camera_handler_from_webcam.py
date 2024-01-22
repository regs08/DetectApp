import unittest
from ClassHandlers.camera_handler import CameraHandler
from unit_tests.configs.camera_config import test_camera_config_from_webcam


class TestCameraHandlerFromStream(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        # Create a default camera configuration
        self.config = test_camera_config_from_webcam

    def test_open_camera(self):
        """Test opening the camera."""
        camera_handler = CameraHandler(self.config)
        try:
            camera_handler.open_camera()
            self.assertTrue(camera_handler.cap.isOpened(), "Camera should be opened.")
        finally:
            camera_handler.close_camera()

    def test_read_frame(self):
        """Test reading a frame from the camera."""
        camera_handler = CameraHandler(self.config)
        try:
            camera_handler.open_camera()
            frame = camera_handler.read_frame()
            self.assertIsNotNone(frame, "Should be able to read a frame.")
        finally:
            camera_handler.close_camera()

    def test_close_camera(self):
        """Test closing the camera."""
        camera_handler = CameraHandler(self.config)
        camera_handler.open_camera()
        camera_handler.close_camera()
        self.assertFalse(camera_handler.cap.isOpened(), "Camera should be closed.")

if __name__ == "__main__":
    unittest.main()
