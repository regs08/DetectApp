import unittest
from ClassHandlers.camera_handler import CameraHandler
from ClassHandlers.stream_handler import StreamHandler
from DefaultClassModels.Configs.default_camera_config_physical import default_camera_config_physical
import time


class TestStreamHandler(unittest.TestCase):

    def setUp(self):
        """Setup necessary objects for testing StreamHandler."""
        self.camera_config = default_camera_config_physical  # Assuming this is already defined
        # Initialize CameraHandler with a test stream URL or camera ID
        self.camera_handler = CameraHandler(config=self.camera_config)
        self.stream_handler = StreamHandler(camera_handler=self.camera_handler)

    def test_stream_start_stop(self):
        """Test starting and stopping the stream."""
        # Start stream processing in a separate thread
        self.stream_handler.start_stream_thread()
        time.sleep(2)  # Allow some time for the stream to start and process frames

        # Check if the stream started correctly
        self.assertTrue(self.stream_handler.running, "StreamHandler should be running.")
        self.assertTrue(self.stream_handler.stream_thread.is_alive(), "Stream thread should be alive.")

        # Stop the stream
        self.stream_handler.stop_stream()

        # Check if the stream stopped correctly
        self.assertFalse(self.stream_handler.running, "StreamHandler should not be running.")
        self.assertFalse(self.stream_handler.stream_thread.is_alive(), "Stream thread should not be alive.")

    def tearDown(self):
        """Clean up resources."""
        self.stream_handler.stop_stream()


if __name__ == "__main__":
    unittest.main()
