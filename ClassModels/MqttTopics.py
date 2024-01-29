class MqttTopics:
    def __init__(self, **topics):
        """
        Initialize the MqttTopics class with a variable number of topic arguments.

        Args:
            **topics: Variable keyword arguments where each keyword is the topic name
                      and its value is the corresponding topic string.

        Raises:
            ValueError: If any of the topic values is not a string.
        """
        self._topics = topics  # Store topics in an internal dictionary

        # Validate that each topic is a string
        for name, topic in self._topics.items():
            if not isinstance(topic, str):
                raise ValueError(f"Topic value for '{name}' must be a string.")

    def __iter__(self):
        """
        Allows iteration over the MqttTopics instance.

        Returns:
            An iterator over the topic items (key-value pairs).
        """
        return iter(self._topics.items())

    def __getitem__(self, key):
        """
        Allows accessing a topic value using the subscription syntax.

        Args:
            key: The topic name.

        Returns:
            The topic value associated with the given key.
        """
        return self._topics[key]

    def __setitem__(self, key, value):
        """
        Allows setting a topic value using the subscription syntax.

        Args:
            key: The topic name.
            value: The topic value to be set.

        Raises:
            ValueError: If the topic value is not a string.
        """
        if not isinstance(value, str):
            raise ValueError(f"Topic value for '{key}' must be a string.")
        self._topics[key] = value

    def items(self):
        """
        Provides access to the topic items (key-value pairs).

        Returns:
            The items of the internal topics dictionary.
        """
        return self._topics.items()
