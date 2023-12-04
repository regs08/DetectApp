
class MqttTopics:
    def __init__(self, **topics):
        self._topics = topics  # Store topics in an internal dictionary
        for name, topic in self._topics.items():
            if not isinstance(topic, str):
                raise ValueError(f"Topic value for '{name}' must be a string.")

    def __iter__(self):
        return iter(self._topics.items())

    def __getitem__(self, key):
        return self._topics[key]

    def __setitem__(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f"Topic value for '{key}' must be a string.")
        self._topics[key] = value

    def items(self):
        return self._topics.items()
