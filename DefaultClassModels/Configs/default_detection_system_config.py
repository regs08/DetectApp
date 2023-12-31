from DefaultClassModels.Configs.default_mqtt_config import default_mqtt_config
from DefaultClassModels.Configs.grape_model_config import grape_model_config
from DefaultClassModels.Configs.default_camera_config import default_camera_config
from ClassModels.Configs.detection_system_config import DetectionSystemConfig


default_detection_system_config = DetectionSystemConfig(model_config=grape_model_config,
                                                        camera_config=default_camera_config,
                                                        mqtt_config=default_mqtt_config)