from ClassModels.Configs import model_config, mqtt_config, camera_config

class DetectionSystemConfig:
    """
    A class to aggregate and manage configurations for a detection system.

    This class combines configurations for various components of the detection system,
    such as the model, MQTT, and camera, into a single unified configuration object.
    It allows for easy access and modification of these configurations.
    """

    def __init__(self, model_config: model_config.ModelConfig,
                 mqtt_config: mqtt_config.MqttConfig,
                 camera_config: camera_config.CameraConfig):
        """
        Initializes the DetectionSystemConfig with individual component configurations.

        Parameters:
        - model_config (ModelConfig): Configuration settings for the model.
        - mqtt_config (MqttConfig): Configuration settings for MQTT communication.
        - camera_config (CameraConfig): Configuration settings for the camera.
        """
        self.model_config = model_config
        self.mqtt_config = mqtt_config
        self.camera_config = camera_config

        # Set attributes from each configuration
        self.set_attributes(camera_config)
        self.set_attributes(model_config)
        self.set_attributes(mqtt_config)

    def set_attributes(self, config):
        """
        Sets attributes of the DetectionSystemConfig based on a given configuration.

        This method iterates over the key-value pairs in the configuration's dictionary
        representation and sets them as attributes of the DetectionSystemConfig instance.

        Parameters:
        - config: The configuration object (ModelConfig, MqttConfig, CameraConfig).
        """
        for key, value in config.to_dict().items():
            setattr(self, key, value)

    def update_attributes(self, updates):
        """
        Updates attributes of the DetectionSystemConfig based on provided key-value pairs.

        #todo when an attribute is already found log it or notify
        This method allows for updating the configuration dynamically. It checks if the
        attribute exists before updating it. If an attribute is not found, it prints a
        warning message.

        Parameters:
        - updates (dict): A dictionary of updates to apply to the configuration.
        """
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Attribute {key} not found in DetectionSystemConfig")
