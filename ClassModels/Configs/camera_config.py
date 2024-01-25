class CameraConfig:
    def __init__(self, camera_src, width, height):
        """

        :rtype: object
        """
        self.camera_src = camera_src
        self.width = width
        self.height = height

    def to_dict(self):
        return vars(self)
