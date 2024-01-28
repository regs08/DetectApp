class CameraConfig:
    """
    A class to represent camera configuration settings.

    This class holds the configuration details for a camera, including its source
    (like a URL or a device ID) and the desired dimensions for the captured frames.
    """

    def __init__(self, camera_src, width, height):
        """
        Initializes a new CameraConfig instance.

        Parameters:
        - camera_src: The source of the camera. This could be a URL for IP cameras,
                      or an integer for local cameras (e.g., 0 for the default camera).
        - width (int): The desired width of the camera frames.
        - height (int): The desired height of the camera frames.
        """
        self.camera_src = camera_src  # Source of the camera
        self.width = width            # Desired width of the frames
        self.height = height          # Desired height of the frames

    def to_dict(self):
        """
        Converts the CameraConfig instance to a dictionary.

        This method can be useful for serialization, logging, or debugging purposes,
        as it provides a dictionary representation of the camera configuration.

        Returns:
        - dict: A dictionary containing the camera configuration.
        """
        return vars(self)  # Return the internal dictionary of the instance
