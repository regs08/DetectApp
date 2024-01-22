from DetectionSystem.detection_system import DetectionSystem


class DetectionSystemController:
    def __init__(self, detection_system: DetectionSystem):
        self.detection_system = detection_system
        # Mapping user input commands to DetectionSystem methods
        self.command_map = {
            "start mqtt thread": self.detection_system.start_mqtt_client_thread,
            "start stream thread": self.detection_system.start_stream_thread,
            "start payload sender": self.detection_system.start_payload_sender_handler_thread,
            # Add more commands as needed
        }

    def run_command(self, command: str):
        """Executes the command corresponding to the user input."""
        if command in self.command_map:
            self.command_map[command]()
            print(f"Executed command: {command}")
        else:
            print("Unknown command.")

    def start(self):
        """Starts the command loop for user input."""
        while True:
            command = input("Enter command: ")
            if command.lower() == "exit":
                break
            self.run_command(command)
