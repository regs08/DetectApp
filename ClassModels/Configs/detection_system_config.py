from ClassModels.Configs import model_config, mqtt_config, camera_config


class DetectionSystemConfig:
    def __init__(self, model_config: model_config.ModelConfig,
                 mqtt_config: mqtt_config.MqttConfig,
                 camera_config: camera_config.CameraConfig):

        self.model_config = model_config
        self.mqtt_config = mqtt_config
        self.camera_config = camera_config

        self.set_attributes(camera_config)
        self.set_attributes(model_config)
        self.set_attributes(mqtt_config)

    def set_attributes(self, config):
        for key, value in config.to_dict().items():
            setattr(self, key, value)

    def update_attributes(self, updates):
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Attribute {key} not found in DetectionSystemConfig")


