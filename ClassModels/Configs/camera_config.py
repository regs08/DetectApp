class CameraConfig:
    def __init__(self, camera_id, width, height):
        self.camera_id = camera_id
        self.width = width
        self.height = height

    def to_dict(self):
        return vars(self)
