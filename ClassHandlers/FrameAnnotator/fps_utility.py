import time


class FPSUtility:
    def __init__(self, avg_frame_count=5):
        """
        Initializes the FPS utility.

        :param avg_frame_count: The number of frames to average over when calculating FPS.
                                Default is 5.
        """
        self.avg_frame_count = avg_frame_count  # Number of frames to average for FPS calculation
        self.frame_counter = 0  # Counter for the number of frames processed
        self.start_time = time.time()  # Timestamp when the first frame was processed
        self.fps = 0  # The calculated frames per second

    def update(self):
        """
        Update the frame counter and recalculate FPS.

        This method should be called for each new frame. It increments the frame counter,
        and if the number of frames reaches the avg_frame_count, it calculates the FPS
        based on the time elapsed and resets the counter and start time.
        """
        self.frame_counter += 1  # Increment the frame counter
        if self.frame_counter % self.avg_frame_count == 0:
            # If frame_counter reaches avg_frame_count, calculate FPS
            end_time = time.time()  # Current time
            self.fps = self.avg_frame_count / (end_time - self.start_time)  # Calculate FPS
            self.start_time = end_time  # Reset start time for the next FPS calculation

    def get_fps(self):
        """
        Returns the current calculated FPS.

        :return: Calculated frames per second.
        """
        return self.fps  # Return the most recently calculated FPS

