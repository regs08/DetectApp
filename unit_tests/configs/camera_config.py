from ClassModels.Configs.camera_config import CameraConfig

stream_url = 'http://127.0.0.1:5000/video'
test_camera_config_from_stream = CameraConfig(camera_src=0, width=640, height=480, stream_url=stream_url)
test_camera_config_from_webcam = CameraConfig(camera_src=0, width=640, height=480)