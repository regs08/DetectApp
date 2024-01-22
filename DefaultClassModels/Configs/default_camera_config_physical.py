from ClassModels.Configs.camera_config import CameraConfig

default_camera_config_physical = CameraConfig(camera_src=0, width=480, height=480)
default_camera_config_stream = CameraConfig(camera_src='http://127.0.0.1:5000/video', width=480, height=480)